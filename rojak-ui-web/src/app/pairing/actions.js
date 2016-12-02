import { ajax } from '../services';

export const SET_PAIRINGS = 'SET_PAIRINGS';
export const SET_PAIRING = 'SET_PAIRING';

export const fetchPairings = () => ({
  type: SET_PAIRINGS,
  payload: ajax.get('pairings')
});

export const fetchPairing = (id) => ({
  type: SET_PAIRING,
  payload: ajax.get(`pairings/${id}?embed[]=overall_sentiments&embed[]=sentiments_by_media`)
});
