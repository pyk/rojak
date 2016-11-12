import React from 'react'
import { connect } from 'react-redux'
import { createSelector } from 'reselect'

import Candidate from '../candidate/Candidate'
import Media from '../media/Media'

import { fetchCandidates } from '../candidate/actions'
import { fetchMedias } from '../media/actions'

class SearchEngine extends React.Component {
  static propTypes = {
    keyword: React.PropTypes.string.isRequired,
    candidate: React.PropTypes.object,
    media: React.PropTypes.object,
    fetchCandidates: React.PropTypes.func.isRequired,
    fetchMedias: React.PropTypes.func.isRequired
  }

  componentWillMount () {
    this.props.fetchCandidates()
    this.props.fetchMedias()
  }

  render () {
    const { keyword, candidate, media } = this.props

    if (candidate) {
      return <Candidate id={candidate.id} />
    }

    if (media) {
      return <Media id={media.id} />
    }

    return (
      <div>
        Maaf, kami tidak bisa menemukan pencarian dengan kata kunci {keyword}
      </div>
    )
  }
}

const getCandidates = (state) => (state.candidates.list)
const getMedias = (state) => (state.medias.list)
const getKeyword = (state) => (state.root.keyword.trim())

const getCandidateByKeyword = createSelector([ getKeyword, getCandidates ], (keyword, candidates) => {
  const regex = new RegExp(`(${keyword.toLowerCase()})`, 'g')

  return candidates.find((candidate) => {
    const keywords = `${candidate.full_name.toLowerCase()} ${candidate.alias_name.toLowerCase()}`
    return regex.test(keywords)
  })
})

const getMediaByKeyword = createSelector([ getKeyword, getMedias ], (keyword, medias) => {
  const regex = new RegExp(`(${keyword.toLowerCase()})`, 'g')

  return medias.find((media) => {
    const keywords = media.name.toLowerCase()
    return regex.test(keywords)
  })
})

const mapStateToProps = (state) => ({
  keyword: state.root.keyword,
  candidate: getCandidateByKeyword(state),
  media: getMediaByKeyword(state)
})

export default connect(mapStateToProps, { fetchCandidates, fetchMedias })(SearchEngine)
