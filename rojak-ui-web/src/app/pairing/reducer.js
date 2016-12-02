import { SET_PAIRING, SET_PAIRINGS } from './actions';

const initialState = {
  list: [],
  pairing: {},
  error: null,
  loading_list: false,
  loading_pairing: false
};

export default (state = initialState, action = {}) => {
  const { type, payload } = action
  switch (type) {
    case `${SET_PAIRINGS}_PENDING`:
      // return Object.assign({}, state, { loading_list: true });
      return { ...state, loading_list: true };
    case `${SET_PAIRINGS}_FULFILLED`:
      // return Object.assign({}, state, { loading_list: false, list: payload.data });
      return { ...state, loading_list: false, list: payload.data };
    case `${SET_PAIRINGS}_REJECTED`:
      // return Object.assign({}, state, { loading_list: false, error: payload.error });
      return { ...state, loading_list: false, error: payload.error };
    case `${SET_PAIRING}_PENDING`:
      // return Object.assign({}, state, { loading_pairing: true });
      return { ...state, loading_pairing: true };
    case `${SET_PAIRING}_FULFILLED`:
      // return Object.assign({}, state, { loading_pairing: false, pairing: payload.data });
      return { ...state, loading_pairing: false, pairing: payload.data };
    case `${SET_PAIRING}_REJECTED`:
      // return Object.assign({}, state, { loading_pairing: false, error: payload.error });
      return { ...state, loading_pairing: false, error: payload.error }
    default:
      return state;
  }
};
