import { SET_MEDIAS, SET_MEDIA } from './actions'

const initialState = {
  list: [],
  media: {}
}

export default (state = initialState, action = {}) => {
  const { payload, type } = action
  switch (type) {
    case SET_MEDIAS:
      return Object.assign({}, state, { list: payload.medias })
    case SET_MEDIA:
      return Object.assign({}, state, { media: payload.media })
    default:
      return state
  }
}
