import { createStore, combineReducers } from 'redux';

import viewer from './app/viewer/reducer';

const reducers = combineReducers({
    viewer,
});

export default createStore(reducers);
