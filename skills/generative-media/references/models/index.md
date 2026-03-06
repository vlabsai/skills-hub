# Model Selection Guide

Quick reference for choosing the right model. Detailed guides in individual model files.

## Model Comparison

| Feature | Nano Banana 2 (Gemini 3.1 Flash) | FLUX.2 Pro | FLUX.2 Flex |
|---------|---------------------------|------------|-------------|
| **Provider** | Google via OpenRouter | Black Forest Labs via OpenRouter | Black Forest Labs via OpenRouter |
| **Generation** | Yes | Yes | Yes |
| **Editing** | Yes (send image + instructions) | No | No |
| **Max resolution** | 4K (~4096px) | ~4MP (multiples of 16) | ~4MP (multiples of 16) |
| **Speed** | 20-40s (can spike 180s+ at peak) | 3-8s | 2-5s |
| **Cost** | ~$0.04-0.08/image | ~$0.05/image | ~$0.02/image |
| **Text rendering** | Good (best overall) | Moderate | Good (best FLUX variant) |
| **Photorealism** | Excellent | Excellent | Good |
| **Illustration** | Good | Excellent | Good |
| **HEX color control** | Good | Excellent | Excellent |
| **Negative prompts** | Rephrase as positives | Not supported | Not supported |
| **Prompt style** | Natural language, conversational | Keyword-rich, structured | Keyword-rich, structured |
| **API key** | OPENROUTER_API_KEY | OPENROUTER_API_KEY | OPENROUTER_API_KEY |

## Decision Tree

1. **Need to edit an existing image?** → Nano Banana (only option with editing)
2. **Need text rendered in the image?** → Nano Banana (best overall) or FLUX.2 Flex (good + fast)
3. **Need 2K/4K resolution?** → Nano Banana (explicit size tiers)
4. **Need exact brand colors?** → FLUX.2 Pro/Flex (strongest HEX matching)
5. **Need artistic/illustration style?** → FLUX.2 Pro (strongest for creative styles)
6. **Need photorealistic image?** → Nano Banana or FLUX.2 Pro (both excellent)
7. **Need fast/cheap exploration?** → FLUX.2 Flex ($0.02/img, 2-5s)
8. **Default choice** → Nano Banana (most versatile)

## API Key Setup

All models use OpenRouter. Single key for everything:

```bash
export OPENROUTER_API_KEY="your-key-here"
```

Get a key at https://openrouter.ai/keys
