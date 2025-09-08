# 聊天完成接口测试说明

## 测试脚本

测试脚本位于 `backend/tests/test_chat_completions.py`，包含以下测试用例：

1. 获取模型列表接口测试
2. 非流式聊天完成接口测试
3. 流式聊天完成接口测试
4. 带对话历史的聊天完成接口测试
5. 无效模型请求测试

## 运行测试

### 环境准备

确保已安装测试所需的依赖：

```bash
pip install requests
```

### 启动后端服务

在运行测试之前，需要先启动后端服务：

```bash
# 进入后端目录
cd backend

# 启动服务
python app/main.py
```

### 运行测试脚本

```bash
# 在backend目录下运行测试
python tests/test_chat_completions.py
```

## 测试用例说明

### 1. 获取模型列表接口测试
- 请求路径: `GET /api/models`
- 验证接口是否能正确返回模型列表

### 2. 非流式聊天完成接口测试
- 请求路径: `POST /api/chat/completions`
- 请求参数: 
  - stream: false
  - model: "stellar-byte-llm"
  - messages: 包含用户消息的数组
- 验证接口是否能正确返回完整的聊天回复

### 3. 流式聊天完成接口测试
- 请求路径: `POST /api/chat/completions`
- 请求参数:
  - stream: true
  - model: "stellar-byte-llm"
  - messages: 包含用户消息的数组
- 验证接口是否能正确返回SSE流式数据

### 4. 带对话历史的聊天完成接口测试
- 请求路径: `POST /api/chat/completions`
- 请求参数:
  - stream: false
  - model: "stellar-byte-llm"
  - messages: 包含多轮对话历史的数组
- 验证接口是否能正确处理对话历史

### 5. 无效模型请求测试
- 请求路径: `POST /api/chat/completions`
- 请求参数:
  - stream: false
  - model: "invalid-model"
  - messages: 包含用户消息的数组
- 验证接口是否能正确拒绝无效模型请求并返回400状态码

## 预期结果

所有测试用例都应该通过，显示绿色的"✓"标记。如果有任何测试失败，会显示红色的"✗"标记以及错误信息。

## 故障排除

如果测试失败，请检查：

1. 后端服务是否正常运行
2. 端口是否正确（默认8080）
3. 模型文件是否存在且可加载
4. 网络连接是否正常