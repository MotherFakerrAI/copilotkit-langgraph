'use client';

import { useState } from 'react';
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

// 模式类型
type Mode = 'learn' | 'decision' | 'idea' | null;

export default function Home() {
  const [mode, setMode] = useState<Mode>('learn'); // 默认学习伴侣
  const [runtimeUrl, setRuntimeUrl] = useState('/api/copilotkit');

  // 模式卡片组件
  const ModeCard = ({ 
    id, 
    title, 
    icon, 
    description, 
    onSelect 
  }: { 
    id: Mode; 
    title: string; 
    icon: string; 
    description: string;
    onSelect: (id: Mode) => void;
  }) => (
    <div 
      onClick={() => onSelect(id)}
      className={`bg-white rounded-xl shadow-lg p-6 cursor-pointer hover:shadow-xl transition-shadow border-2 ${
        mode === id ? 'border-blue-500' : 'border-transparent hover:border-blue-500'
      }`}
    >
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-bold text-gray-800 mb-2">{title}</h3>
      <p className="text-gray-600 text-sm">{description}</p>
    </div>
  );

  // 返回首页
  const goHome = () => {
    setMode(null);
  };

  return (
    <CopilotKit
      runtimeUrl={runtimeUrl}
      agent={
        mode === 'decision' ? 'decision_agent' : 
        mode === 'idea' ? 'idea_agent' : 'learn_agent'
      }
    >
      <main className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-purple-50">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <header className="text-center mb-8">
            <div className="flex items-center justify-center gap-2 mb-2">
              <button 
                onClick={goHome}
                className="text-gray-500 hover:text-gray-700 text-sm"
              >
                ← 返回
              </button>
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-green-600 via-blue-600 to-purple-600 bg-clip-text text-transparent mb-3">
              📚 LearnLoop
            </h1>
            <p className="text-gray-600 text-lg">
              监督式学习伴侣
            </p>
          </header>

          {/* 模式选择 */}
          {!mode && (
            <div className="max-w-6xl mx-auto">
              <div className="grid md:grid-cols-3 gap-6 mb-8">
                <ModeCard
                  id="learn"
                  title="📚 学习伴侣"
                  icon="📚"
                  description="设定学习目标，AI 帮你规划路径、每日打卡、跟踪进度。"
                  onSelect={(id) => {
                    setMode(id);
                    setRuntimeUrl('/api/learn');
                  }}
                />
                <ModeCard
                  id="decision"
                  title="🧭 决策导航仪"
                  icon="🧭"
                  description="面临选择困难？帮你分析各维度，做出明智决策。"
                  onSelect={(id) => {
                    setMode(id);
                    setRuntimeUrl('/api/decision');
                  }}
                />
                <ModeCard
                  id="idea"
                  title="🚀 创意孵化器"
                  icon="🚀"
                  description="有好点子？帮你验证痛点，定义 MVP，生成执行计划。"
                  onSelect={(id) => {
                    setMode(id);
                    setRuntimeUrl('/api/idea');
                  }}
                />
              </div>

              {/* 使用说明 */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4">💡 使用指南</h2>
                <div className="grid md:grid-cols-3 gap-6">
                  <div>
                    <h3 className="font-semibold text-green-600 mb-2">📚 学习伴侣</h3>
                    <ol className="text-gray-600 text-sm space-y-1 list-decimal list-inside">
                      <li>输入学习目标（如"3 个月学会 Python"）</li>
                      <li>AI 生成学习路径和周计划</li>
                      <li>每日打卡报告进度</li>
                      <li>查看进度和成就</li>
                    </ol>
                  </div>
                  <div>
                    <h3 className="font-semibold text-blue-600 mb-2">🧭 决策导航仪</h3>
                    <ol className="text-gray-600 text-sm space-y-1 list-decimal list-inside">
                      <li>输入决策问题</li>
                      <li>AI 从多维度追问</li>
                      <li>输入选项</li>
                      <li>生成对比矩阵和报告</li>
                    </ol>
                  </div>
                  <div>
                    <h3 className="font-semibold text-purple-600 mb-2">🚀 创意孵化器</h3>
                    <ol className="text-gray-600 text-sm space-y-1 list-decimal list-inside">
                      <li>输入创意想法</li>
                      <li>验证痛点和用户</li>
                      <li>生成 MVP 功能</li>
                      <li>输出 4 周计划</li>
                    </ol>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* 聊天界面 */}
          {mode && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                <CopilotChat
                  className="h-[600px]"
                  placeholder={
                    mode === 'learn'
                      ? "输入你的学习目标，例如：3 个月学会 Python"
                      : mode === 'decision'
                      ? "输入你的决策问题，例如：要不要跳槽？"
                      : "输入你的创意想法，例如：做一个 AI 写作工具"
                  }
                  labels={{
                    initial: mode === 'learn'
                      ? "📚 你好！我是你的学习伴侣。告诉我你想学什么，我来帮你规划学习路径！"
                      : mode === 'decision'
                      ? "🧭 你好！我来帮你做出明智决策。请告诉我你面临的选择问题。"
                      : "🚀 你好！我来帮你孵化创意。请告诉我你的想法。"
                  }}
                />
              </div>

              {/* 快捷操作 */}
              <div className="mt-4 flex gap-4 justify-center">
                <button
                  onClick={goHome}
                  className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                >
                  切换模式
                </button>
                <button
                  onClick={() => window.open('/api/history', '_blank')}
                  className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                >
                  查看历史
                </button>
              </div>
            </div>
          )}

          {/* Footer */}
          <footer className="mt-12 text-center text-gray-500 text-sm">
            <p>Made with ❤️ by MotherFaker Studio</p>
            <p className="mt-1">
              技术栈：Next.js + CopilotKit + LangGraph + FastAPI
            </p>
          </footer>
        </div>
      </main>
    </CopilotKit>
  );
}
