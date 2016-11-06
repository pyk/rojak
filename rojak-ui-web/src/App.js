import React from 'react';
import { Provider } from 'react-redux';
import { ReduxRouter } from 'redux-router';
import routes from './routes';
import store from './store';
import createRojakClient from './app/utils/createRojakClient';

class App extends React.Component {
    static childContextTypes = {
        rojakClient: React.PropTypes.object,
    }

    getChildContext() {
        return {
            rojakClient: createRojakClient(process.env.ROJAK_API_ENDPOINT),
        }
    }

    render() {
        return (
            <Provider store={store}>
                <ReduxRouter routes={routes} />
            </Provider>
        );
    }
}

export default App;
