const { createProxyMiddleware } = require('http-proxy-middleware');
module.exports = function (app) {
    app.use(
        '/api',
        createProxyMiddleware({
            target: 'http://34.238.156.1:8093',
            changeOrigin: true,
            pathRewrite: {
                '^/api': '',
            }
        })
    );
};