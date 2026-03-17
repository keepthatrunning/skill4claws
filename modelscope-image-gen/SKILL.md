---
name: modelscope-image-gen
description: Generate images using ModelScope (魔塔社区) API with Tongyi-MAI/Z-Image-Turbo model.
---
# ModelScope Image Generator

使用魔塔社区(ModelScope) API 生成AI图片，基于通义万相(Z-Image-Turbo)模型。

## Configuration
- API Key: Set `MODELSCOPE_API_KEY` environment variable.

## Usage
```bash
export MODELSCOPE_API_KEY="your_api_key_here"
node skills/modelscope-image-gen/index.js "Your prompt here" [--output <filename>]
```

## Options
- `--output`: Output filename (Default: result_image.jpg)
- `--model`: Model ID (Default: Tongyi-MAI/Z-Image-Turbo)

## Example
```bash
node skills/modelscope-image-gen/index.js "一只金色的猫在草地上玩耍"
node skills/modelscope-image-gen/index.js "A beautiful sunset over mountains" --output sunset.jpg
```

## API Reference
- Base URL: https://api-inference.modelscope.cn/
- Model: Tongyi-MAI/Z-Image-Turbo
- Mode: Async (轮询获取结果)
