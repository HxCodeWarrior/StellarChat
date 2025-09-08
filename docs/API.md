# API接口文档

## 1. 概述

本文档详细描述了StellarByte LLM Chat Backend的所有API接口，包括端点、参数、请求/响应格式和示例。

## 2. 基础配置

- **基础URL**: `http://localhost:8080/api` (默认配置)
- **文档**: 
  - Swagger UI: `http://localhost:8080/api/docs`
  - ReDoc: `http://localhost:8080/api/redoc`

## 3. API端点

### 3.1 健康检查

#### GET /health
检查应用健康状态。

**响应:**
```json
{
  "status": "healthy"
}
```

### 3.2 模型管理

#### GET /models
获取可用模型列表。

**响应:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "stellar-byte-llm",
      "object": "model",
      "created": 1700000000,
      "owned_by": "stellar-byte"
    }
  ]
}
```

### 3.3 聊天完成 (REST API)

#### POST /chat/completions
创建聊天完成。

**参数:**
- `session_id` (query, optional): 会话ID，用于保存聊天历史

**请求体:**
```json
{
  "model": "stellar-byte-llm",
  "messages": [
    {
      "role": "user",
      "content": "你好"
    }
  ],
  "temperature": 0.7,
  "top_p": 1.0,
  "max_tokens": 100,
  "stream": false,
  "stop": null,
  "user": null
}
```

**响应 (非流式):**
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "stellar-byte-llm",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！有什么我可以帮助你的吗？"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

**流式响应:**
当`stream=true`时，返回SSE流:
```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1700000000,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1700000000,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"你"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1700000000,"model":"stellar-byte-llm","choices":[{"index":0,"delta":{"content":"好"},"finish_reason":null}]}

data: [DONE]
```

### 3.4 WebSocket聊天

#### WebSocket /ws/chat
WebSocket聊天接口。

**参数:**
- `session_id` (query, optional): 会话ID，用于保存聊天历史

**客户端发送:**
```json
{
  "type": "chat.message",
  "content": "你好"
}
```

**服务器事件:**

1. **会话开始**
```json
{
  "event": "session_start",
  "data": {
    "session_id": "123e4567-e89b-12d3-a456-426614174000"
  }
}
```

2. **内容块开始**
```json
{
  "event": "content_block_start",
  "data": {
    "type": "text",
    "index": 0
  }
}
```

3. **内容块增量**
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

4. **内容块结束**
```json
{
  "event": "content_block_stop",
  "data": {
    "index": 0
  }
}
```

5. **消息增量**
```json
{
  "event": "message_delta",
  "data": {
    "delta": {
      "finish_reason": "stop"
    },
    "usage": {
      "output_tokens": 10
    }
  }
}
```

6. **消息结束**
```json
{
  "event": "message_stop",
  "data": {}
}
```

7. **错误事件**
```json
{
  "event": "error",
  "data": {
    "type": "server_error",
    "message": "处理消息时出错"
  }
}
```

### 3.5 会话管理

#### POST /sessions
创建新会话。

**请求体:**
```json
{
  "title": "新会话"
}
```

**响应:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "新会话",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00",
  "is_active": true
}
```

#### GET /sessions
获取会话列表。

**参数:**
- `skip` (query, optional): 跳过的记录数，默认0
- `limit` (query, optional): 返回记录数，默认100
- `active_only` (query, optional): 仅返回活跃会话，默认true

**响应:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "新会话",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00",
    "is_active": true
  }
]
```

#### GET /sessions/{session_id}
获取会话详情。

**响应:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "新会话",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00",
  "is_active": true
}
```

#### PUT /sessions/{session_id}
更新会话。

**请求体:**
```json
{
  "title": "更新后的会话"
}
```

**响应:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "更新后的会话",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:01:00",
  "is_active": true
}
```

#### DELETE /sessions/{session_id}
删除会话。

**响应:**
```json
{
  "message": "会话删除成功"
}
```

#### POST /sessions/{session_id}/messages
添加消息到会话。

**请求体:**
```json
{
  "role": "user",
  "content": "你好",
  "tokens": 2,
  "metadata_info": {}
}
```

**响应:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174001",
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "role": "user",
  "content": "你好",
  "created_at": "2023-01-01T00:00:00",
  "tokens": 2,
  "metadata_info": {}
}
```

#### GET /sessions/{session_id}/messages
获取会话消息。

**参数:**
- `skip` (query, optional): 跳过的记录数，默认0
- `limit` (query, optional): 返回记录数，默认100

**响应:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174001",
    "session_id": "123e4567-e89b-12d3-a456-426614174000",
    "role": "user",
    "content": "你好",
    "created_at": "2023-01-01T00:00:00",
    "tokens": 2,
    "metadata_info": {}
  }
]
```

#### GET /sessions/{session_id}/history
获取会话聊天历史（用于模型推理）。

**响应:**
```json
[
  {
    "role": "user",
    "content": "你好"
  }
]
```