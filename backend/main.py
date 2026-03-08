"""
IdeaForge - 决策导航仪 + 创意孵化器
基于 CopilotKit AG-UI 协议

功能：
1. 决策导航仪 - 帮助用户做出明智决策
2. 创意孵化器 - 验证创意并生成 MVP 计划
"""

from typing import Annotated, TypedDict, List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ag_ui_langgraph import AGUIBridge
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
import json
from datetime import datetime

# ==================== 环境配置 ====================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-demo-key")

# ==================== FastAPI 应用 ====================
app = FastAPI(title="IdeaForge Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 内存存储（MVP 用）====================
memory_store = {
    "sessions": {},  # 会话存储
    "history": []    # 历史记录
}

# ==================== 决策导航仪 State ====================
class DecisionState(TypedDict):
    """决策导航仪状态"""
    messages: Annotated[List, add_messages]
    problem: str              # 决策问题
    dimensions: List[str]     # 决策维度
    options: List[str]        # 选项列表
    matrix: dict              # 对比矩阵
    report: str               # 决策报告
    step: str                 # 当前步骤

# ==================== 创意孵化器 State ====================
class IdeaState(TypedDict):
    """创意孵化器状态"""
    messages: Annotated[List, add_messages]
    idea: str                 # 创意想法
    pain_point: str           # 痛点描述
    target_users: str         # 目标用户
    mvp_features: List[str]   # MVP 功能
    plan: dict                # 执行计划
    step: str                 # 当前步骤

# ==================== 决策导航仪节点 ====================
def decision_clarify_node(state: DecisionState) -> DecisionState:
    """步骤 1: 澄清决策问题"""
    messages = state["messages"]
    last_message = messages[-1] if messages else None
    
    if not last_message or not isinstance(last_message, HumanMessage):
        return state
    
    problem = last_message.content.strip()
    
    # 预设决策维度
    dimensions = [
        "💰 经济收益（薪资/成本）",
        "📈 成长空间（技能/职业发展）",
        "👥 团队环境（同事/领导）",
        "⚖️ 工作生活平衡",
        "🎯 个人兴趣匹配度",
        "⚠️ 风险评估"
    ]
    
    response = f"""📋 **决策问题：{problem}**

我将从以下维度帮你分析：

{' | '.join(dimensions[:3])}
{' | '.join(dimensions[3:])}

请告诉我你有哪几个选项？（2-3 个）
例如：
- 选项 A: 留在当前公司
- 选项 B: 跳槽到新公司
"""
    
    return {
        **state,
        "problem": problem,
        "dimensions": dimensions,
        "step": "collecting_options"
    }

def decision_options_node(state: DecisionState) -> DecisionState:
    """步骤 2: 收集选项"""
    messages = state["messages"]
    
    # 解析用户输入的选项
    last_message = messages[-1].content if messages else ""
    
    # 简单解析选项（实际项目中用 LLM 解析）
    options = []
    for line in last_message.split('\n'):
        line = line.strip()
        if line and any(marker in line for marker in ['选项', 'Option', '-', '•', '1.', '2.', '3.']):
            # 清理文本
            option = line.lstrip('-•').strip()
            for marker in ['选项', 'Option', '1.', '2.', '3.']:
                option = option.replace(marker, '').strip()
            if option and len(option) > 2:
                options.append(option)
    
    # 如果选项不足，使用默认
    if len(options) < 2:
        options = ["选项 A", "选项 B"]
    
    response = f"""✅ 收到 {len(options)} 个选项：
{chr(10).join(f'• {opt}' for opt in options)}

正在生成对比矩阵，请稍候...
"""
    
    return {
        **state,
        "options": options,
        "step": "generating_matrix"
    }

def decision_matrix_node(state: DecisionState) -> DecisionState:
    """步骤 3: 生成对比矩阵"""
    options = state.get("options", [])
    dimensions = state.get("dimensions", [])
    
    # 生成对比矩阵（MVP 用模拟数据）
    matrix = {
        "headers": ["维度"] + options,
        "rows": []
    }
    
    for dim in dimensions:
        row = [dim]
        for opt in options:
            # 模拟评分（实际项目中用 LLM 生成）
            import random
            score = random.choice(["✅ 优势", "⚠️ 中性", "❌ 劣势"])
            row.append(score)
        matrix["rows"].append(row)
    
    response = f"""📊 **对比矩阵**

| {' | '.join(matrix['headers'])} |
|{'|'.join(['---'] * len(matrix['headers']))}|
"""
    for row in matrix["rows"]:
        response += f"| {' | '.join(row)} |\n"
    
    response += "\n正在生成决策报告..."
    
    return {
        **state,
        "matrix": matrix,
        "step": "generating_report"
    }

def decision_report_node(state: DecisionState) -> DecisionState:
    """步骤 4: 生成决策报告"""
    problem = state.get("problem", "")
    options = state.get("options", [])
    dimensions = state.get("dimensions", [])
    
    # 生成决策报告
    report = f"""# 📋 决策报告

## 决策问题
{problem}

## 对比维度
{chr(10).join(f'- {dim}' for dim in dimensions)}

## 选项分析
{chr(10).join(f'### {opt}' for opt in options)}

## 建议
基于以上分析，建议综合考虑各维度权重，选择最符合你长期目标的选项。

---
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
*IdeaForge 决策导航仪*
"""
    
    # 保存到历史记录
    history_item = {
        "id": f"decision_{len(memory_store['history']) + 1}",
        "type": "decision",
        "problem": problem,
        "created_at": datetime.now().isoformat(),
        "report": report
    }
    memory_store["history"].append(history_item)
    
    response = f"""✅ **决策报告已生成！**

{report}

---
💡 你可以：
1. 复制报告保存
2. 开始新的决策
3. 切换到"创意孵化器"
"""
    
    return {
        **state,
        "report": report,
        "step": "completed"
    }

# ==================== 创意孵化器节点 ====================
def idea_validate_node(state: IdeaState) -> IdeaState:
    """步骤 1: 验证痛点"""
    messages = state["messages"]
    last_message = messages[-1] if messages else None
    
    if not last_message or not isinstance(last_message, HumanMessage):
        return state
    
    idea = last_message.content.strip()
    
    response = f"""💡 **创意：{idea}**

让我帮你验证这个创意的价值。

**问题 1/3：** 这个创意解决了什么痛点？
请描述目标用户当前的困扰或需求。
"""
    
    return {
        **state,
        "idea": idea,
        "step": "validating_pain_point"
    }

def idea_users_node(state: IdeaState) -> IdeaState:
    """步骤 2: 定义目标用户"""
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""
    
    pain_point = last_message.strip()
    
    response = f"""✅ 痛点：{pain_point}

**问题 2/3：** 谁是你的目标用户？
请描述用户画像（年龄/职业/特征等）
"""
    
    return {
        **state,
        "pain_point": pain_point,
        "step": "defining_users"
    }

def idea_features_node(state: IdeaState) -> IdeaState:
    """步骤 3: 优先功能"""
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""
    
    target_users = last_message.strip()
    
    # 生成 MVP 功能列表
    mvp_features = [
        "核心功能 1: 解决主要痛点的基础功能",
        "核心功能 2: 最小可用产品必需",
        "辅助功能 1: 提升用户体验",
        "辅助功能 2: 差异化特色"
    ]
    
    response = f"""✅ 目标用户：{target_users}

**问题 3/3：** 基于以上信息，我为你生成了 MVP 功能列表：

{chr(10).join(f'{i+1}. {f}' for i, f in enumerate(mvp_features))}

是否调整或确认？
"""
    
    return {
        **state,
        "target_users": target_users,
        "mvp_features": mvp_features,
        "step": "creating_plan"
    }

def idea_plan_node(state: IdeaState) -> IdeaState:
    """步骤 4: 创建执行计划"""
    mvp_features = state.get("mvp_features", [])
    
    # 生成 4 周执行计划
    plan = {
        "week_1": {
            "focus": "需求确认 + 技术选型",
            "tasks": ["完善需求文档", "技术栈调研", "搭建开发环境"]
        },
        "week_2": {
            "focus": "核心功能开发",
            "tasks": ["实现核心功能 1", "实现核心功能 2", "内部测试"]
        },
        "week_3": {
            "focus": "辅助功能 + 优化",
            "tasks": ["实现辅助功能", "UI/UX优化", "性能调优"]
        },
        "week_4": {
            "focus": "测试 + 发布",
            "tasks": ["完整测试", "Bug 修复", "上线发布"]
        }
    }
    
    # 生成报告
    report = f"""# 🚀 MVP 执行计划

## 创意
{state.get('idea', '')}

## 痛点
{state.get('pain_point', '')}

## 目标用户
{state.get('target_users', '')}

## MVP 功能
{chr(10).join(f'- {f}' for f in mvp_features)}

## 4 周计划

### 第 1 周：{plan['week_1']['focus']}
{chr(10).join(f'- {t}' for t in plan['week_1']['tasks'])}

### 第 2 周：{plan['week_2']['focus']}
{chr(10).join(f'- {t}' for t in plan['week_2']['tasks'])}

### 第 3 周：{plan['week_3']['focus']}
{chr(10).join(f'- {t}' for t in plan['week_3']['tasks'])}

### 第 4 周：{plan['week_4']['focus']}
{chr(10).join(f'- {t}' for t in plan['week_4']['tasks'])}

---
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
*IdeaForge 创意孵化器*
"""
    
    # 保存到历史记录
    history_item = {
        "id": f"idea_{len(memory_store['history']) + 1}",
        "type": "idea",
        "idea": state.get('idea', ''),
        "created_at": datetime.now().isoformat(),
        "report": report
    }
    memory_store["history"].append(history_item)
    
    response = f"""✅ **MVP 执行计划已生成！**

{report}

---
💡 你可以：
1. 复制计划保存
2. 开始新的创意
3. 切换到"决策导航仪"
"""
    
    return {
        **state,
        "plan": plan,
        "step": "completed"
    }

# ==================== 构建 Graphs ====================
def build_decision_graph():
    """构建决策导航仪图"""
    graph = StateGraph(DecisionState)
    
    graph.add_node("clarify", decision_clarify_node)
    graph.add_node("options", decision_options_node)
    graph.add_node("matrix", decision_matrix_node)
    graph.add_node("report", decision_report_node)
    
    graph.add_edge(START, "clarify")
    graph.add_edge("clarify", "options")
    graph.add_edge("options", "matrix")
    graph.add_edge("matrix", "report")
    graph.add_edge("report", END)
    
    return graph.compile()

def build_idea_graph():
    """构建创意孵化器图"""
    graph = StateGraph(IdeaState)
    
    graph.add_node("validate", idea_validate_node)
    graph.add_node("users", idea_users_node)
    graph.add_node("features", idea_features_node)
    graph.add_node("plan", idea_plan_node)
    
    graph.add_edge(START, "validate")
    graph.add_edge("validate", "users")
    graph.add_edge("users", "features")
    graph.add_edge("features", "plan")
    graph.add_edge("plan", END)
    
    return graph.compile()

# 编译 Graphs
decision_graph = build_decision_graph()
idea_graph = build_idea_graph()

# ==================== AG-UI 桥接 ====================
# 决策导航仪端点
decision_bridge = AGUIBridge(
    graph=decision_graph,
    input_schema=DecisionState,
)

# 创意孵化器端点
idea_bridge = AGUIBridge(
    graph=idea_graph,
    input_schema=IdeaState,
)

# 注册路由（使用不同 agent 标识）
decision_bridge.register_routes(app, prefix="/decision")
idea_bridge.register_routes(app, prefix="/idea")

# ==================== 辅助 API ====================
@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "service": "ideaforge-backend",
        "version": "0.1.0"
    }

@app.get("/api/history")
async def get_history():
    """获取历史记录"""
    return {
        "history": memory_store["history"][-10:]  # 最近 10 条
    }

@app.delete("/api/history")
async def clear_history():
    """清空历史记录"""
    memory_store["history"] = []
    return {"status": "ok"}

# ==================== 主入口 ====================
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 启动 IdeaForge 后端...")
    print("📡 决策导航仪：http://localhost:8000/decision")
    print("📡 创意孵化器：http://localhost:8000/idea")
    print("🏥 健康检查：http://localhost:8000/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
