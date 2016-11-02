import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'
import { connect } from 'react-redux'
import { Link } from 'react-router'

class OpenKandidat extends React.Component {
  static propTypes = {
    candidate: React.PropTypes.object.isRequired,
  }

  render() {
    return (
      <ResultGateway hideIn={[/^(kandidat: )/]}  showIn={[/^(buka kandidat: )/]}>
        <div className={styles.resultWrapper}>
          <h1 className={styles.resultHeader}>
            {this.props.candidate.full_name} ({this.props.candidate.alias_name})
          </h1>
        </div>
      </ResultGateway>
    )
  }
}

const getCandidateDetailFromKeyword = (keyword, candidates, sentiments) => {
  let candidateKeyword = keyword.split(/buka kandidat: /g)[1];
  if (candidateKeyword) {
    candidateKeyword = candidateKeyword.toLowerCase();
    return candidates.find(candidate => (
      candidate.alias_name.toLowerCase().includes(candidateKeyword) ||
      candidate.full_name.toLowerCase().includes(candidateKeyword)
    ));
  }

  return {};
}

const mapStateToProps = (state) => ({
  candidate: getCandidateDetailFromKeyword(
      state.root.keyword,
      state.candidates,
      state.sentiments),
}) 

export default connect(mapStateToProps)(OpenKandidat)
