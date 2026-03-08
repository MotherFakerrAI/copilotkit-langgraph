# 🚀 MotherFaker AI Studio

基于 CopilotKit AG-UI 协议的 AI 应用矩阵。

## 📋 项目矩阵

| 项目 | 状态 | 说明 |
|------|------|------|
| **📚 LearnLoop** | ✅ MVP | 监督式学习伴侣 |
| **🧭 决策导航仪** | ✅ MVP | 决策分析工具 |
| **🚀 创意孵化器** | ✅ MVP | 创意验证工具 |

---

## 📚 LearnLoop - 学习伴侣

**监督式学习，让坚持变得简单**

### 核心功能
- 🎯 **目标设定** - 输入学习目标（如"3 个月学会 Python"）
- 📋 **路径规划** - AI 拆解成周任务 + 每日待办
- ✅ **每日打卡** - 报告进度，AI 记录
- 📊 **进度可视化** - 学习日历 + 完成度条

### 使用流程
1. 选择"学习伴侣"模式
2. 输入目标："3 个月学会 Python"
3. AI 生成学习路径
4. 每日打卡："完成今日任务"
5. 查看进度报告

### LangGraph 状态
```python
LearnState:
  - goal: str          # 学习目标
  - subject: str       # 学科
  - deadline: str      # 截止日期
  - plan: dict         # 周计划
  - progress: dict     # 打卡记录
  - streak: int        # 连续天数
```

---

## 🧭 决策导航仪

**明智决策，从多维度分析开始**

### 核心功能
- 📝 输入决策问题
- 🔍 6 维度分析（经济/成长/团队/平衡/兴趣/风险）
- 📊 对比矩阵生成
- 📋 决策报告输出

### 使用流程
1. 选择"决策导航仪"模式
2. 输入问题："要不要跳槽？"
3. 回答 AI 追问
4. 输入 2-3 个选项
5. 获取对比矩阵和报告

---

## 🚀 创意孵化器

**从想法到 MVP，只需 4 周**

### 核心功能
- 💡 创意想法输入
- 🔍 痛点验证
- 👥 目标用户定义
- 📋 MVP 功能列表
- 📅 4 周执行计划

### 使用流程
1. 选择"创意孵化器"模式
2. 输入创意："AI 写作工具"
3. 回答痛点和用户问题
4. 获取 MVP 功能和计划

---

## 🛠️ 技术栈

### 后端
| 组件 | 说明 |
|------|------|
| **LangGraph** | Agent 状态机编排 |
| **FastAPI** | Web 服务 |
| **ag-ui-langgraph** | AG-UI 协议适配器 |

### 前端
| 组件 | 说明 |
|------|------|
| **Next.js 14** | React 框架 |
| **CopilotKit** | AI 对话 SDK |
| **Tailwind CSS** | 样式框架 |

---

## 🚀 快速开始

### 1. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

后端将在 **http://localhost:8000** 启动

可用端点：
- `/learn` - 学习伴侣
- `/decision` - 决策导航仪
- `/idea` - 创意孵化器
- `/health` - 健康检查

### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 **http://localhost:3000** 启动

### 3. 访问应用

打开浏览器访问 **http://localhost:3000**

选择模式开始使用！

---

## 📁 项目结构

```
copilotkit-langgraph/
├── backend/
│   ├── main.py          # LangGraph + 3 个 Agent
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── app/
    │   ├── api/
    │   │   └── copilotkit/
    │   │       └── route.ts
    │   ├── page.tsx     # 3 模式选择
    │   └── layout.tsx
    └── package.json
```

---

## 🎯 MVP 状态

### LearnLoop (学习伴侣)
- [x] 目标设定
- [x] 路径规划
- [x] 每日打卡
- [x] 进度可视化
- [ ] 弱点分析（P1）
- [ ] 成就系统（P1）

### 决策导航仪
- [x] 问题澄清
- [x] 选项收集
- [x] 对比矩阵
- [x] 决策报告

### 创意孵化器
- [x] 痛点验证
- [x] 用户定义
- [x] MVP 功能
- [x] 执行计划

---

## 📖 API 端点

### 后端
| 端点 | 方法 | 说明 |
|------|------|------|
| `/learn` | POST | 学习伴侣 AG-UI |
| `/decision` | POST | 决策导航仪 AG-UI |
| `/idea` | POST | 创意孵化器 AG-UI |
| `/health` | GET | 健康检查 |
| `/api/history` | GET | 历史记录 |
| `/api/progress` | GET | 学习进度 |

### 前端
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/copilotkit` | POST | 代理到后端 |

---

## 🔧 配置

### 后端 (.env)
```env
OPENAI_API_KEY=sk-your-key-here
```

### 前端 (.env.local)
```env
BACKEND_URL=http://localhost:8000
```

---

## 📝 待办事项

### P0 (核心功能)
- [x] 3 个 Agent 流程跑通
- [x] 前端模式选择
- [x] 内存存储
- [ ] 真实 LLM 集成

### P1 (增强功能)
- [ ] 持久化存储（数据库）
- [ ] 用户认证
- [ ] 报告导出
- [ ] 分享功能

---

## 🙋 常见问题

### Q: 如何切换模式？
A: 点击"返回"按钮回到模式选择页面。

### Q: 学习进度会保存吗？
A: MVP 版本存储在内存中，重启后清空。生产环境需接入数据库。

### Q: 如何接入真实 LLM？
A: 在节点函数中调用 LangChain 的 ChatModel：
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI()
response = llm.invoke(messages)
```

---

## 📚 参考资源

- [CopilotKit 文档](https://docs.copilotkit.ai)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [AG-UI 协议](https://github.com/ag-ui-protocol/ag-ui)

---

Made with ❤️ by MotherFaker Studio
