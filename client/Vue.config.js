const plugins = ['@vue/babel-plugin-transform-vue-jsx']

let devServer = (process.env.NODE_ENV === 'development') ? {
  devServer: {
    proxy: 'http://localhost:5000'
  }
} : {}

// 生产环境移除console
if (process.env.NODE_ENV === 'production') {
  plugins.push('transform-remove-console')
}
module.exports = {
  // 生产环境是否生成 sourceMap 文件
  productionSourceMap: false,
  // 输出文件目录
  outputDir: './../static/',
  ...devServer
}
