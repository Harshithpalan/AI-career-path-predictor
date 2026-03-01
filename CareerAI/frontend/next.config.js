/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    esmExternals: false
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*', // Proxy to backend
      },
    ]
  },
  // Use custom HTML file for index page
  trailingSlash: false,
  pageExtensions: ['jsx', 'js', 'ts', 'tsx', 'mdx'],
  // Disable automatic font optimization to use custom HTML
  optimizeFonts: false,
}

module.exports = nextConfig
