// 图片生成触发器 - 集成到飞书聊天
// 触发词: 画、生成图片、/image、/img

const { generateImage } = require('./index.js');
const fs = require('fs');
const path = require('path');

// 设置API Key
process.env.MODELSCOPE_API_KEY = 'ms-886b0bb9-c1e5-476b-914a-5bfaeba4edbf';

/**
 * 解析用户消息，提取图片生成提示词
 */
function parseImagePrompt(message) {
    const triggers = [
        { keyword: '画', remove: true },
        { keyword: '生成图片', remove: true },
        { keyword: '/image', remove: true },
        { keyword: '/img', remove: true },
        { keyword: '画一个', remove: true },
        { keyword: '画一张', remove: true },
        { keyword: '画幅', remove: true }
    ];
    
    let prompt = message.trim();
    
    for (const trigger of triggers) {
        if (prompt.toLowerCase().startsWith(trigger.keyword.toLowerCase())) {
            prompt = prompt.substring(trigger.keyword.length).trim();
            // 移除开头的标点符号
            prompt = prompt.replace(/^[，。！？,.!?]/, '').trim();
            break;
        }
    }
    
    return prompt;
}

/**
 * 检查消息是否是图片生成请求
 */
function isImageGenRequest(message) {
    const triggers = ['画', '生成图片', '/image', '/img'];
    return triggers.some(trigger => 
        message.toLowerCase().startsWith(trigger.toLowerCase())
    );
}

/**
 * 生成图片并返回结果
 */
async function generateImageFromMessage(message, options = {}) {
    const prompt = parseImagePrompt(message);
    
    if (!prompt || prompt.length < 2) {
        return {
            success: false,
            error: '请提供图片描述，例如："画一只可爱的猫"'
        };
    }
    
    const timestamp = new Date().getTime();
    const outputDir = '/workspace/projects/workspace/temp';
    const outputFile = path.join(outputDir, `img_${timestamp}.jpg`);
    
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    
    try {
        console.log(`[ImageGen] 🎨 生成图片: "${prompt}"`);
        
        const result = await generateImage(prompt, {
            output: outputFile
        });
        
        console.log(`[ImageGen] ✅ 成功: ${result.outputFile}`);
        
        return {
            success: true,
            outputFile: result.outputFile,
            prompt: prompt,
            message: `🎨 根据描述 "${prompt}" 生成的图片`
        };
        
    } catch (error) {
        console.error('[ImageGen] ❌ 错误:', error.message);
        return {
            success: false,
            error: error.message,
            prompt: prompt
        };
    }
}

module.exports = {
    isImageGenRequest,
    parseImagePrompt,
    generateImageFromMessage
};

// 如果是直接运行测试
if (require.main === module) {
    const message = process.argv.slice(2).join(' ');
    
    if (!message) {
        console.log('🎨 ModelScope 图片生成器');
        console.log('');
        console.log('使用方法:');
        console.log('  node image-gen-trigger.js "画一只可爱的猫"');
        console.log('  node image-gen-trigger.js "生成图片 夕阳下的海滩"');
        console.log('');
        process.exit(0);
    }
    
    generateImageFromMessage(message).then(result => {
        if (result.success) {
            console.log(result.message);
            console.log(`📁 文件: ${result.outputFile}`);
        } else {
            console.error('❌ 错误:', result.error);
            process.exit(1);
        }
    });
}
