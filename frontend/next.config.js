/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // API 重写配置（连接后端 AG-UI 端点）
  async rewrites() {
    return [
      {
        source: '/api/copilotkit/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ];
  },
}

module.exports = nextConfig
