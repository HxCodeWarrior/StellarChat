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