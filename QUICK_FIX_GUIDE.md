# 快速故障排除指南

## 界面美化不生效？

### 方法1：强制刷新浏览器
```bash
# Chrome/Edge: Ctrl + Shift + R
# Firefox: Ctrl + F5
# 或打开开发者工具 (F12) → Network → 勾选 "Disable cache"
```

### 方法2：清除Vite缓存并重启
```bash
cd /home/user/rewrite/frontend
rm -rf node_modules/.vite
npm run dev
```

### 方法3：硬重置
```bash
cd /home/user/rewrite/frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## Authors API 500错误？

### 问题原因
JANE API (jane.biosemantics.org) 是外部服务，经常不可用或返回错误。

### 解决方案
这是**正常行为** - 不影响核心功能。系统会优雅降级：
- Authors推荐可能为空
- Papers推荐仍然可用
- 不影响文本增强功能

### 如果想禁用JANE API
编辑 `backend/app/api/routes.py`，在recommendations路由中添加try-except：

```python
try:
    authors = await jane_client.find_potential_collaborators(...)
except Exception as e:
    logger.warning(f"JANE API unavailable: {e}")
    authors = []
```

## 验证所有改进

### 前端检查清单
- [ ] 访问 http://localhost:3003/
- [ ] 顶栏是紫色渐变且sticky
- [ ] 页面背景是渐变色
- [ ] 字符计数显示 "X / 4000"
- [ ] Literature Recommendations只有2个标签
- [ ] 在编辑器中右键看到新菜单项
- [ ] 卡片有统一阴影和圆角

### 后端检查
- [ ] 访问 http://localhost:53431/docs
- [ ] 测试 /api/enhance 端点
- [ ] 查看日志确认gpt-4o正在使用

## 前端重启命令

```bash
# 方法1：在当前终端
cd /home/user/rewrite/frontend
npm run dev

# 方法2：强制清除缓存
cd /home/user/rewrite/frontend
npm run dev -- --force

# 方法3：如果端口被占用
cd /home/user/rewrite/frontend
lsof -ti:3003 | xargs kill -9
npm run dev
```

## 后端重启命令

```bash
cd /home/user/rewrite/backend
./start.sh
```
