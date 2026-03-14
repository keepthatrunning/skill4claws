const axios = require('axios');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const BASE_URL = 'https://api-inference.modelscope.cn/';
const CONFIG_FILE = '.modelscope_config.enc';
const ALGORITHM = 'aes-256-gcm';

/**
 * Secure Secret Manager
 * 安全的密钥管理模块
 */
class SecureSecretManager {
    constructor() {
        this.configPath = path.join(__dirname, CONFIG_FILE);
        this.keyPath = path.join(__dirname, '.key');
    }

    /**
     * 生成或加载加密密钥
     */
    getOrCreateKey() {
        if (fs.existsSync(this.keyPath)) {
            // 检查密钥文件权限
            const stats = fs.statSync(this.keyPath);
            const mode = stats.mode & 0o777;
            if (mode !== 0o600) {
                throw new Error(
                    `Key file permissions too open (${mode.toString(8)}). ` +
                    `Run: chmod 600 ${this.keyPath}`
                );
            }
            return fs.readFileSync(this.keyPath);
        }

        // 生成新密钥
        const key = crypto.randomBytes(32);
        fs.writeFileSync(this.keyPath, key, { mode: 0o600 });
        console.log('Generated new encryption key');
        return key;
    }

    /**
     * 加密并存储 API Key
     */
    storeApiKey(apiKey) {
        const key = this.getOrCreateKey();
        const iv = crypto.randomBytes(16);
        const cipher = crypto.createCipheriv(ALGORITHM, key, iv);
        
        let encrypted = cipher.update(apiKey, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        
        const authTag = cipher.getAuthTag();
        
        const data = {
            iv: iv.toString('hex'),
            authTag: authTag.toString('hex'),
            encrypted: encrypted,
            createdAt: new Date().toISOString()
        };

        fs.writeFileSync(this.configPath, JSON.stringify(data), { mode: 0o600 });
        console.log('API key stored securely');
    }

    /**
     * 读取并解密 API Key
     */
    loadApiKey() {
        // 优先从加密配置文件读取
        if (fs.existsSync(this.configPath)) {
            // 检查配置文件权限
            const stats = fs.statSync(this.configPath);
            const mode = stats.mode & 0o777;
            if (mode !== 0o600) {
                throw new Error(
                    `Config file permissions too open (${mode.toString(8)}). ` +
                    `Run: chmod 600 ${this.configPath}`
                );
            }

            const key = this.getOrCreateKey();
            const data = JSON.parse(fs.readFileSync(this.configPath, 'utf8'));
            
            const decipher = crypto.createDecipheriv(
                ALGORITHM,
                key,
                Buffer.from(data.iv, 'hex')
            );
            decipher.setAuthTag(Buffer.from(data.authTag, 'hex'));
            
            let decrypted = decipher.update(data.encrypted, 'hex', 'utf8');
            decrypted += decipher.final('utf8');
            
            return decrypted;
        }

        // 回退到环境变量（仅用于迁移）
        const envKey = process.env.MODELSCOPE_API_KEY;
        if (envKey) {
            console.warn('Warning: Using environment variable. Consider migrating to secure storage.');
            // 自动迁移到安全存储
            this.storeApiKey(envKey);
            return envKey;
        }

        return null;
    }

    /**
     * 验证 API Key 格式
     */
    validateApiKey(key) {
        if (!key || typeof key !== 'string') {
            return { valid: false, error: 'API key is empty' };
        }

        // ModelScope API key 格式验证
        if (!key.startsWith('ms-')) {
            return { valid: false, error: 'Invalid API key format. Must start with "ms-"' };
        }

        if (key.length < 20) {
            return { valid: false, error: 'API key too short' };
        }

        // 检查是否包含可疑字符（防止注入）
        const suspiciousPattern = /[<>\"'&;|$]/;
        if (suspiciousPattern.test(key)) {
            return { valid: false, error: 'API key contains invalid characters' };
        }

        return { valid: true };
    }
}

// 全局密钥管理实例
const secretManager = new SecureSecretManager();

async function generateImage(prompt, options = {}) {
    // 安全获取 API Key
    let apiKey;
    try {
        apiKey = secretManager.loadApiKey();
    } catch (error) {
        console.error('Error loading API key:', error.message);
        process.exit(1);
    }

    if (!apiKey) {
        console.error('Error: MODELSCOPE_API_KEY not set.');
        console.error('Options:');
        console.error('  1. Set environment variable: export MODELSCOPE_API_KEY="ms-xxx"');
        console.error('  2. Run setup: node index.js --setup');
        process.exit(1);
    }

    // 验证 API Key 格式
    const validation = secretManager.validateApiKey(apiKey);
    if (!validation.valid) {
        console.error('Error: Invalid API key:', validation.error);
        process.exit(1);
    }

    const outputFile = options.output || 'result_image.jpg';
    const model = options.model || 'Tongyi-MAI/Z-Image-Turbo';

    // 只发送必要的请求头，不包含其他环境变量
    const headers = {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
    };

    try {
        console.log(`Generating image with prompt: "${prompt}"`);
        console.log(`Using model: ${model}`);
        
        // Step 1: Submit generation task
        console.log('Submitting task...');
        const submitResponse = await axios.post(
            `${BASE_URL}v1/images/generations`,
            {
                model: model,
                prompt: prompt
            },
            {
                headers: {
                    ...headers,
                    'X-ModelScope-Async-Mode': 'true'
                },
                // 设置超时，防止长时间挂起
                timeout: 30000
            }
        );

        const taskId = submitResponse.data.task_id;
        console.log(`Task submitted. Task ID: ${taskId}`);

        // Step 2: Poll for result
        console.log('Waiting for generation to complete...');
        let imageUrl = null;
        let attempts = 0;
        const maxAttempts = 60; // 最多等待 5 分钟
        
        while (attempts < maxAttempts) {
            await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds
            attempts++;
            
            const resultResponse = await axios.get(
                `${BASE_URL}v1/tasks/${taskId}`,
                {
                    headers: {
                        ...headers,
                        'X-ModelScope-Task-Type': 'image_generation'
                    },
                    timeout: 10000
                }
            );

            const data = resultResponse.data;
            console.log(`Task status: ${data.task_status}`);

            if (data.task_status === 'SUCCEED') {
                imageUrl = data.output_images[0];
                break;
            } else if (data.task_status === 'FAILED') {
                throw new Error('Image generation failed: ' + JSON.stringify(data));
            }
        }

        if (!imageUrl) {
            throw new Error('Image generation timeout after 5 minutes');
        }

        // Step 3: Download image
        console.log(`Downloading image from: ${imageUrl}`);
        const imageResponse = await axios.get(imageUrl, {
            responseType: 'arraybuffer',
            timeout: 30000
        });

        // Save image
        fs.writeFileSync(outputFile, imageResponse.data);
        console.log(`✅ Image saved to: ${outputFile}`);
        
        return {
            success: true,
            outputFile: path.resolve(outputFile),
            imageUrl: imageUrl
        };

    } catch (error) {
        console.error('Error:', error.message);
        if (error.response) {
            console.error('Response status:', error.response.status);
            // 只打印必要的错误信息，不暴露敏感数据
            const safeData = { ...error.response.data };
            delete safeData.token;
            delete safeData.api_key;
            delete safeData.secret;
            console.error('Response data:', safeData);
        }
        process.exit(1);
    }
}

// Setup mode - securely store API key
function setupMode() {
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    console.log('=== ModelScope Image Generator Setup ===');
    console.log('This will securely store your API key with encryption.');
    console.log('');

    rl.question('Enter your ModelScope API key: ', (apiKey) => {
        const validation = secretManager.validateApiKey(apiKey);
        if (!validation.valid) {
            console.error('Error:', validation.error);
            rl.close();
            process.exit(1);
        }

        try {
            secretManager.storeApiKey(apiKey);
            console.log('✅ API key stored securely!');
            console.log('');
            console.log('You can now run:');
            console.log('  node index.js "Your prompt here"');
            console.log('');
            console.log('Your API key is encrypted and stored in:');
            console.log(`  ${secretManager.configPath}`);
        } catch (error) {
            console.error('Error storing API key:', error.message);
            process.exit(1);
        }

        rl.close();
    });
}

// Parse command line arguments
function parseArgs() {
    const args = process.argv.slice(2);
    const options = {};
    let prompt = '';

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--output' || args[i] === '-o') {
            options.output = args[i + 1];
            i++;
        } else if (args[i] === '--model' || args[i] === '-m') {
            options.model = args[i + 1];
            i++;
        } else if (args[i] === '--setup') {
            options.setup = true;
        } else if (!prompt) {
            prompt = args[i];
        } else {
            prompt += ' ' + args[i];
        }
    }

    return { prompt, options };
}

// Main
if (require.main === module) {
    const { prompt, options } = parseArgs();
    
    if (options.setup) {
        setupMode();
    } else if (!prompt) {
        console.log('ModelScope Image Generator (Secure Edition)');
        console.log('');
        console.log('Usage:');
        console.log('  Setup:     node index.js --setup');
        console.log('  Generate:  node index.js "Your prompt here" [--output filename.jpg]');
        console.log('');
        console.log('Options:');
        console.log('  --setup         Securely store your API key');
        console.log('  --output, -o    Output filename (default: result_image.jpg)');
        console.log('  --model, -m     Model ID (default: Tongyi-MAI/Z-Image-Turbo)');
        console.log('');
        console.log('Features:');
        console.log('  ✅ Encrypted API key storage (AES-256-GCM)');
        console.log('  ✅ File permission checks (600)');
        console.log('  ✅ API key format validation');
        console.log('  ✅ No credential exposure in error messages');
        console.log('  ✅ Request timeouts to prevent hanging');
        console.log('');
        process.exit(0);
    } else {
        generateImage(prompt, options);
    }
}

module.exports = { generateImage, SecureSecretManager };
