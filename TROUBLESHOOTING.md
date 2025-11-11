# AWIES 故障排除指南

## 端口配置已更新

✅ **后端端口**: 53431
✅ **前端端口**: 3003

---

## 快速启动步骤

### 1. 启动后端（终端1）

```bash
cd backend

# 如果还没有 .env 文件，创建它
cp .env.example .env

# 编辑 .env，添加你的 API 密钥
# nano .env 或 vim .env

# 启动后端
./start.sh
```

后端应该在 `http://localhost:53431` 启动

**测试后端：**
```bash
curl http://localhost:53431/api/health
```

### 2. 启动前端（终端2）

```bash
cd frontend

# 启动前端
./start.sh
```

前端应该在 `http://localhost:3003` 启动

---

## 前端无法打开？按以下步骤排查

### 步骤 1: 检查 Node.js 版本

```bash
node --version
```

需要 **Node.js 18 或更高**。如果版本太低：

```bash
# 使用 nvm 安装最新版本
nvm install 18
nvm use 18
```

### 步骤 2: 清理并重新安装依赖

```bash
cd frontend

# 删除旧的依赖
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

### 步骤 3: 手动启动前端

```bash
cd frontend
npm run dev
```

如果看到错误，请记录错误信息。

### 步骤 4: 检查端口占用

```bash
# 检查 3003 端口是否被占用
lsof -i :3003

# 如果被占用，杀死进程
kill -9 <PID>
```

### 步骤 5: 使用测试页面

打开浏览器访问：
```
http://localhost:3003/test.html
```

这个简单的 HTML 页面可以测试后端连接。

---

## 常见错误及解决方案

### 错误 1: "Cannot find module '@vitejs/plugin-react'"

**解决：**
```bash
cd frontend
npm install @vitejs/plugin-react --save-dev
```

### 错误 2: "Failed to resolve import"

**解决：**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 错误 3: "EADDRINUSE: address already in use"

**解决：**
```bash
# 查找占用端口的进程
lsof -i :3003

# 杀死进程
kill -9 <PID>

# 或者修改端口
# 编辑 frontend/vite.config.ts
# 将 port: 3003 改为其他端口
```

### 错误 4: "Network: use --host to expose"

这是正常的！Vite 默认只监听 localhost。

访问 `http://localhost:3003` 即可。

### 错误 5: 前端启动了但页面空白

**检查浏览器控制台：**
1. 按 F12 打开开发者工具
2. 查看 Console 标签
3. 查看是否有错误信息

**常见原因：**
- 后端没有启动（检查 http://localhost:53431/api/health）
- CORS 错误（检查后端日志）
- 模块导入错误（清理并重装依赖）

### 错误 6: "Failed to fetch" 或 CORS 错误

**解决：**
1. 确保后端在运行
2. 检查后端 CORS 配置：
   ```bash
   # 检查 backend/.env
   CORS_ORIGINS=["http://localhost:3003","http://localhost:5173"]
   ```
3. 重启后端服务器

---

## 直接测试后端 API

### 测试健康检查
```bash
curl http://localhost:53431/api/health
```

**预期输出：**
```json
{
  "status": "healthy",
  "timestamp": "2024-...",
  "version": "1.0.0"
}
```

### 测试文本分析
```bash
curl -X POST "http://localhost:53431/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a big problem in modern research.",
    "discipline": "computer_science"
  }'
```

### 测试文档页面

打开浏览器访问：
```
http://localhost:53431/docs
```

这会打开自动生成的 API 文档（Swagger UI）。

---

## 完整的前端依赖安装

如果 `npm install` 失败，可以逐个安装：

```bash
cd frontend

# 核心依赖
npm install react react-dom
npm install antd @ant-design/icons
npm install axios
npm install diff
npm install @monaco-editor/react
npm install chart.js react-chartjs-2

# 开发依赖
npm install -D @vitejs/plugin-react
npm install -D vite
npm install -D typescript
npm install -D @types/react
npm install -D @types/react-dom
npm install -D @types/diff
```

---

## 检查清单

在联系支持之前，请检查：

- [ ] Node.js 版本 >= 18
- [ ] Python 版本 >= 3.10
- [ ] 后端 .env 文件已配置
- [ ] 后端 API 密钥已添加
- [ ] 后端在 53431 端口运行
- [ ] 前端依赖已安装（node_modules 存在）
- [ ] 3003 端口未被占用
- [ ] 浏览器控制台无错误
- [ ] 测试页面可以访问后端

---

## 查看日志

### 后端日志
后端会在终端输出日志。查找：
- `INFO` - 正常信息
- `ERROR` - 错误信息
- `WARNING` - 警告信息

### 前端日志
1. 打开浏览器开发者工具（F12）
2. 查看 Console 标签
3. 查看 Network 标签（检查 API 请求）

---

## 最简单的测试方法

### 方法 1: 使用测试页面

1. 确保后端在运行
2. 访问 `http://localhost:53431/docs`
3. 在 Swagger UI 中测试 API

### 方法 2: 使用 curl

```bash
# 测试健康检查
curl http://localhost:53431/api/health

# 测试分析
curl -X POST "http://localhost:53431/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text":"test","discipline":"general"}'
```

### 方法 3: 使用静态测试页面

访问：`http://localhost:3003/test.html`

这个页面不依赖 React，可以快速测试后端连接。

---

## 仍然无法解决？

请提供以下信息：

1. **系统信息**
   ```bash
   node --version
   python --version
   npm --version
   ```

2. **错误信息**
   - 后端终端输出
   - 前端终端输出
   - 浏览器控制台错误

3. **端口检查**
   ```bash
   lsof -i :53431
   lsof -i :3003
   ```

4. **网络测试**
   ```bash
   curl http://localhost:53431/api/health
   ```

---

## 端口配置总结

| 服务 | 旧端口 | 新端口 | URL |
|------|--------|--------|-----|
| 后端 | 8000 | **53431** | http://localhost:53431 |
| 前端 | 3000 | **3003** | http://localhost:3003 |
| API 文档 | - | **53431** | http://localhost:53431/docs |
| 测试页面 | - | **3003** | http://localhost:3003/test.html |

---

**祝调试顺利！如果还有问题，请提供具体错误信息。** 🚀
