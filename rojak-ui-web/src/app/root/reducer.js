import { SET_KEYWORD, SET_SCREEN_EXPANDED } from './actions.js'

const initialState = {
  keyword: '',
  expanded: false
}

export default (state = initialState, action = {}) => {
  switch (action.type) {
    case SET_KEYWORD:
      return Object.assign({}, state, { keyword: action.keyword })
    case SET_SCREEN_EXPANDED:
      return Object.assign({}, state, { expanded: action.expanded })
    default:
      return state;
  }
}
