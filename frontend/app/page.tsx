'use client';

import { useState } from 'react';
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

// 模式类型
type Mode = 'decision' | 'idea' | null;

export default function Home() {
  const [mode, setMode] = useState<Mode>(null);
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
      className="bg-white rounded-xl shadow-lg p-6 cursor-pointer hover:shadow-xl transition-shadow border-2 border-transparent hover:border-blue-500"
    >
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-bold text-gray-800 mb-2">{title}</h3>
      <p className="text-gray-600 text-sm">{description}</p>
    </div>
  );

  // 返回首页
  const goHome = () => {
    setMode(null);
    setRuntimeUrl('/api/copilotkit');
  };

  return (
    <CopilotKit
      runtimeUrl={runtimeUrl}
      agent={mode === 'decision' ? 'decision_agent' : 'idea_agent'}
    >
      <main className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
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
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">
              💡 IdeaForge
            </h1>
            <p className="text-gray-600 text-lg">
              决策导航仪 + 创意孵化器
            </p>
          </header>

          {/* 模式选择 */}
          {!mode && (
            <div className="max-w-4xl mx-auto">
              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <ModeCard
                  id="decision"
                  title="🧭 决策导航仪"
                  icon="🧭"
                  description="面临选择困难？帮你分析各维度，生成对比矩阵，做出明智决策。"
                  onSelect={(id) => {
                    setMode(id);
                    setRuntimeUrl('/api/decision');
                  }}
                />
                <ModeCard
                  id="idea"
                  title="🚀 创意孵化器"
                  icon="🚀"
                  description="有好点子？帮你验证痛点，定义 MVP，生成 4 周执行计划。"
                  onSelect={(id) => {
                    setMode(id);
                    setRuntimeUrl('/api/idea');
                  }}
                />
              </div>

              {/* 使用说明 */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4">💡 使用指南</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold text-blue-600 mb-2">🧭 决策导航仪</h3>
                    <ol className="text-gray-600 text-sm space-y-1 list-decimal list-inside">
                      <li>输入你的决策问题（如"要不要跳槽"）</li>
                      <li>AI 会从多个维度追问澄清</li>
                      <li>输入 2-3 个选项</li>
                      <li>生成对比矩阵和决策报告</li>
                    </ol>
                  </div>
                  <div>
                    <h3 className="font-semibold text-purple-600 mb-2">🚀 创意孵化器</h3>
                    <ol className="text-gray-600 text-sm space-y-1 list-decimal list-inside">
                      <li>输入你的创意想法</li>
                      <li>AI 引导验证痛点和目标用户</li>
                      <li>生成 MVP 功能列表</li>
                      <li>输出 4 周执行计划</li>
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
                    mode === 'decision' 
                      ? "输入你的决策问题，例如：要不要跳槽？"
                      : "输入你的创意想法，例如：做一个 AI 写作工具"
                  }
                  labels={{
                    initial: mode === 'decision'
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
