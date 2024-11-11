const HtmlWebpackPlugin = require("html-webpack-plugin");
const ModuleFederationPlugin = require("webpack/lib/container/ModuleFederationPlugin");

module.exports = {
  entry: "./src/index",
  mode: "development",
  devServer: {
    port: 3000,
    hot: true,
    historyApiFallback: true,
    allowedHosts: "all",
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-react", "@babel/preset-typescript"],
          },
        },
      },
      {
        test: /\.scss$/,
        use: ["style-loader", "css-loader", "postcss-loader"],
      },
      {
        test: /\.(png|jpg|gif|svg|eot|ttf|woff)$/,
        use: ["file-loader"],
      },
    ],
  },
  plugins: [
    new ModuleFederationPlugin({
      name: "todoApp",
      filename: "remoteEntry.js",
      exposes: {
        "./TodoList": "./src/components/TodoList",
      },
      shared: {
        react: { singleton: true, eager: true, requiredVersion: "^18.2.0" },
        "react-dom": {
          singleton: true,
          eager: true,
          requiredVersion: "^18.2.0",
        },
        "@reduxjs/toolkit": {
          singleton: true,
          eager: true,
          requiredVersion: "^1.9.5",
        },
        "react-redux": {
          singleton: true,
          eager: true,
          requiredVersion: "^8.1.1",
        },
        "@heroicons/react": {
          singleton: true,
          eager: true,
          requiredVersion: "^2.1.5",
        },
      },
    }),
    new HtmlWebpackPlugin({
      template: "./public/index.html",
    }),
  ],
  resolve: {
    extensions: [".ts", ".tsx", ".js"],
  },
};
