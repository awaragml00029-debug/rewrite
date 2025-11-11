# 🔧 修复配置问题

## 问题诊断

从错误日志看到：

### 问题 1: Enhanced Text 没有变化
**原因**: LLM API 配置错误导致改写失败
- 你在使用 `gemini-2.5-flash` 模型
- 但配置的 `LLM_PROVIDER=openai`
- API 端点: `https://off.092420.xyz/v1/chat/completions`
- **API 拒绝了 OpenAI 格式的请求**

**错误信息**:
```
Unknown name "messages": Cannot find field.
Unknown name "max_tokens": Cannot find field.
Unknown name "temperature": Cannot find field.
```

这说明你的 API 期望 Gemini 格式，而不是 OpenAI 格式！

### 问题 2: Literature Recommendations 为空
**原因**: JANE API 可能无法访问（外部服务）
- JANE 是第三方服务，可能暂时不可用
- 这不会影响核心改写功能

---

## ✅ 解决方案

### 步骤 1: 修复 .env 配置

编辑 `backend/.env` 文件：

#### 选项 A: 使用你的 Gemini API 代理

```bash
# 如果你的 API 是 Gemini 格式的代理
LLM_PROVIDER=gemini
LLM_API_KEY=你的API密钥
LLM_BASE_URL=https://off.092420.xyz/v1beta
LLM_MODEL=gemini-2.5-flash

# 注意：
# 1. PROVIDER 必须设为 "gemini"
# 2. 从 URL 中移除 "/chat/completions"
# 3. 使用 /v1beta 而不是 /v1
```

#### 选项 B: 使用标准 Gemini API

```bash
LLM_PROVIDER=gemini
LLM_API_KEY=你的Gemini密钥
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta
LLM_MODEL=gemini-pro
```

#### 选项 C: 使用 OpenAI API

```bash
LLM_PROVIDER=openai
LLM_API_KEY=sk-你的OpenAI密钥
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo
```

### 步骤 2: 重启后端服务器

```bash
# 停止当前服务器 (Ctrl+C)
# 然后重新启动
cd backend
./start.sh
```

### 步骤 3: 测试

```bash
# 测试健康检查
curl http://localhost:53431/api/health

# 测试文本分析 (不需要 LLM)
curl -X POST "http://localhost:53431/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a test.",
    "discipline": "general"
  }'

# 测试改写 (需要 LLM)
curl -X POST "http://localhost:53431/api/enhance" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a test.",
    "level": 1,
    "discipline": "general"
  }'
```

---

## 📋 配置检查清单

### 必须匹配的配置

| 如果你的 API 是... | 那么配置应该是... |
|-------------------|------------------|
| Gemini API | `LLM_PROVIDER=gemini` |
| OpenAI API | `LLM_PROVIDER=openai` |
| 使用 gemini 模型 | `LLM_PROVIDER=gemini` |
| 使用 gpt 模型 | `LLM_PROVIDER=openai` |
| URL 包含 generativelanguage.googleapis.com | `LLM_PROVIDER=gemini` |
| URL 包含 openai.com | `LLM_PROVIDER=openai` |

### URL 格式

| Provider | 正确的 URL 格式 | 错误的格式 |
|----------|---------------|-----------|
| gemini | `https://xxx.com/v1beta` | `https://xxx.com/v1/chat/completions` ❌ |
| openai | `https://xxx.com/v1` | `https://xxx.com/v1beta` ❌ |

---

## 🧪 快速测试脚本

创建一个测试文件 `test_config.sh`:

```bash
#!/bin/bash

echo "Testing AWIES Configuration..."
echo

# Load .env
export $(cat backend/.env | grep -v '^#' | xargs)

echo "Current Configuration:"
echo "  Provider: $LLM_PROVIDER"
echo "  Model: $LLM_MODEL"
echo "  Base URL: $LLM_BASE_URL"
echo

# Check for mismatches
if [[ "$LLM_MODEL" == *"gemini"* ]] && [[ "$LLM_PROVIDER" != "gemini" ]]; then
    echo "❌ ERROR: Model is Gemini but provider is $LLM_PROVIDER"
    exit 1
fi

if [[ "$LLM_PROVIDER" == "gemini" ]] && [[ "$LLM_BASE_URL" == *"/chat/completions"* ]]; then
    echo "❌ ERROR: Gemini provider but URL contains /chat/completions"
    exit 1
fi

echo "✅ Configuration looks correct"
```

运行:
```bash
chmod +x test_config.sh
./test_config.sh
```

---

## 🆘 仍然有问题？

### 查看后端日志

后端启动时会显示：
```
INFO - Initialized [Provider] client with model: [Model]
```

如果看到 `OpenAI client with model: gemini-2.5-flash`，说明配置错误！

应该是：
- `Gemini client with model: gemini-2.5-flash` ✅

### 常见错误

#### 错误 1: "Invalid JSON payload received"
- **原因**: Provider 和 API 格式不匹配
- **解决**: 检查 `LLM_PROVIDER` 设置

#### 错误 2: "Authentication failed"
- **原因**: API 密钥错误
- **解决**: 检查 `LLM_API_KEY`

#### 错误 3: "Connection refused"
- **原因**: API URL 错误
- **解决**: 检查 `LLM_BASE_URL`

---

## 📝 完整的正确配置示例

### Gemini API (你的情况)

```bash
# backend/.env

API_HOST=0.0.0.0
API_PORT=53431
API_RELOAD=true

# Gemini Configuration
LLM_PROVIDER=gemini
LLM_API_KEY=your-actual-api-key-here
LLM_BASE_URL=https://off.092420.xyz/v1beta
LLM_MODEL=gemini-2.5-flash

# JANE API Configuration
JANE_WSDL_URL=http://jane.biosemantics.org:8080/JaneServer/services/JaneSOAPServer?wsdl
JANE_BASE_URL=http://jane.biosemantics.org/

REDIS_ENABLED=false
CORS_ORIGINS=["http://localhost:3003","http://localhost:5173"]
CACHE_TTL=3600
ENABLE_CACHE=true
LOG_LEVEL=INFO
```

---

## ✅ 配置成功的标志

重启后端后，应该看到：

```
INFO - Initialized Gemini client with model: gemini-2.5-flash
INFO - Starting AWIES backend server...
INFO - Application startup complete
```

在前端测试改写功能，应该看到：
- ✅ 文本分析正常工作
- ✅ Enhanced Text 有实际变化
- ✅ 显示修改建议和原因

JANE 推荐可能为空（这是正常的，外部服务可能不可用）。

---

**配置完成后，记得重启后端服务器！** 🚀
