# StellarChat 数据库设计方案

## 1. 概述

本方案为StellarChat项目设计后端聊天记录存储数据库，支持会话管理、消息存储和会话历史浏览功能。

## 2. 存储方案选择

### 2.1 选择SQLite的原因

1. **轻量级**: SQLite是一个轻量级的嵌入式数据库，无需单独的服务器进程
2. **易于部署**: 无需复杂的数据库服务器配置，适合当前项目的规模
3. **兼容性**: 与Python的SQLAlchemy ORM兼容良好
4. **开发友好**: 便于开发和测试环境的快速搭建
5. **成本效益**: 无需额外的数据库服务器资源

### 2.2 未来扩展考虑

如果项目需要扩展到多实例部署或高并发场景，可以考虑迁移到PostgreSQL，当前设计保持了良好的可扩展性。

## 3. 数据库表结构设计

### 3.1 会话表 (sessions)

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | TEXT | PRIMARY KEY | 会话唯一标识符 (UUID) |
| title | TEXT | NOT NULL | 会话标题 |
| created_at | DATETIME | NOT NULL DEFAULT CURRENT_TIMESTAMP | 会话创建时间 |
| updated_at | DATETIME | NOT NULL DEFAULT CURRENT_TIMESTAMP | 会话最后更新时间 |
| is_active | BOOLEAN | NOT NULL DEFAULT TRUE | 会话是否活跃 |

### 3.2 消息表 (messages)

| 字段名 | 类型 | 约束 | 描述 |
|--------|------|------|------|
| id | TEXT | PRIMARY KEY | 消息唯一标识符 (UUID) |
| session_id | TEXT | NOT NULL, FOREIGN KEY | 所属会话ID |
| role | TEXT | NOT NULL | 消息角色 (user/assistant/system) |
| content | TEXT | NOT NULL | 消息内容 |
| created_at | DATETIME | NOT NULL DEFAULT CURRENT_TIMESTAMP | 消息创建时间 |
| tokens | INTEGER | DEFAULT 0 | 消息token数量 |
| metadata | TEXT |  | 额外元数据 (JSON格式) |

### 3.3 索引设计

1. **sessions表索引**:
   - 主键索引: id
   - 时间索引: created_at (用于按时间排序)

2. **messages表索引**:
   - 主键索引: id
   - 外键索引: session_id
   - 时间索引: created_at (用于按时间排序)
   - 复合索引: session_id + created_at (优化会话内消息查询)

## 4. 数据模型关系

```
+-----------+          +-----------+
| sessions  |<---------| messages  |
+-----------+    1..*  +-----------+
| id (PK)   |          | id (PK)   |
| title     |          | session_id|
| created_at|          | role      |
| updated_at|          | content   |
| is_active |          | created_at|
+-----------+          | tokens    |
                       | metadata  |
                       +-----------+
```

## 5. API接口设计

### 5.1 会话管理接口

1. **创建会话**
   - POST /api/sessions
   - 请求: { "title": "新会话标题" }
   - 响应: 会话对象

2. **获取会话列表**
   - GET /api/sessions
   - 参数: page, size, active_only
   - 响应: 会话列表

3. **获取会话详情**
   - GET /api/sessions/{session_id}
   - 响应: 会话对象及消息历史

4. **更新会话**
   - PUT /api/sessions/{session_id}
   - 请求: { "title": "更新后的标题" }
   - 响应: 更新后的会话对象

5. **删除会话**
   - DELETE /api/sessions/{session_id}
   - 响应: 成功/失败状态

### 5.2 消息管理接口

1. **添加消息**
   - POST /api/sessions/{session_id}/messages
   - 请求: 消息对象
   - 响应: 添加的消息

2. **获取会话消息**
   - GET /api/sessions/{session_id}/messages
   - 参数: page, size
   - 响应: 消息列表

## 6. 数据库初始化脚本

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tokens INTEGER DEFAULT 0,
    metadata TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions (created_at);
CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages (session_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages (created_at);
CREATE INDEX IF NOT EXISTS idx_messages_session_created ON messages (session_id, created_at);
```

## 7. 数据库连接配置

在 `backend/app/config.py` 中添加数据库配置:

```python
# 数据库配置
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./chat_history.db")
```

## 8. 数据库访问层设计

使用SQLAlchemy ORM进行数据库操作，创建以下模型类:

1. SessionModel - 会话模型
2. MessageModel - 消息模型
3. DatabaseService - 数据库服务类，提供CRUD操作

## 9. 性能优化建议

1. **分页查询**: 对于大量消息的会话，使用分页查询避免内存溢出
2. **索引优化**: 根据查询模式创建合适的索引
3. **连接池**: 使用连接池管理数据库连接
4. **缓存**: 对于频繁访问的会话数据，可考虑使用缓存机制

## 10. 数据备份与恢复

1. **定期备份**: 设置定时任务定期备份SQLite数据库文件
2. **恢复机制**: 提供数据库恢复接口
3. **数据导出**: 支持会话数据导出功能