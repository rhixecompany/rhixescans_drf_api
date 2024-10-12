const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require("webpack");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

module.exports = {
  target: "web",
  context: path.join(__dirname, "../"),
  entry: {
    project: path.resolve(__dirname, "../", "api", "static", "scripts", "js", "project"),
    vendors: path.resolve(__dirname, "../", "api", "static", "scripts", "js", "vendors"),
  },
  output: {
    path: path.resolve(__dirname, "../", "dist", "webpack_bundles"),
    publicPath: "/static/webpack_bundles/",
    filename: "js/[name]-[fullhash].js",
    chunkFilename: "js/[name]-[hash].js",
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      // Make the font available globally
      FiraSans: "typeface-fira-sans",
    }),
    new BundleTracker({
      path: path.resolve(path.join(__dirname, "../", "dist", "webpack_bundles")),
      filename: "webpack-stats.json",
    }),
    new MiniCssExtractPlugin({ filename: "css/[name].[contenthash].css" }),
  ],
  module: {
    rules: [
      {
        test: /\.ts?$/i,
        use: "ts-loader",
        exclude: /node_modules/,
      },

      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
      // {
      //   test: /\.(png|svg|jpg|jpeg|gif)$/i,
      //   type: "asset/resource",
      // },

      {
        test: /\.(jpe?g|png|gif|svg|webp)$/i,
        loader: "file-loader",
        options: {
          name: "/assets/[name].[ext]",
          // name(resourcePath, resourceQuery) {
          //   // `resourcePath` - `/absolute/path/to/file.js`
          //   // `resourceQuery` - `?foo=bar`

          //   if (process.env.NODE_ENV === "development") {
          //     return "/assets/[name].[ext]";
          //   }

          //   return "/assets/[contenthash].[ext]";
          // },

          publicPath: "/assets",
          // publicPath: (url, resourcePath, context) => {
          //   // `resourcePath` is original absolute path to asset
          //   // `context` is directory where stored asset (`rootContext`) or `context` option

          //   // To get relative path you can use
          //   // const relativePath = path.relative(context, resourcePath);
          //   if (/black\.webp/.test(resourcePath)) {
          //     return `/assets/other_public_path/${url}`;
          //   }

          //   if (/images/.test(context)) {
          //     return `/assets/image_output_path/${url}`;
          //   }

          //   return `/assets/${url}`;
          // },
        },
      },
    ],
  },
  resolve: {
    modules: ["node_modules"],
    extensions: [".ts", ".js", ".css", "..."],
  },
  optimization: {
    minimize: true,
    minimizer: [new CssMinimizerPlugin()],
  },
};
