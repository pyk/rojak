require('dotenv').config({ path: './.env.dev' });
const webpack = require('webpack');
const combineLoaders = require('webpack-combine-loaders');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const envars = Object.keys(process.env)
    .map(key => ({ key, value: process.env[key] }))
    .reduce((prev, curr) => Object.assign({}, prev, {
        [`process.env.${curr.key}`]: JSON.stringify(curr.value),
    }), {});

module.exports = {
    devtool: 'source-maps',
    entry: {
        main: [
            'webpack-dev-server/client?http://localhost:3000',
            'webpack/hot/only-dev-server',
            './src/index',
        ],
    },
    output: {
        path: '/',
        publicPath: '/',
        filename: '[name].js',
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.DefinePlugin(envars),
        new HtmlWebpackPlugin({
            title: process.env.APP_TITLE,
            template: '!!ejs!src/index.ejs',
        }),
        new webpack.NoErrorsPlugin(),
    ],
    module: {
        loaders: [{
            test: /\.js$/,
            exclude: /node_modules/,
            loader: combineLoaders([
                { loader: 'react-hot' },
                {
                    loader: 'babel',
                    query: {
                        presets: ['react', 'es2015', 'stage-2'],
                        cacheDirectory: true,
                    },
                },
            ]),
        },
        {
            test: /\.(svg|png|jpg|jpeg)$/i,
            loader: 'file',
        }],
    },
};
