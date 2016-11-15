import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router'

import ResultGateway from '../result/ResultGateway'
import Candidates from '../candidate/Candidates'
import styles from './result.css'

class KandidatResult extends React.Component {
  render() {
    return (
      <ResultGateway showIn={[/^(kandidat)$/]}>
        <Candidates />
      </ResultGateway>
    )
  }
}

/*
const getCandidatesFromKeyword = (keyword, candidates) => {
  let candidateKeyword = keyword.split(/kandidat: /g)[1];
  if (candidateKeyword) {
    candidateKeyword = candidateKeyword.toLowerCase();
    return candidates.filter(candidate => (
      candidate.alias_name.toLowerCase().includes(candidateKeyword) ||
      candidate.full_name.toLowerCase().includes(candidateKeyword)
    ));
  }

  return candidates;
}

const mapStateToProps = (state) => ({
  searchResults: getCandidatesFromKeyword(state.root.keyword, state.candidates),
})

export default connect(mapStateToProps)(KandidatResult)
 */
export default KandidatResult
