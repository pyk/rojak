import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'
import { connect } from 'react-redux'
import { Link } from 'react-router'

class KandidatResult extends React.Component {
  static propTypes = {
    searchResults: React.PropTypes.array.isRequired,
  }

  render() {
    return (
      <ResultGateway showIn={[/^(kandidat: )/]} hideIn={[/^(buka kandidat: )/]}>
        <div className={styles.resultWrapper}>
          <h1 className={styles.resultHeader}>Kandidat</h1>
          <table className="uk-table">
            <thead>
              <tr>
                  <th>Nama</th>
              </tr>
            </thead>
            <tbody>
              {this.props.searchResults.map(result => (
                <tr key={result.full_name} className={styles.resultRow}>
                  <td className={styles.resultCell}>
                    <span className={styles.resultCell}>{result.alias_name} ({result.full_name})  </span>
                    <Link className={styles.resultCell} to={`/search/buka kandidat: ${result.alias_name}`}>→</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ResultGateway>
    )
  }
}

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
