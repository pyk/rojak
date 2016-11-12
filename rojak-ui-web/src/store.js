import { createStore, combineReducers, compose, applyMiddleware } from 'redux'
import { reduxReactRouter, routerStateReducer } from 'redux-router'
import { createHistory } from 'history'
import thunk from 'redux-thunk'

import sentiments from './app/sentiments/reducer';
import viewer from './app/viewer/reducer';
import medias from './app/media/reducer';
import candidates from './app/candidate/reducer';
import root from './app/root/reducer';

const reducers = combineReducers({
    router: routerStateReducer,
    viewer,
    medias,
    candidates,
    sentiments,
    root,
});

export default compose(
  reduxReactRouter({ createHistory }),
  applyMiddleware(thunk),
  window.devToolsExtension ? window.devToolsExtension() : f => f
)(createStore)(reducers)
