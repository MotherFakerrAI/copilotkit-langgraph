import { CopilotRuntime, OpenAIAdapter } from "@copilotkit/runtime";
import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {
  const copilotRuntimeHandler = new CopilotRuntime({
    // 后端 AG-UI 端点
    remoteActions: [
      {
        url: process.env.BACKEND_URL || "http://localhost:8000",
      },
    ],
    serviceAdapter: new OpenAIAdapter({
      // 使用本地后端，不依赖 OpenAI
      // 实际项目中可以配置真实的 LLM
    }),
  });

  const response = await copilotRuntimeHandler.handleRequest(req);
  return response;
}
