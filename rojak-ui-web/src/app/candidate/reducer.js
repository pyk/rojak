import { SET_CANDIDATES, SET_CANDIDATE } from './actions'

const initialState = {
  list: [],
  candidate: {}
}

export default (state = initialState, action = {}) => {
  const { type, payload } = action
  switch (type) {
    case SET_CANDIDATES:
      return Object.assign({}, state, { list: payload.candidates })
    case SET_CANDIDATE:
      return Object.assign({}, state, { candidate: payload.candidate })
    default:
      return state
  }
}
