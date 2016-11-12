import React from 'react'
import { connect } from 'react-redux'
import { fetchCandidate } from './actions'
import Card from '../kit/Card'
import SocialMedia from '../kit/SocialMedia'

class Candidate extends React.Component {
  static propTypes = {
    id: React.PropTypes.number.isRequired,
    candidate: React.PropTypes.object.isRequired,
    fetchCandidate: React.PropTypes.func.isRequired
  }

  componentWillMount () {
    const { id, fetchCandidate } = this.props
    fetchCandidate(id)
  }

  componentWillReceiveProps (nextProps) {
    const { id, fetchCandidate } = nextProps
    if (this.props.id !== id) {
      fetchCandidate(id)
    }
  }

  render () {
    const { candidate } = this.props

    return (
      <div>
        <h2>
          {candidate.full_name} ({candidate.alias_name})
        </h2>
        <Card style={{ margin: '10px auto' }}>
          <div className="uk-grid">
            <div className="uk-width-1-3">
              <img alt={candidate.alias_name} src={candidate.photo_url} />
            </div>
            <div className="uk-width-1-3">
              <dl style={{ lineHeight: '26px' }}>
                <dt>Nama lengkap</dt>
                <dd>{candidate.full_name}</dd>
                <dt>Tempat, tanggal lahir</dt>
                <dd>{candidate.date_of_birth}, {candidate.place_of_birth}</dd>
                <dt>Agama</dt>
                <dd>{candidate.religion}</dd>
                <dt>Website</dt>
                <dd><a href={candidate.website_url} target="_blank">{candidate.website_url}</a></dd>
              </dl>
            </div>
            <div className="uk-width-1-3">
              <SocialMedia
                instagram={candidate.instagram_username}
                twitter={candidate.twitter_username}
                facebook={candidate.fbpage_username}
                style={{ float: 'right' }} />
            </div>
          </div>
        </Card>
        <br />
      </div>
    )
  }
}

const mapStateProps = (state) => ({
  candidate: state.candidates.candidate
})

export default connect(mapStateProps, { fetchCandidate })(Candidate)
