import { Route, IndexRoute } from 'react-router';
import React from 'react';

import Container from './app/utils/Container';
import HomePage from './app/home/HomePage';

export default (
  <Route path='/' component={Container}>
    <IndexRoute component={HomePage} />
    <Route path="search/:keyword" component={HomePage} />
  </Route>
)
