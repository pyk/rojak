import { createStore, combineReducers } from 'redux';

import viewer from './app/viewer/reducer';
import medias from './app/media/reducer';
import candidates from './app/candidate/reducer';

const reducers = combineReducers({
    viewer,
    medias,
    candidates,
});

export default createStore(
    reducers,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);
