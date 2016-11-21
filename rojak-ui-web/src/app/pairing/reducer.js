import { SET_PAIRING, SET_PAIRINGS } from './actions'

const initialState = {
  list: [],
  pairing: {}
}

export default (state = initialState, action = {}) => {
  const { type, payload } = action
  switch (type) {
    case SET_PAIRINGS:
      return Object.assign({}, state, { list: payload.pairings })
    case SET_PAIRING:
      return Object.assign({}, state, { pairing: payload.pairing })
    default:
      return state
  }
}
