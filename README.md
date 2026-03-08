# 🚀 IdeaForge - 决策导航仪 + 创意孵化器

基于 CopilotKit AG-UI 协议的智能决策和创意验证工具。

## 📋 目录

- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [API 端点](#api-端点)

---

## 功能特性

### 🧭 决策导航仪
帮助用户在面临选择时做出明智决策。

**流程：**
1. 输入决策问题（如"要不要跳槽"）
2. AI 从 6 个维度追问澄清
3. 输入 2-3 个选项
4. 生成对比矩阵
5. 输出决策报告

**决策维度：**
- 💰 经济收益
- 📈 成长空间
- 👥 团队环境
- ⚖️ 工作生活平衡
- 🎯 兴趣匹配度
- ⚠️ 风险评估

### 🚀 创意孵化器
验证创意价值并生成 MVP 执行计划。

**流程：**
1. 输入创意想法
2. AI 引导验证痛点
3. 定义目标用户
4. 生成 MVP 功能列表
5. 输出 4 周执行计划

**输出内容：**
- 痛点验证报告
- 用户画像
- MVP 功能优先级
- 周计划分解

---

## 技术栈

### 后端
| 组件 | 说明 |
|------|------|
| **LangGraph** | Agent 状态机编排 |
| **FastAPI** | Web 服务 |
| **ag-ui-langgraph** | AG-UI 协议适配器 |
| **内存存储** | MVP 会话管理 |

### 前端
| 组件 | 说明 |
|------|------|
| **Next.js 14** | React 框架 |
| **CopilotKit** | AI 对话 SDK |
| **Tailwind CSS** | 样式框架 |

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

后端将在 **http://localhost:8000** 启动

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

前端将在 **http://localhost:3000** 启动

### 3. 访问应用

打开浏览器访问 **http://localhost:3000**

---

## 使用指南

### 🧭 使用决策导航仪

1. 点击"决策导航仪"卡片
2. 输入决策问题，例如：
   ```
   要不要跳槽到新公司？
   ```
3. AI 会从多个维度追问
4. 输入你的选项：
   ```
   - 选项 A: 留在当前公司
   - 选项 B: 接受新 Offer
   ```
5. 查看对比矩阵和决策报告
6. 复制报告保存

### 🚀 使用创意孵化器

1. 点击"创意孵化器"卡片
2. 输入创意想法，例如：
   ```
   做一个 AI 写作助手
   ```
3. 回答 AI 的验证问题：
   - 痛点是什么？
   - 目标用户是谁？
4. 查看 MVP 功能列表
5. 获取 4 周执行计划
6. 复制计划开始执行

---

## API 端点

### 后端 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/decision` | POST | 决策导航仪 AG-UI 端点 |
| `/idea` | POST | 创意孵化器 AG-UI 端点 |
| `/health` | GET | 健康检查 |
| `/api/history` | GET | 获取历史记录 |
| `/api/history` | DELETE | 清空历史记录 |

### 前端 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/copilotkit` | POST | 代理到后端 AG-UI 端点 |

---

## 项目结构

```
copilotkit-langgraph/
├── backend/
│   ├── main.py          # LangGraph + FastAPI
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── app/
    │   ├── api/
    │   │   └── copilotkit/
    │   │       └── route.ts
    │   ├── page.tsx     # 主页面（模式选择）
    │   └── layout.tsx
    └── package.json
```

---

## MVP 状态

### 已实现 ✅
- [x] 决策导航仪流程
- [x] 创意孵化器流程
- [x] 模式选择 UI
- [x] 对话式交互
- [x] 内存存储历史记录
- [x] 报告生成

### 待实现 🔄
- [ ] 持久化存储（数据库）
- [ ] 报告导出（PDF/图片）
- [ ] 分享功能
- [ ] 真实 LLM 集成
- [ ] 用户认证

---

## 常见问题

### Q: 回复是模拟的？
A: MVP 版本使用规则引擎演示流程。接入真实 LLM 只需在节点中调用 LangChain 的 ChatModel。

### Q: 如何接入真实 LLM？
A: 在 `backend/main.py` 的节点函数中：
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
response = llm.invoke(messages)
```

### Q: 历史记录存在哪？
A: MVP 存储在内存中，重启后清空。生产环境需接入数据库。

---

## 参考资源

- [CopilotKit 文档](https://docs.copilotkit.ai)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [AG-UI 协议](https://github.com/ag-ui-protocol/ag-ui)

---

Made with ❤️ by MotherFaker Studio
