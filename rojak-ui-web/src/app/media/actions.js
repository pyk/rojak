import { ajax } from '../services'

export const SET_MEDIAS = 'SET_MEDIAS'
export const SET_MEDIA = 'SET_MEDIA'

export function setMedias (medias) {
  return { type: SET_MEDIAS, payload: { medias } }
}
export function setMedia (media) {
  return { type: SET_MEDIA, payload: { media } }
}

export function fetchMedias () {
  return (dispatch) => (
    ajax.get('/media?limit=20').then((res) => {
      dispatch(setMedias(res.data))
    })
  )
}

export function fetchMedia (id) {
  return (dispatch) => (
    ajax.get(`/media/${id}?embed[]=sentiments_on_pairings&embed[]=latest_news`).then((res) => {
      dispatch(setMedia(res.data))
    })
  )
}
