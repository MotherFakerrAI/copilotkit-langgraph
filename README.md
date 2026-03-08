# 🤖 CopilotKit + LangGraph 前后端框架

基于 AG-UI 协议的完整工程化项目，连接 CopilotKit 前端与 LangGraph 后端。

## 📋 目录

- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [开发指南](#开发指南)

---

## 技术栈

### 后端 (Python)
| 组件 | 说明 |
|------|------|
| **LangGraph** | Agent 编排框架 |
| **FastAPI** | Web 服务 |
| **ag-ui-langgraph** | AG-UI 协议适配器 |
| **langchain-core** | LLM 抽象层 |

### 前端 (Next.js + React)
| 组件 | 说明 |
|------|------|
| **Next.js 14** | React 框架 (App Router) |
| **@copilotkit/react-core** | CopilotKit 核心 SDK |
| **@copilotkit/react-ui** | 聊天 UI 组件 |
| **@copilotkit/runtime** | 运行时适配器 |

---

## 项目结构

```
copilotkit-langgraph/
├── backend/              # Python 后端
│   ├── main.py          # LangGraph + FastAPI + AG-UI
│   ├── requirements.txt # Python 依赖
│   └── .env.example     # 环境配置模板
│
└── frontend/            # Next.js 前端
    ├── app/
    │   ├── api/
    │   │   └── copilotkit/
    │   │       └── route.ts  # API Route（连接后端）
    │   ├── page.tsx     # 主页面（聊天界面）
    │   ├── layout.tsx   # 根布局
    │   └── globals.css  # 全局样式
    ├── package.json     # Node.js 依赖
    └── .env.local.example # 环境配置模板
```

---

## 快速开始

### 1. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境
cp .env.example .env

# 启动服务
python main.py
```

后端将在 http://localhost:8000 启动

### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 配置环境
cp .env.local.example .env.local

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:3000 启动

### 3. 验证

1. 打开浏览器访问 http://localhost:3000
2. 在聊天界面输入消息
3. 查看 AI 回复

---

## 配置说明

### 后端配置 (.env)

```env
# OpenAI API Key（可选，用于实际 LLM 调用）
OPENAI_API_KEY=sk-your-api-key-here

# 服务配置
HOST=0.0.0.0
PORT=8000
```

### 前端配置 (.env.local)

```env
# 后端 AG-UI 端点 URL
BACKEND_URL=http://localhost:8000

# Next.js 配置
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## 开发指南

### 添加新 Agent 节点

在 `backend/main.py` 中：

```python
def new_node(state: AgentState) -> AgentState:
    """新节点逻辑"""
    messages = state["messages"]
    # 处理逻辑
    return {"messages": [AIMessage(content="回复")]}

# 添加到图
graph.add_node("new_node", new_node)
graph.add_edge("chat", "new_node")
```

### 添加工具调用

```python
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """搜索网络"""
    return f"搜索结果：{query}"

# 在节点中使用
def chat_with_tools(state: AgentState):
    # 调用工具
    result = search_web.invoke({"query": "xxx"})
```

### 自定义前端 UI

编辑 `frontend/app/page.tsx`：

```tsx
<CopilotChat
  className="h-[600px]"
  placeholder="自定义提示文字..."
  labels={{
    initial: "自定义欢迎消息",
  }}
/>
```

---

## API 端点

### 后端

| 端点 | 说明 |
|------|------|
| `POST /` | AG-UI 消息端点 |
| `GET /health` | 健康检查 |

### 前端

| 端点 | 说明 |
|------|------|
| `POST /api/copilotkit` | 代理到后端 AG-UI 端点 |

---

## 常见问题

### Q: 消息无法发送？
A: 检查后端是否启动，确认 `BACKEND_URL` 配置正确。

### Q: 如何连接真实 LLM？
A: 在 `backend/main.py` 的 `chat_node` 中调用 LangChain 的 ChatModel。

### Q: 如何部署？
A: 
- 后端：Docker + 任意云平台
- 前端：Vercel / Netlify

---

## 参考资源

- [CopilotKit 文档](https://docs.copilotkit.ai)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [AG-UI 协议](https://github.com/ag-ui-protocol/ag-ui)
- [FastAPI 文档](https://fastapi.tiangolo.com/)

---

Made with ❤️ by MotherFaker Studio
