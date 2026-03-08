"""
LearnLoop - 学习伴侣（监督式学习）
基于 CopilotKit AG-UI 协议

功能：
1. 学习目标设定
2. 学习路径规划
3. 每日打卡
4. 进度可视化
"""

from typing import Annotated, TypedDict, List, Optional, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ag_ui_langgraph import AGUIBridge
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from datetime import datetime, timedelta

# ==================== 环境配置 ====================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-demo-key")

# ==================== FastAPI 应用 ====================
app = FastAPI(title="LearnLoop Backend")

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

# ==================== LearnState 定义 ====================
class LearnState(TypedDict):
    """学习伴侣状态"""
    messages: Annotated[List, add_messages]
    user_id: str                 # 用户 ID（MVP 用 session）
    goal: str                    # 学习目标
    subject: str                 # 学科/技能
    deadline: str                # 截止日期
    plan: dict                   # 学习计划 {week1: [...], week2: [...]}
    progress: dict               # 进度记录 {date: status}
    weak_points: List[str]       # 弱点列表
    streak: int                  # 连续打卡天数
    step: str                    # 当前步骤

# ==================== Node 函数 ====================
def goal_node(state: LearnState) -> LearnState:
    """步骤 1: 设定学习目标"""
    messages = state["messages"]
    last_message = messages[-1] if messages else None
    
    if not last_message or not isinstance(last_message, HumanMessage):
        return state
    
    goal = last_message.content.strip()
    
    # 解析目标（简单关键词提取）
    subject = "通用技能"
    deadline = "3 个月"
    
    # 检测学科关键词
    if any(kw in goal.lower() for kw in ['python', '编程', '代码']):
        subject = "Python 编程"
    elif any(kw in goal.lower() for kw in ['英语', 'english', '语言']):
        subject = "英语学习"
    elif any(kw in goal.lower() for kw in ['数学', 'math']):
        subject = "数学"
    
    # 检测时间关键词
    if any(kw in goal for kw in ['1 个月', '一个月', '30 天']):
        deadline = "1 个月"
    elif any(kw in goal for kw in ['3 个月', '三个月', '90 天']):
        deadline = "3 个月"
    elif any(kw in goal for kw in ['6 个月', '六个月', '180 天']):
        deadline = "6 个月"
    
    response = f"""🎯 **学习目标：{goal}**

**学科：** {subject}
**期限：** {deadline}

正在为你生成学习路径...

---
💡 学习路径已生成！我将帮你：
1. 拆解成周任务
2. 制定每日待办
3. 跟踪进度和打卡
4. 分析弱点并调整计划

准备好了吗？我们开始吧！📚
"""
    
    # 生成学习计划（MVP 用模板）
    plan = generate_learning_plan(subject, deadline)
    
    return {
        **state,
        "goal": goal,
        "subject": subject,
        "deadline": deadline,
        "plan": plan,
        "step": "plan_created"
    }

def plan_node(state: LearnState) -> LearnState:
    """步骤 2: 展示学习计划"""
    plan = state.get("plan", {})
    subject = state.get("subject", "")
    
    response = f"""📚 **{subject} 学习路径**

"""
    
    # 展示周计划
    for week_num in range(1, min(5, len(plan) + 1)):
        week_key = f"week_{week_num}"
        if week_key in plan:
            week_data = plan[week_key]
            response += f"""**第{week_num}周：{week_data.get('focus', '学习主题')}**
"""
            for i, task in enumerate(week_data.get('tasks', [])[:3], 1):
                response += f"  {i}. {task}\n"
            response += "\n"
    
    response += """---
💡 **每日打卡说明：**
- 每天完成后回复"打卡"或"完成今日任务"
- 我会记录你的进度
- 连续打卡有奖励哦！🏆

现在告诉我，你想从第几周开始？或者直接说"开始学习"！
"""
    
    return {
        **state,
        "step": "ready_to_start"
    }

def checkin_node(state: LearnState) -> LearnState:
    """步骤 3: 每日打卡"""
    messages = state["messages"]
    
    # 获取今天日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 更新进度
    progress = state.get("progress", {})
    progress[today] = {
        "status": "completed",
        "date": today,
        "note": "完成今日任务"
    }
    
    # 计算连续打卡天数
    streak = calculate_streak(progress)
    
    # 获取今日任务
    today_task = get_today_task(state.get("plan", {}), progress)
    
    response = f"""✅ **打卡成功！**

📅 日期：{today}
🔥 连续打卡：{streak} 天
📊 总完成：{len(progress)} 天

"""
    
    if streak >= 7:
        response += f"""🏆 **成就解锁！**
连续打卡{streak}天，太棒了！继续保持！🎉

"""
    
    response += f"""---
📋 **今日任务：**
{today_task}

明天继续加油！💪
"""
    
    # 保存到历史记录
    history_item = {
        "id": f"checkin_{len(memory_store['history']) + 1}",
        "type": "checkin",
        "date": today,
        "streak": streak,
        "created_at": datetime.now().isoformat()
    }
    memory_store["history"].append(history_item)
    
    return {
        **state,
        "progress": progress,
        "streak": streak,
        "step": "checked_in"
    }

