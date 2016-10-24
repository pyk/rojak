import { createStore, combineReducers, compose } from 'redux'
import { reduxReactRouter, routerStateReducer } from 'redux-router'
import { createHistory } from 'history'

import viewer from './app/viewer/reducer';
import medias from './app/media/reducer';
import candidates from './app/candidate/reducer';
import root from './app/root/reducer';

const reducers = combineReducers({
    router: routerStateReducer,
    viewer,
    medias,
    candidates,
    root
});

export default compose(
  reduxReactRouter({ createHistory }),
  window.devToolsExtension ? window.devToolsExtension() : f => f
)(createStore)(reducers)
