import { ajax } from '../services'

export const SET_PAIRINGS = 'SET_PAIRINGS'
export const SET_PAIRING = 'SET_PAIRING'

export const setPairings = pairings => ({
  type: SET_PAIRINGS,
  payload: { pairings }
})

export const setPairing = pairing => ({
  type: SET_PAIRING,
  payload: { pairing }
})

export const fetchPairings = () => dispatch => {
  ajax.get('pairings').then((res) => {
    dispatch(setPairings(res.data))
  })
}

export const fetchPairing = id => dispatch => {
  ajax.get(`pairings/${id}?embed[]=overall_sentiments&embed[]=sentiments_by_media`).then((res) => {
    dispatch(setPairing(res.data))
  })
}

