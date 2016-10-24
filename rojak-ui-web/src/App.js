import React from 'react';
import { Provider } from 'react-redux';
import { ReduxRouter } from 'redux-router';
import routes from './routes';
import store from './store';

class App extends React.Component {
    render() {
        return (
            <Provider store={store}>
                <ReduxRouter routes={routes} />
            </Provider>
        );
    }
}

export default App;
