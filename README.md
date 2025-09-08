# StellarChat
StellarChat is a modern web chat app built with the StellarByte LLM model. It provides real-time interaction, streaming responses, and themes for high usability. Combining React and FastAPI, it delivers fast and responsive user experiences.

# Object-Structure
```
StellarChat/
│
├── backend/                   # 后端服务（加载 LLM 权重，提供 API 接口）
│   ├── app/
│   │   ├── main.py            # FastAPI/Flask 入口
│   │   ├── routers/
│   │   │   ├── chat_ws.py     # 聊天接口（WebSocket）
│   │   │   ├── chat.py        # 聊天接口（LLM 推理）
│   │   │   ├── health.py      # 健康检查接口
│   │   ├── models/
│   │   │   ├── inference.py   # 调用本地 LLM 权重推理逻辑
│   │   │   ├── tokenizer.py   # 分词与预处理
│   │   ├── config.py          # 配置文件（模型路径、端口等）
│   │   └── utils.py           # 工具函数（日志、缓存等）
│   ├── requirements.txt       # 后端依赖
│   ├── Dockerfile             # 后端容器化部署文件
│   └── run.sh                 # 启动脚本
│
├── frontend/                  # 前端（精美聊天网页）
│   ├── public/
│   │   └── index.html         # 页面模板
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx # 聊天窗口
│   │   │   ├── Message.tsx    # 单条消息气泡
│   │   │   ├── InputBox.tsx   # 输入框组件
│   │   │   ├── Sidebar.tsx    # 左侧历史会话/设置
│   │   ├── pages/
│   │   │   ├── Home.tsx       # 主页面
│   │   ├── hooks/
│   │   │   ├── useChat.ts     # 管理聊天逻辑的 Hook
│   │   ├── services/
│   │   │   ├── api.ts         # 封装 axios/fetch 调用后端 API
│   │   ├── styles/
│   │   │   ├── global.css     # 全局样式
│   │   ├── App.tsx            # React 入口
│   │   └── main.tsx           # 前端入口
│   ├── package.json           # 前端依赖
│   ├── vite.config.ts         # Vite 配置
│   └── tailwind.config.js     # Tailwind 配置
│
├── docs/                      # 项目文档
│   ├── README.md
│   └── api_spec.md            # API 设计规范
│
├── docker-compose.yml         # 前后端一键部署
└── README.md                  # 总体说明
```

## PLAN

<details>
<summary>2025.8.23</summary>

### DONE
1. 初始化项目前端
2. 初始化项目后端

### TODO
1. 完善基础后端初始化
2. 设计后端优化升级方案

</details>

---

<details>
<summary>2025.8.24</summary>

### DONE
1. backend/app/main.py 添加Prometheus监控指标和全局异常处理
- 引入Prometheus客户端库添加请求计数和延迟监控指标
- 添加全局异常处理中间件返回统一错误格式
- 挂载/metrics端点用于Prometheus采集指标数据
2. backend/app/models/interfence.py 重构模型加载逻辑并支持异步流式生成
- 实现单例模式避免重复加载模型
- 使用AutoTokenizer替代自定义Tokenizer
- 根据设备可用性自动选择精度和设备映射
- 将stream_chat改为异步方法
3. backend/app/models/tokenizer.py 当分词器没有设置pad_token时，使用eos_token作为替代，确保模型能够正常处理填充操作
4. backend/app/routers/chat_ws.py 添加会话ID支持并改进消息处理
- 为每个WebSocket连接生成唯一会话ID便于追踪
- 使用stream_chat方法直接处理聊天流
- 改进错误处理和消息格式，使用JSON格式发送事件和错误

### TODO
1. 添加上下文管理器
- 记忆功能
- 支持多轮对话

</details>