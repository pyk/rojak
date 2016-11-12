import { ajax } from '../services'

export const SET_CANDIDATES = 'SET_CANDIDATES'
export const SET_CANDIDATE = 'SET_CANDIDATE'

export function setCandidates (candidates) {
  return { type: SET_CANDIDATES, payload: { candidates } }
}

export function setCandidate (candidate) {
  return { type: SET_CANDIDATE, payload: { candidate } }
}

export function fetchCandidates () {
  return (dispatch) => (
    ajax.get('candidates').then((res) => {
      dispatch(setCandidates(res.data))
    })
  )
}

export function fetchCandidate (id) {
  return (dispatch) => (
    ajax.get(`candidates/${id}?embed[]=pairing`).then((res) => {
      dispatch(setCandidate(res.data))
    })
  )
}
