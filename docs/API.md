# StellarChat API 接口文档（更新版）

## 1. 概述

本文档详细描述了 StellarChat 项目的后端 API 接口规范，包括 HTTP 接口和 WebSocket 接口，供前端开发人员参考使用。API 设计参考了 OpenAI、Anthropic Claude 和 Google Gemini 等主流 LLM API，提供了更好的兼容性和扩展性。

## 2. 基础信息

- **基础路径**: `/api`
- **通信协议**: HTTP/HTTPS, WebSocket
- **数据格式**: JSON
- **字符编码**: UTF-8

## 3. HTTP 接口

### 3.1 健康检查

#### 接口说明
检查后端服务运行状态

#### 请求地址
`GET /api/health`

#### 请求参数
无

#### 响应结果
```json
{
  "status": "healthy"
}
```

#### 响应说明
- status: 服务状态，固定值 "healthy"

### 3.2 获取模型列表

#### 接口说明
获取可用的模型列表

#### 请求地址
`GET /api/models`

#### 请求参数
无

#### 响应结果
```json
{
  "object": "list",
  "data": [
    {
      "id": "stellar-byte-llm",
      "object": "model",
      "created": 1677610602,
      "owned_by": "stellar-byte"
    }
  ]
}
```

### 3.3 聊天完成接口（兼容OpenAI格式）

#### 接口说明
发送聊天消息并获取回复，支持流式和非流式输出

#### 请求地址
`POST /api/chat/completions`

#### 请求头
```
Content-Type: application/json
```

#### 请求参数
```json
{
  "model": "stellar-byte-llm",
  "messages": [
    {
      "role": "user",
      "content": "你好，世界！"
    }
  ],
  "temperature": 0.7,
  "top_p": 1.0,
  "max_tokens": 150,
  "stream": false,
  "stop": null,
  "user": null
}
```

#### 请求参数说明
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| model | string | 是 | 模型名称 |
| messages | array | 是 | 聊天消息历史 |
| temperature | number | 否 | 采样温度，0-2之间，默认0.7 |
| top_p | number | 否 | 核采样，0-1之间，默认1.0 |
| max_tokens | integer | 否 | 最大生成token数 |
| stream | boolean | 否 | 是否启用流式输出，默认false |
| stop | string/array | 否 | 停止词 |
| user | string | 否 | 用户标识符 |

#### 消息格式
消息内容支持两种格式：
1. 简单文本格式：
```json
{
  "role": "user",
  "content": "你好，世界！"
}
```

2. 多模态格式（支持文本）：
```json
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "你好，世界！"
    }
  ]
}
```

#### 响应结果（非流式）
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "stellar-byte-llm",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "你好！很高兴见到你。有什么我可以帮助你的吗？"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

#### 响应结果（流式）
```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"role":"assistant","content":"你"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"好"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"！"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"有"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"什"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"么"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"我"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"可"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"以"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"帮"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"助"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"你"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"的"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"吗"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"？"},"finish_reason":"stop"}]}

data: [DONE]
```

#### 响应参数说明
| 参数名 | 类型 | 说明 |
|--------|------|------|
| id | string | 唯一标识符 |
| object | string | 对象类型 |
| created | integer | 创建时间戳 |
| model | string | 模型名称 |
| choices | array | 选择结果数组 |
| usage | object | 使用量统计 |

#### 错误响应
```json
{
  "error": {
    "type": "invalid_request_error",
    "message": "Invalid request format",
    "param": null,
    "code": "invalid_request"
  }
}
```

## 4. WebSocket 接口

### 4.1 实时聊天（标准化事件流）

#### 接口说明
建立 WebSocket 连接进行实时聊天，支持标准化事件流

#### 连接地址
`WebSocket /api/ws/chat`

#### 连接流程
1. 客户端发起 WebSocket 连接请求
2. 服务端接受连接并生成唯一会话ID
3. 客户端发送聊天消息
4. 服务端按标准化事件流返回回复内容
5. 会话结束时服务端发送结束标记

#### 客户端发送消息
```json
{
  "type": "chat.message",
  "content": "你好，世界！"
}
```

#### 服务端响应消息

##### 会话开始事件
```json
{
  "event": "session_start",
  "data": {
    "session_id": "sess_1234567890"
  }
}
```

##### 内容块开始事件
```json
{
  "event": "content_block_start",
  "data": {
    "type": "text",
    "index": 0
  }
}
```

##### 内容块增量事件
```json
{
  "event": "content_block_delta",
  "data": {
    "index": 0,
    "delta": {
      "type": "text_delta",
      "text": "你"
    }
  }
}
```

##### 内容块结束事件
```json
{
  "event": "content_block_stop",
  "data": {
    "index": 0
  }
}
```

