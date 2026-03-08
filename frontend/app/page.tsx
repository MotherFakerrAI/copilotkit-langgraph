'use client';

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function Home() {
  return (
    <CopilotKit
      // 使用本地后端 AG-UI 端点（不依赖 Copilot Cloud）
      runtimeUrl="/api/copilotkit"
      agent="assistant"
    >
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <header className="text-center mb-8">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
              🤖 CopilotKit + LangGraph
            </h1>
            <p className="text-gray-600">
              MotherFaker Studio - AG-UI 协议演示
            </p>
          </header>

          {/* Chat Interface */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <CopilotChat
                className="h-[600px]"
                placeholder="输入消息开始对话..."
                labels={{
                  initial: "你好！我是 AI 助手，有什么可以帮你的吗？",
                }}
              />
            </div>
          </div>

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
