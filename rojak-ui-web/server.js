const webpack = require('webpack');
const WebpackDevServer = require('webpack-dev-server');
const config = require('./webpack.config.dev');
const PORT = process.env.PORT || 3000

new WebpackDevServer(webpack(config), {
    publicPath: config.output.publicPath,
    hot: true,
    historyApiFallback: true,
}).listen(PORT, 'localhost', (err, result) => {
    if (err) {
        return console.log(err);
    }

    console.log('Listening at http://localhost:' + PORT + '/');
});
