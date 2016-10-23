export const SET_KEYWORD = 'ROOT.SET_KEYWORD'
export const SET_SCREEN_EXPANDED = 'ROOT.SET_SCREEN_EXPANDED'

export function setKeyword (keyword) {
  return { type: SET_KEYWORD, keyword }
}

export function setScreenExpanded (expanded) {
  return { type: SET_SCREEN_EXPANDED, expanded }
}
