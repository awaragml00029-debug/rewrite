# API Configuration Guide for OhMyGPT

## Problem Diagnosis

Based on your logs, the current configuration is using:
- **Model**: `gpt-5-nano`
- **Base URL**: `https://api.ohmygpt.com/v1`
- **Issues**:
  - Returns 0 characters (empty responses)
  - Only supports `temperature=1` (default value)
  - Not suitable for text enhancement tasks

## Recommended Configuration

According to the OhMyGPT API documentation, use one of these supported models:

### Option 1: GPT-4o (Recommended)
```bash
LLM_PROVIDER=openai
LLM_API_KEY=<YOUR_OHMYGPT_API_KEY>
LLM_BASE_URL=https://api.ohmygpt.com/v1
LLM_MODEL=gpt-4o
```

### Option 2: Gemini 2.0 Flash
```bash
LLM_PROVIDER=openai
LLM_API_KEY=<YOUR_OHMYGPT_API_KEY>
LLM_BASE_URL=https://api.ohmygpt.com/v1
LLM_MODEL=gemini-2.0-flash-001
```

### Option 3: Claude (if available)
```bash
LLM_PROVIDER=openai
LLM_API_KEY=<YOUR_OHMYGPT_API_KEY>
LLM_BASE_URL=https://api.ohmygpt.com/v1
LLM_MODEL=claude-3-5-sonnet-20241022
```

## How to Fix

### Step 1: Update Configuration

Edit `/home/user/rewrite/backend/.env`:

```bash
cd /home/user/rewrite/backend
nano .env
```

Change these lines:
```bash
LLM_PROVIDER=openai
LLM_API_KEY=<YOUR_ACTUAL_API_KEY>
LLM_BASE_URL=https://api.ohmygpt.com/v1
LLM_MODEL=gpt-4o
```

### Step 2: Test Configuration

Run the test script:
```bash
cd /home/user/rewrite/backend
python test_api.py
```

Expected output:
```
✅ Success!
Response length: 150 characters
✅ Configuration appears to be working!
```

### Step 3: Restart Backend

```bash
cd /home/user/rewrite/backend
./start.sh
```

## Why gpt-5-nano Doesn't Work

1. **Empty Responses**: The model returns 0 characters, which breaks the enhancement pipeline
2. **Temperature Restriction**: Only supports default temperature (1.0), no customization
3. **Not Listed**: Not in OhMyGPT's official model list

## Verification

After changing the configuration and restarting, check the logs:

**Before (broken):**
```
OpenAI API retry success: received 0 characters
Level 1 completed: 1182 chars -> 0 chars
```

**After (working):**
```
OpenAI API response: 1250 characters
Level 1 completed: 1182 chars -> 1250 chars
```

## Need Help?

If you still have issues:

1. Run `python test_api.py` to diagnose
2. Check API key is valid
3. Verify you have access to the selected model
4. Review logs in `/home/user/rewrite/backend/logs/`

## Reference

- OhMyGPT API Docs: https://api.ohmygpt.com/docs (if available)
- Your API console for model availability