##### 消息增量事件
```json
{
  "event": "message_delta",
  "data": {
    "delta": {
      "finish_reason": "stop"
    },
    "usage": {
      "output_tokens": 12
    }
  }
}
```

##### 消息结束事件
```json
{
  "event": "message_stop",
  "data": {}
}
```

##### 错误消息
```json
{
  "event": "error",
  "data": {
    "type": "server_error",
    "message": "服务器内部错误"
  }
}
```

#### 事件参数说明

##### 会话开始事件
| 参数名 | 类型 | 说明 |
|--------|------|------|
| event | string | 事件类型，固定值 "session_start" |
| data.session_id | string | 会话唯一标识符 |

##### 内容块开始事件
| 参数名 | 类型 | 说明 |
|--------|------|------|
| event | string | 事件类型，固定值 "content_block_start" |
| data.type | string | 内容块类型 |
| data.index | integer | 内容块索引 |

##### 内容块增量事件
| 参数名 | 类型 | 说明 |
|--------|------|------|
| event | string | 事件类型，固定值 "content_block_delta" |
| data.index | integer | 内容块索引 |
| data.delta.type | string | 增量类型 |
| data.delta.text | string | 增量文本内容 |

##### 内容块结束事件
| 参数名 | 类型 | 说明 |
|--------|------|------|
| event | string | 事件类型，固定值 "content_block_stop" |
| data.index | integer | 内容块索引 |

##### 消息增量事件
| 参数名 | 类型 | 说明 |
|--------|------|------|
| event | string | 事件类型，固定值 "message_delta" |
| data.delta.finish_reason | string | 结束原因 |
| data.usage.output_tokens | integer | 输出token数 |

##### 消息结束事件
| 参数名 | 类型 | 说明 |
|--------|------|------|
| event | string | 事件类型，固定值 "message_stop" |

##### 错误消息
| 参数名 | 类型 | 说明 |
|--------|------|------|
| event | string | 事件类型，固定值 "error" |
| data.type | string | 错误类型 |
| data.message | string | 错误信息描述 |

## 5. 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 接口不存在 |
| 500 | 服务器内部错误 |
| 101 | WebSocket 协议升级 |

## 6. 监控接口

### 6.1 Prometheus 监控指标

#### 接口说明
获取 Prometheus 监控指标数据

#### 请求地址
`GET /metrics`

#### 响应结果
Prometheus 格式的监控指标数据

#### 主要指标
- `requests_total`: 总请求数
- `request_latency_seconds`: 请求延迟分布

## 7. 使用示例

### 7.1 HTTP 聊天示例（非流式）

#### 请求
```bash
curl -X POST http://localhost:8080/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "stellar-byte-llm",
    "messages": [
      {"role": "user", "content": "你好"}
    ],
    "temperature": 0.7
  }'
```

#### 响应
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "stellar-byte-llm",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "你好！有什么我可以帮助你的吗？"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

### 7.2 HTTP 聊天示例（流式）

#### 请求
```bash
curl -X POST http://localhost:8080/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "stellar-byte-llm",
    "messages": [
      {"role": "user", "content": "你好"}
    ],
    "stream": true
  }'
```

#### 响应
```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"role":"assistant","content":"你"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"好"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"！"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"有"},"finish_reason":null}]}

data: [DONE]
```

### 7.3 WebSocket 聊天示例 (JavaScript)

```javascript
// 建立 WebSocket 连接
const ws = new WebSocket('ws://localhost:8080/api/ws/chat');

// 连接成功回调
ws.onopen = function() {
  // 发送消息
  ws.send(JSON.stringify({
    "type": "chat.message",
    "content": "你好"
  }));
};

// 接收消息回调
ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  
  switch(data.event) {
    case 'session_start':
      console.log('会话开始:', data.data.session_id);
      break;
    case 'content_block_start':
      console.log('内容块开始:', data.data);
      break;
    case 'content_block_delta':
      console.log('收到内容:', data.data.delta.text);
      break;
    case 'content_block_stop':
      console.log('内容块结束:', data.data);
      break;
    case 'message_delta':
      console.log('消息增量:', data.data);
      break;
    case 'message_stop':
      console.log('回复结束');
      break;
    case 'error':
      console.error('错误:', data.data.message);
      break;
  }
};

// 连接关闭回调
ws.onclose = function() {
  console.log('连接已关闭');
};
```

## 8. 注意事项

1. 所有接口均支持跨域访问
2. WebSocket 连接建立后会为每个会话生成唯一ID用于日志追踪
3. 流式输出接口会逐 token 返回内容，前端需要拼接显示
4. 错误发生时会通过统一异常处理返回标准错误格式
5. 建议在生产环境中使用 HTTPS 协议
6. API 设计兼容 OpenAI 接口格式，便于迁移和集成
7. 消息内容支持多模态格式，当前版本主要支持文本内容