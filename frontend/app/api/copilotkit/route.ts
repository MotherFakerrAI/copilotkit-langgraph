import { CopilotRuntime, OpenAIAdapter } from "@copilotkit/runtime";
import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {
  const copilotRuntimeHandler = new CopilotRuntime({
    // 后端 AG-UI 端点（支持两种模式）
    remoteActions: [
      {
        url: process.env.BACKEND_URL || "http://localhost:8000",
      },
    ],
    serviceAdapter: new OpenAIAdapter({
      // MVP 使用本地后端，不依赖外部 LLM
    }),
  });

  const response = await copilotRuntimeHandler.handleRequest(req);
  return response;
}

// GET 请求用于健康检查
export async function GET() {
  return NextResponse.json({
    status: "ok",
    service: "ideaforge-frontend-api"
  });
}
