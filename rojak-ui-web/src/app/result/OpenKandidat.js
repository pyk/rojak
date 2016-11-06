import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'
import { connect } from 'react-redux'
import { Link } from 'react-router'
import Card from '../kit/Card';

class OpenKandidat extends React.Component {
  static propTypes = {
    candidate: React.PropTypes.object.isRequired,
  }

  static contextTypes = {
    rojakClient: React.PropTypes.object,
  }

  loadSentiments(candidateId) {
    this
      .context
      .rojakClient
      .getSentimentsOfCandidate(
        candidateId
      ).then(sentiments => {
        this.props.setSentimentsOfCandidateId(
          sentiments,
          candidateId
        );
      });
  }

  componentDidMount() {
    this.loadSentiments(this.props.candidate.id)
  }

  componentWillUpdate(nextProps) {
    if (nextProps.candidate.id && this.props.candidate.id !== nextProps.candidate.id) {
      this.loadSentiments(nextProps.candidate.id);
    }
  }

  render() {
    const sentimentsOfCandidate = this
      .props
      .sentiments
      .filter(sentiment => sentiment.candidateId === this.props.candidate.id);
    return (
      <ResultGateway hideIn={[/^(kandidat: )/]}  showIn={[/^(buka kandidat: )/]}>
        <div className={styles.resultWrapper}>
          <h1 className={styles.resultHeader}>
            {this.props.candidate.full_name} ({this.props.candidate.alias_name})
          </h1>
          <Card>
            <div className="uk-grid">
              <div className="uk-width-1-3">
                <img alt={this.props.candidate.alias_name} src={this.props.candidate.photo_url} />
              </div>
              <div className="uk-width-1-3">
                <dl>
                  <dt>Nama lengkap</dt>
                  <dd>{this.props.candidate.full_name}</dd>
                  <dt>Tempat, tanggal lahir</dt>
                  <dd>{this.props.candidate.date_of_birth}, {this.props.candidate.place_of_birth}</dd>
                  <dt>Agama</dt>
                  <dd>{this.props.candidate.religion}</dd>
                  <dt>Website</dt>
                  <dd>{this.props.candidate.website_url}</dd>
                </dl>
              </div>
              <div className="uk-width-1-3">
                <div className={styles.socialMedia}>
                  <Link
                    to={`//instagram.com/${this.props.candidate.instagram_username}`}
                    target="_blank"
                    className={`ion-social-instagram-outline ${styles.socialIcon}`}
                  />
                  <Link
                    to={`//twitter.com/${this.props.candidate.twitter_username}`}
                    target="_blank"
                    className={`ion-social-twitter-outline ${styles.socialIcon}`}
                  />
                  <Link
                    to={`//facebook.com/${this.props.candidate.fbpage_username}`}
                    target="_blank"
                    className={`ion-social-facebook-outline ${styles.socialIcon}`}
                  />
                </div>
              </div>
            </div>
          </Card>
          <br />
          <table className="uk-table">
            <thead>
              <tr>
                  <th>Media</th>
                  <th>Positif</th>
                  <th>Negatif</th>
                  <th>Netral</th>
              </tr>
            </thead>
            <tbody>
              {sentimentsOfCandidate.map(sentiment => (
                <tr key={sentiment.id} className={styles.resultRow}>
                  <td className={styles.resultCell}>
                    <span className={styles.resultCell}>{sentiment.name}  </span>
                    <Link className={styles.resultCell} to={sentiment.website_url} target="_blank">
                      <span className="ion-android-open" />
                    </Link>
                  </td>
                  <td>{sentiment.sentiments.positive * 100} % <span className="ion-happy-outline" /></td>
                  <td>{sentiment.sentiments.negative * 100} % <span className="ion-sad-outline" /></td>
                  <td>{sentiment.sentiments.neutral * 100} % <span className="ion-drag" /></td>
                </tr>
              ))}
            </tbody>
          </table>
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
  sentiments: state.sentiments,
});

const mapDispatchToProps = (dispatch) => ({
  setSentimentsOfCandidateId: (sentiments, candidateId) => {
    dispatch({
      type: 'SET_SENTIMENTS_OF_CANDIDATE_ID',
      payload: {
        sentiments,
        candidateId,
      },
    })
  },
})

export default connect(mapStateToProps, mapDispatchToProps)(OpenKandidat)
