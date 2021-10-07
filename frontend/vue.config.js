const BundleTracker = require("webpack-bundle-tracker");
const debug = !process.env.PEPS_DEBUG || process.env.PEPS_DEBUG === 'True'
const publicPath = debug ? "http://localhost:8080/" : "/static/"

module.exports = {
  pwa: {
    name: 'Peps',
    themeColor: '#008763',
    msTileColor: '#008763',
    appleMobileWebAppStatusBarStyle: 'black',
    iconPaths: {
      favicon32: '/favicon-32x32.png',
      favicon16: '/favicon-16x16.png',
      appleTouchIcon: '/apple-touch-icon.png',
      maskIcon: '/safari-pinned-tab.svg',
      msTileImage: '/mstile-150x150.png'
    },
    manifestOptions: {
      icons: [{
        'src': publicPath + 'android-chrome-192x192.png',
        'sizes': '192x192',
        'type': 'image/png'
      }, {
        'src': publicPath + 'android-chrome-512x512.png',
        'sizes': '512x512',
        'type': 'image/png'
      }]
    }
  },
  "transpileDependencies": [
    "vuetify"
  ],
  publicPath: publicPath,
  outputDir: './dist/',

  configureWebpack: {
    devtool: 'source-map',
  },

  chainWebpack: config => {

    config.optimization
      .splitChunks(false)

    config
      .plugin('BundleTracker')
      .use(BundleTracker, [{ filename: '../frontend/webpack-stats.json' }])

    config.resolve.alias
      .set('__STATIC__', 'static')

    config.devServer
      .public('http://localhost:8080')
      .host('localhost')
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      // eslint-disable-next-line no-useless-escape
      .headers({ "Access-Control-Allow-Origin": ["\*"] })
  }
}