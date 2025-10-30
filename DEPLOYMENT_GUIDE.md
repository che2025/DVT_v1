# DVT Report Generator - GCP Cloud Run 部署指南

## 概述
这个指南将帮你将DVT Report Generator部署到Google Cloud Platform (GCP)的Cloud Run服务上。

## 前提条件

### 1. 安装Google Cloud CLI
如果你还没有安装Google Cloud CLI，请按照以下步骤：

**macOS (推荐使用Homebrew):**
```bash
brew install --cask google-cloud-sdk
```

**或者下载安装器:**
访问: https://cloud.google.com/sdk/docs/install

### 2. 登录Google Cloud
```bash
gcloud auth login
```
这会打开浏览器让你登录你的Google账户。

### 3. 验证项目访问权限
```bash
gcloud projects list
```
确保你能看到 `hardware-firmware-dvt` 项目。

## 部署步骤

### 快速部署 (推荐)
我已经为你创建了一个自动化部署脚本，只需运行：

```bash
cd /Users/jianhuache/Downloads/DVT_v1
./deploy.sh
```

这个脚本会自动：
1. 设置正确的GCP项目
2. 启用必要的API服务
3. 构建Docker镜像
4. 部署到Cloud Run
5. 提供访问URL

### 手动部署步骤

如果你想了解每个步骤，也可以手动执行：

1. **设置项目**
```bash
gcloud config set project hardware-firmware-dvt
```

2. **启用API**
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

3. **构建镜像**
```bash
gcloud builds submit --tag gcr.io/hardware-firmware-dvt/dvt-report-generator
```

4. **部署到Cloud Run**
```bash
gcloud run deploy dvt-report-generator \
    --image gcr.io/hardware-firmware-dvt/dvt-report-generator \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 4Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --port 8000
```

## 配置说明

### 资源配置
- **内存**: 4GB (处理大文件和AI任务需要)
- **CPU**: 2个vCPU (确保性能)
- **超时**: 300秒 (报告生成可能需要较长时间)
- **最大实例**: 10个 (控制成本)

### 环境设置
- **端口**: 8000 (FastAPI默认端口)
- **访问权限**: 公开访问 (任何人都可以使用)

## 部署后验证

部署完成后：

1. **测试应用**: 访问提供的URL
2. **上传测试文件**: 尝试生成一个报告
3. **检查日志**: 
```bash
gcloud logs tail /projects/hardware-firmware-dvt/logs/run.googleapis.com%2Frequest
```

## 故障排除

### 常见问题

1. **权限错误**
   - 确保你有项目的部署权限
   - 联系manager确认IAM角色

2. **构建失败**
   - 检查Dockerfile语法
   - 确保所有依赖都在requirements.txt中

3. **内存不足**
   - 增加内存配置到8GB
   - 优化代码减少内存使用

4. **超时错误**
   - 增加超时设置到600秒
   - 优化AI处理速度

## 更新部署

当你需要更新应用时，只需重新运行：
```bash
./deploy.sh
```

## 成本估算

Cloud Run按使用量计费：
- **CPU和内存**: 仅在处理请求时计费
- **请求数**: 每100万请求约$0.40
- **预估月成本**: $10-50 (取决于使用量)

## 安全考虑

当前配置允许公开访问，如果需要：

1. **添加身份验证**:
```bash
gcloud run deploy dvt-report-generator --no-allow-unauthenticated
```

2. **配置自定义域名**
3. **设置VPC连接** (如需要内部网络访问)

## 支持

如遇问题，请检查：
1. GCP控制台中的Cloud Run日志
2. 构建历史和错误信息
3. 项目IAM权限设置
