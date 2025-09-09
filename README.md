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

---

<details>
<summary>2025.9.9</summary>

### DONE
**迁移前端项目从React到Vue并实现LLM聊天功能**
1. 重构前端架构，从React迁移到Vue 3，并实现完整的LLM聊天功能：
2. 使用Vue 3 + Pinia + Element Plus重构前端架构
3. 实现多会话管理功能，支持创建、编辑和删除对话
4. 添加Markdown渲染和代码高亮支持
5. 实现流式响应和消息处理
6. 添加设置面板，支持模型选择和参数配置
7. 优化UI设计，支持深色/浅色主题切换
8. 添加文件上传和预览功能
9. 实现本地数据持久化存储

### TODO
1. 代码复用和组件化
  - 优化点: 多个组件中存在相似的文件预览逻辑和样式。
  - 建议: 创建一个通用的文件预览组件，统一处理图片和文件的显示逻辑，减少重复代码。
2. 性能优化
  - 优化点: 在ChatMessage.vue中，使用了MutationObserver来监听DOM变化，这可能影响性能。
  - 建议: 考虑使用Vue的响应式系统来替代MutationObserver，或者使用v-show/v-if指令来控制元素的显示，减少不必要
  的DOM操作。
3. 代码可维护性
  - 优化点: 在ChatMessage.vue中，处理代码块主题切换的逻辑较为复杂。
  - 建议: 将代码块主题切换的逻辑封装成独立的函数或组件，提高代码的可读性和可维护性。
4. 用户体验优化
  - 优化点: 在ChatInput.vue中，文件上传功能没有明确的文件类型限制提示。
  - 建议: 在文件上传组件中添加明确的文件类型和大小限制提示，改善用户体验。
5. 样式优化
  - 优化点: 在多个组件中，存在重复的样式代码，如按钮样式、布局样式等。
  - 建议: 将通用的样式提取到SCSS mixins或CSS变量中，统一管理样式，减少重复代码。
6. 代码规范
  - 优化点: 在ChatMessage.vue中，存在一些未使用的注释代码。
  - 建议: 清理未使用的注释代码，保持代码整洁。
7. 主题切换优化
  - 优化点: 在markdown.js中，代码块主题切换依赖于图片资源。
  - 建议: 考虑使用CSS变量或类名切换来实现主题切换，减少对图片资源的依赖，提高性能。
8. 状态管理优化
  - 优化点: 在chat.js中，对话ID使用时间戳生成，可能存在重复风险。
  - 建议: 使用更可靠的ID生成方式，如UUID，确保ID的唯一性。
9. 为了提高与OpenAI API的兼容性，可以考虑以下改进：
  - 扩展模型支持：允许使用更通用的模型名称
  - 增加参数支持：添加OpenAI支持但本地缺失的参数
  - 完善文档：提供与OpenAI API兼容性对照表
  - 错误处理：保持错误响应格式与OpenAI一致

</details>