def review_node(state: LearnState) -> LearnState:
    """步骤 4: 复习进度"""
    progress = state.get("progress", {})
    plan = state.get("plan", {})
    goal = state.get("goal", "")
    
    total_days = len(progress)
    streak = state.get("streak", 0)
    
    # 计算完成度
    total_tasks = sum(len(week.get('tasks', [])) for week in plan.values())
    completed_tasks = total_days * 3  # 假设每天 3 个任务
    completion_rate = min(100, int((completed_tasks / max(1, total_tasks)) * 100))
    
    response = f"""📊 **学习进度报告**

🎯 目标：{goal}

**整体进度：**
完成度：{completion_rate}%
已学习：{total_days} 天
连续打卡：{streak} 天 🔥

"""
    
    # 弱点分析（MVP 简单版本）
    weak_points = state.get("weak_points", [])
    if not weak_points and total_days >= 3:
        weak_points = ["需要加强复习", "可以增加练习量"]
        response += f"""**弱点分析：**
{chr(10).join(f'• {wp}' for wp in weak_points)}

建议：
1. 每周安排 1 次复习日
2. 增加实践练习比例

"""
    
    # 进度可视化（文本版）
    response += f"""**最近打卡记录：**
"""
    recent_dates = sorted(progress.keys())[-5:]
    for date in recent_dates:
        status_emoji = "✅" if progress[date].get("status") == "completed" else "⏳"
        response += f"{status_emoji} {date}\n"
    
    response += f"""
---
💡 继续加油！坚持就是胜利！🚀
"""
    
    return {
        **state,
        "weak_points": weak_points,
        "step": "reviewed"
    }

# ==================== 辅助函数 ====================
def generate_learning_plan(subject: str, deadline: str) -> dict:
    """生成学习计划（MVP 用模板）"""
    
    # 不同学科的模板
    plans = {
        "Python 编程": {
            "week_1": {
                "focus": "Python 基础语法",
                "tasks": ["变量和数据类型", "条件语句和循环", "函数定义", "列表和字典"]
            },
            "week_2": {
                "focus": "面向对象编程",
                "tasks": ["类和对象", "继承和多态", "异常处理", "模块和包"]
            },
            "week_3": {
                "focus": "常用库学习",
                "tasks": ["文件操作", "数据处理 (pandas)", "网络请求", "数据可视化"]
            },
            "week_4": {
                "focus": "实战项目",
                "tasks": ["小项目设计", "代码实现", "测试调试", "文档编写"]
            }
        },
        "英语学习": {
            "week_1": {
                "focus": "词汇积累",
                "tasks": ["每日 50 词", "词根词缀", "同义词辨析", "词汇复习"]
            },
            "week_2": {
                "focus": "语法强化",
                "tasks": ["时态语态", "从句结构", "非谓语动词", "语法练习"]
            },
            "week_3": {
                "focus": "听说训练",
                "tasks": ["听力练习", "口语跟读", "对话模拟", "发音纠正"]
            },
            "week_4": {
                "focus": "阅读写作",
                "tasks": ["阅读理解", "写作练习", "作文修改", "综合测试"]
            }
        }
    }
    
    # 默认计划
    default_plan = {
        "week_1": {"focus": "基础知识", "tasks": ["概念学习", "基础练习", "复习总结"]},
        "week_2": {"focus": "进阶内容", "tasks": ["深入学习", "实践应用", "复习总结"]},
        "week_3": {"focus": "实战练习", "tasks": ["项目实践", "问题解决", "复习总结"]},
        "week_4": {"focus": "综合提升", "tasks": ["综合测试", "弱点强化", "总结复盘"]}
    }
    
    return plans.get(subject, default_plan)

def calculate_streak(progress: dict) -> int:
    """计算连续打卡天数"""
    if not progress:
        return 0
    
    today = datetime.now().date()
    streak = 0
    
    for i in range(365):  # 最多回溯 365 天
        check_date = today - timedelta(days=i)
        date_str = check_date.strftime("%Y-%m-%d")
        
        if date_str in progress:
            streak += 1
        elif i > 0:  # 今天没打卡也算连续
            break
        else:
            streak += 1  # 今天打卡了
    
    return streak

def get_today_task(plan: dict, progress: dict) -> str:
    """获取今日任务"""
    if not plan:
        return "暂无计划"
    
    # 简单返回第一周任务（MVP）
    first_week = plan.get("week_1", {})
    tasks = first_week.get("tasks", ["学习任务"])
    
    return "\n".join(f"• {task}" for task in tasks[:3])

# ==================== 构建 Graph ====================
def build_learn_graph():
    """构建学习伴侣图"""
    graph = StateGraph(LearnState)
    
    graph.add_node("goal", goal_node)
    graph.add_node("plan", plan_node)
    graph.add_node("checkin", checkin_node)
    graph.add_node("review", review_node)
    
    # 定义流程
    graph.add_edge(START, "goal")
    graph.add_edge("goal", "plan")
    graph.add_edge("plan", "checkin")  # 默认进入打卡流程
    
    # 根据条件跳转（简化版）
    graph.add_edge("checkin", "review")  # 打卡后可查看进度
    graph.add_edge("review", END)
    
    return graph.compile()

# 编译 Graph
learn_graph = build_learn_graph()

# ==================== AG-UI 桥接 ====================
learn_bridge = AGUIBridge(
    graph=learn_graph,
    input_schema=LearnState,
)

# 注册路由
learn_bridge.register_routes(app, prefix="/learn")

# ==================== 辅助 API ====================
@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "service": "learnloop-backend",
        "version": "0.1.0"
    }

@app.get("/api/history")
async def get_history():
    """获取历史记录"""
    return {
        "history": memory_store["history"][-10:]
    }

@app.get("/api/progress")
async def get_progress(session_id: str = "default"):
    """获取学习进度"""
    session = memory_store["sessions"].get(session_id, {})
    return {
        "goal": session.get("goal", ""),
        "progress": session.get("progress", {}),
        "streak": session.get("streak", 0),
        "plan": session.get("plan", {})
    }

# ==================== 主入口 ====================
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 启动 LearnLoop 后端...")
    print("📡 学习伴侣端点：http://localhost:8000/learn")
    print("🏥 健康检查：http://localhost:8000/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
