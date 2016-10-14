require('dotenv').config({ path: './.env.prod' });
const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const envars = Object.keys(process.env)
    .map(key => ({ key, value: process.env[key] }))
    .reduce((prev, curr) => Object.assign({}, prev, {
        [`process.env.${curr.key}`]: JSON.stringify(curr.value),
    }), {});

module.exports = {
    target: 'web',
    devtool: 'source-map',
    entry: {
        main: './src/index.js',
        vendors: [
            'react',
            'react-dom',
            'react-addons-update',
            'react-router',
            'reselect',
            'redux',
            'react-redux',
            'bluebird',
            'react-uikit-form',
        ],
    },
    output: {
        path: './build',
        filename: 'bundle.min.[hash].js',
        publicPath: '/',
    },
    plugins: [
        new webpack.optimize.CommonsChunkPlugin('vendors', 'vendor.[hash].js', true),
        new webpack.optimize.DedupePlugin(),
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.optimize.AggressiveMergingPlugin(),
        new HtmlWebpackPlugin({
            title: process.env.APP_TITLE,
            template: 'src/index.ejs',
        }),
        new webpack.DefinePlugin(envars),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false,
            },
            sourceMap: true,
            mangle: true,
            preserveComments: false,
            output: {
                comments: false,
            },
        }),
    ],
    module: {
        loaders: [
            {
                test: /\.js$/,
                loader: 'babel',
                include: path.join(__dirname, 'src'),
                query: {
                    sourceMap: true,
                    cacheDirectory: true,
                },
            },
            {
                test: /\.(svg|png|jpg|jpeg)$/i,
                loader: 'file',
            },
            {
                test: /\.css$/,
                loader: "style-loader!css-loader?modules",
            },
            {
                test: /\.json$/i,
                loader: 'json',
            }
        ],
    },
    resolve: {
        alias: {
            bluebird: './node_modules/bluebird/js/browser/bluebird.core.min.js',
        },
    },
};
