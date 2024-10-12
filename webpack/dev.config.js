const { merge } = require("webpack-merge");
const commonConfig = require("./common.config");
const path = require("path");
module.exports = merge(commonConfig, {
  mode: "development",
  devtool: "inline-source-map",
  performance: { hints: false },
  devServer: {
    port: 3000,
    proxy: [
      {
        context: ["/"],
        target: "http://127.0.0.1:8000",
      },
    ],
    client: {
      overlay: {
        errors: true,
        warnings: false,
        runtimeErrors: true,
      },
    },
    static: {
      directory: path.resolve(__dirname, "../", "dist", "webpack_bundles"),
    },
    // We need hot=false (Disable HMR) to set liveReload=true
    hot: false,
    liveReload: true,
    open: true,
  },
});
