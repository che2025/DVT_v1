# DVT项目代码修改和部署工作流程

## 📝 如何修改代码并重新部署

### 方式一：本地开发测试
```bash
# 1. 激活虚拟环境
source venv_1/bin/activate

# 2. 本地运行测试
export GOOGLE_CLOUD_PROJECT=dp-experimental
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=true
python main.py

# 3. 访问 http://localhost:8000 测试功能
```

### 方式二：快速云端部署
```bash
# 1. 修改代码后，提交更改
git add .
git commit -m "描述你的修改内容"

# 2. 重新部署到云端
./deploy.sh

# 3. 访问生成的URL测试
```

### 方式三：分支开发
```bash
# 1. 创建新分支进行开发
git checkout -b feature/你的功能名称

# 2. 修改代码
# ... 编辑你的文件 ...

# 3. 提交更改
git add .
git commit -m "实现新功能: 功能描述"

# 4. 测试部署（可选）
./deploy.sh

# 5. 合并到主分支
git checkout main
git merge feature/你的功能名称
git push origin main
```

## 🎯 常见修改场景

### 修改前端界面
- 文件位置: `frontend/index.html`
- 修改后需要重新部署到云端

### 修改报告生成逻辑
- 文件位置: `report_generator_agent/report_generator.py`
- 可以先本地测试，再部署

### 修改AI提示词
- 文件位置: `report_generator_agent/ai_agents.py`
- 修改后建议立即测试效果

### 添加新的依赖库
- 文件位置: `requirements.txt`
- 添加后需要重新部署

## 🚀 部署目标切换

### 当前配置（测试环境）
- 项目: dp-experimental
- URL: https://dvt-report-generator-test-avrac5dmoa-uc.a.run.app

### 切换到生产环境
1. 获得hardware-firmware-dvt项目权限
2. 修改deploy.sh中的PROJECT_ID:
```bash
# 将这行
PROJECT_ID="dp-experimental"
# 改为
PROJECT_ID="hardware-firmware-dvt"
```
3. 运行 ./deploy.sh

## 💡 开发小贴士

### 快速测试流程
1. **小修改**: 直接修改代码 → 运行 `./deploy.sh`
2. **大修改**: 先本地测试 → 确认无误后部署
3. **实验性功能**: 创建分支 → 测试 → 合并

### 回滚到之前版本
```bash
# 查看提交历史
git log --oneline

# 回滚到特定提交
git reset --hard <commit-hash>

# 重新部署
./deploy.sh
```

### 查看云端日志
```bash
# 实时查看应用日志
/Users/jianhuache/Downloads/DVT_v1/deploy_che_1/google-cloud-sdk/bin/gcloud logs tail /projects/dp-experimental/logs/run.googleapis.com%2Frequest
```

## 🔧 故障排除

### 部署失败
- 检查网络连接
- 验证GCP权限
- 查看构建日志

### 功能异常
- 检查云端日志
- 本地重现问题
- 回滚到上一个工作版本

### 权限问题
- 重新运行认证: `gcloud auth application-default login`
- 确认项目权限
