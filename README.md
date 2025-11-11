# AWIES - Academic Writing Intelligence Enhancement System

一个智能学术写作提升系统，帮助非英语母语研究者提升英文论文写作质量。

## 🎯 核心功能

- **多级文本改写** (4个级别)
  - Level 1: 基础纠错
  - Level 2: Native表达优化
  - Level 3: 学术规范强化
  - Level 4: 整体润色

- **全方位文本分析**
  - 词汇分析（多样性、简单词汇检测）
  - 句法分析（复杂度、句式多样性）
  - 语篇分析（连贯性、过渡词使用）

- **智能文献推荐** (基于JANE API)
  - 期刊推荐
  - 相关论文推荐
  - 潜在合作者推荐

- **实时进度显示**
  - 分阶段处理
  - 进度百分比
  - 预计剩余时间

## 🏗️ 项目结构

```
awies/
├── backend/              # FastAPI后端
│   ├── app/
│   │   ├── api/         # API路由
│   │   ├── core/        # 配置
│   │   ├── services/    # 核心服务
│   │   │   ├── llm_client.py         # LLM集成 (OpenAI/Gemini)
│   │   │   ├── text_analyzer.py      # 文本分析
│   │   │   ├── enhancement_engine.py # 改写引擎
│   │   │   └── jane_client.py        # JANE API集成
│   │   ├── models/      # 数据模型
│   │   └── main.py      # 主应用
│   ├── tests/           # 测试
│   ├── requirements.txt
│   ├── .env.example
│   └── start.sh         # 启动脚本
│
├── frontend/            # React前端 (待实现)
│   ├── src/
│   │   ├── components/  # UI组件
│   │   ├── hooks/       # 自定义Hooks
│   │   ├── services/    # API服务
│   │   └── types/       # TypeScript类型
│   └── package.json
│
└── AWIES_Complete_Design_Document.md  # 完整设计文档
```

## 🚀 快速开始

### 后端设置

1. **安装依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，添加你的API密钥
   ```

3. **启动服务器**
   ```bash
   # 使用启动脚本（推荐）
   ./start.sh

   # 或手动启动
   python -m app.main
   ```

4. **访问API文档**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### 配置示例

在 `.env` 文件中配置你的LLM API：

**使用OpenAI:**
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-key-here
LLM_MODEL=gpt-4
```

**使用Gemini:**
```env
LLM_PROVIDER=gemini
LLM_API_KEY=your-gemini-key
LLM_MODEL=gemini-pro
```

**使用本地模型 (OpenAI兼容):**
```env
LLM_PROVIDER=openai
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=not-needed
LLM_MODEL=local-model
```

## 📖 API使用示例

### 1. 文本分析

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a big problem in modern research.",
    "discipline": "computer_science"
  }'
```

### 2. 文本改写

```bash
# 创建改写任务
curl -X POST "http://localhost:8000/api/enhance" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "We need to make research on this topic.",
    "level": 2,
    "discipline": "general"
  }'

# 返回: {"job_id": "xxx-xxx-xxx", "status": "pending"}

# 查询进度
curl "http://localhost:8000/api/enhance/status/xxx-xxx-xxx"
```

### 3. 获取期刊推荐

```bash
curl -X POST "http://localhost:8000/api/recommendations/journals" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Machine learning applications in medical diagnosis...",
    "limit": 10
  }'
```

## 🎨 前端组件（设计已完成）

前端使用React + TypeScript + Ant Design，包含：

- **MainEditor** - 主编辑器组件
- **DiffViewer** - 对比显示组件
- **AnalysisPanel** - 分析结果面板
- **EnhancementProgress** - 进度指示器
- **RecommendationPanel** - 推荐面板

详细设计见 `AWIES_Complete_Design_Document.md` 第7章。

## 🔧 技术栈

### 后端
- **FastAPI** - 现代化Python Web框架
- **LLM Integration** - OpenAI / Gemini API
- **NLP** - spaCy, NLTK, textstat
- **JANE API** - 期刊/文献推荐

### 前端（待实现）
- **React 18** + TypeScript
- **Ant Design** - UI组件库
- **Monaco Editor** - 代码编辑器
- **Chart.js** - 数据可视化
- **diff** - 文本对比

## 📊 改写级别说明

| 级别 | 名称 | 功能 | 适用场景 |
|------|------|------|---------|
| Level 1 | 基础纠错 | 语法、拼写、标点 | 草稿阶段 |
| Level 2 | Native表达 | 地道表达、搭配 | 提升流畅度 |
| Level 3 | 学术规范 | 学术词汇、语态 | 投稿准备 |
| Level 4 | 整体润色 | 语篇结构、连贯性 | 最终审校 |

## 🎓 支持的学科

- Computer Science (计算机科学)
- Biology (生物学)
- Social Sciences (社会科学)
- Engineering (工程学)
- General (通用学术)

每个学科有专门的写作规范和风格指导。

## ⚡ 性能优化

### 限速因素
1. **LLM API调用** - 最慢 (5-30秒)
   - 优化：分段处理、缓存
2. **JANE API** - 中等 (5-15秒)
   - 优化：并发请求、Redis缓存
3. **文本分析** - 快 (<2秒)
4. **前端渲染** - 很快 (<0.5秒)

### 优化建议
- 启用Redis缓存
- 使用异步处理
- 较短文本用Level 1-2
- 考虑本地LLM模型

## 🧪 测试

```bash
cd backend
pytest tests/
```

## 📝 开发计划

- [x] 完整设计文档
- [x] 后端API实现
- [x] LLM集成（OpenAI/Gemini）
- [x] 文本分析模块
- [x] 改写引擎
- [x] JANE API集成
- [ ] 前端React实现
- [ ] 前后端联调
- [ ] Docker部署
- [ ] 性能优化

## 🤝 贡献

欢迎提Issue和Pull Request！

## 📄 License

MIT License

---

## 常见问题

### Q: 如何切换LLM提供商？

A: 编辑 `.env` 文件，修改 `LLM_PROVIDER` 为 `openai` 或 `gemini`。

### Q: 可以使用本地模型吗？

A: 可以！设置 `LLM_PROVIDER=openai`，然后配置 `LLM_BASE_URL` 指向你的本地OpenAI兼容服务器（如LM Studio、Ollama等）。

### Q: JANE API连接失败怎么办？

A: JANE是外部服务，可能临时不可用。系统会优雅降级，返回空推荐列表不会影响核心改写功能。

### Q: 改写速度太慢？

A:
1. 使用更低的改写级别（Level 1-2更快）
2. 分段处理长文本
3. 考虑使用本地LLM模型
4. 启用Redis缓存

---

**开发者**: AWIES Team
**最后更新**: 2024-01-30
