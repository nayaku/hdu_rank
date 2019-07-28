let devServer = (process.env.NODE_ENV === 'development') ? {
  devServer: {
    proxy: 'http://localhost:5000'
  }
} : {}
module.exports = {
  // 生产环境是否生成 sourceMap 文件
  productionSourceMap: false,
  // 输出文件目录
  outputDir: './../static/',
  // 产品模式下去除console.log
  configureWebpack: (config) => {
    if (process.env.NODE_ENV === 'production') {
      config.optimization.minimizer[0].options.terserOptions.compress.drop_console = true
    }
  },
  ...devServer
}
