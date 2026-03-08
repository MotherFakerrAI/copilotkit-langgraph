"""
MotherFaker Studio - CopilotKit + LangGraph 后端

基于 AG-UI 协议连接 CopilotKit 前端
"""

from typing import Annotated, TypedDict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ag_ui_langgraph import AGUIBridge
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os

# ==================== 环境配置 ====================
# 从环境变量读取 API Key（可选，用于实际 LLM 调用）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-demo-key")

# ==================== FastAPI 应用 ====================
app = FastAPI(title="CopilotKit LangGraph Backend")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Agent 状态定义 ====================
class AgentState(TypedDict):
    """Agent 状态管理"""
    messages: Annotated[List, add_messages]
    user_name: str
    context: dict


# ==================== Agent 节点定义 ====================
def chat_node(state: AgentState) -> AgentState:
    """
    聊天节点 - 处理用户消息
    
    实际项目中这里会调用 LLM
    现在使用简单规则回复作为 Demo
    """
    messages = state["messages"]
    last_message = messages[-1] if messages else None
    
    if not last_message:
        return {"messages": []}
    
    # 简单规则回复（Demo 用）
    if isinstance(last_message, HumanMessage):
        content = last_message.content.lower()
        
        # 根据关键词回复
        if "hello" in content or "你好" in content:
            response = "你好！我是 MotherFaker Studio 的 AI 助手，有什么可以帮你的吗？😊"
        elif "name" in content or "名字" in content:
            response = "我是 CopilotKit + LangGraph 驱动的 AI 助手 🤖"
        elif "help" in content or "帮助" in content:
            response = "我可以帮你：\n1. 回答问题\n2. 执行任务\n3. 提供建议\n\n请告诉我你需要什么帮助！"
        else:
            response = f"收到你的消息：{last_message.content}\n\n（这是 Demo 回复，实际项目中会调用 LLM 生成智能回复）"
        
        return {
            "messages": [AIMessage(content=response)]
        }
    
    return {"messages": []}


def tool_node(state: AgentState) -> AgentState:
    """
    工具调用节点 - 执行工具函数
    
    实际项目中这里会调用各种工具
    """
    messages = state["messages"]
    
    # 简单 Demo：不实际调用工具
    return {"messages": []}


# ==================== 构建 LangGraph ====================
def build_graph():
    """构建 Agent 图"""
    graph = StateGraph(AgentState)
    
    # 添加节点
    graph.add_node("chat", chat_node)
    graph.add_node("tools", tool_node)
    
    # 定义边
    graph.add_edge(START, "chat")
    graph.add_edge("chat", END)
    # graph.add_edge("tools", "chat")  # 工具调用后返回聊天
    
    return graph.compile()


# 编译图
agent_graph = build_graph()


# ==================== AG-UI 桥接 ====================
# 使用 ag-ui-langgraph 将 LangGraph 暴露为 AG-UI 端点
ag_ui_bridge = AGUIBridge(
    graph=agent_graph,
    input_schema=AgentState,
)

# 注册 AG-UI 端点到 FastAPI
ag_ui_bridge.register_routes(app)


# ==================== 健康检查 ====================
@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "ok",
        "service": "copilotkit-langgraph-backend",
        "version": "0.1.0"
    }


# ==================== 主入口 ====================
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 启动 CopilotKit LangGraph 后端...")
    print("📡 AG-UI 端点：http://localhost:8000")
    print("🏥 健康检查：http://localhost:8000/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
