import { Router, Route, IndexRoute, hashHistory } from 'react-router';
import React from 'react';

import Container from './app/utils/Container';
import HomePage from './app/home/HomePage';

const Routes = () => (
    <Router history={hashHistory}>
        <Route path="/" component={Container}>
            <IndexRoute component={HomePage} />
        </Route>
    </Router>
);

export default Routes;
