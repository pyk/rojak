import React from 'react';
import { Provider } from 'react-redux';
import Routes from './Routes';
import store from './store';

class App extends React.Component {
    render() {
        return (
            <Provider store={store}>
                <Routes />
            </Provider>
        );
    }
}

export default App;
