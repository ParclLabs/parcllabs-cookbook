/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://api.parcllabs.com/v1/:path*',
      },
    ];
  },
};

export default nextConfig;
