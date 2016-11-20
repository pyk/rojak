import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router'
import { fetchPairing } from './actions'
import Card from '../kit/Card'
import SimpleList from '../kit/SimpleList'
import SocialMedia from '../kit/SocialMedia'

class Pairing extends React.Component {
  static propTypes = {
    id: React.PropTypes.number.isRequired,
    pairing: React.PropTypes.object.isRequired,
    fetchPairing: React.PropTypes.func.isRequired
  }

  componentWillMount () {
    const { id, fetchPairing } = this.props
    fetchPairing(id)
  }

  componentWillReceiveProps (nextProps) {
    const { id, fetchPairing } = nextProps
    if (this.props.id !== id) {
      fetchPairing(id)
    }
  }

  render () {
    const { pairing } = this.props
    const sentiments = this.props.pairing &&
      this.props.pairing.sentiments_by_media &&
      this.props.pairing.sentiments_by_media.map(sentiment => (
        <tr key={sentiment.media.id}>
          <td>
            <Link to={`/search/${sentiment.media.name}`}>
              <span>{sentiment.media.name}</span> →
            </Link>
          </td>
          <td>
            {sentiment.positive_news_count || 0}
          </td>
          <td>
            {sentiment.negative_news_count || 0}
          </td>
        </tr>
      ))

    return (
      <div>
        <Card style={{ margin: '10px auto' }}>
          <div className="uk-grid">
            <div className="uk-width-1-3">
              <img alt={pairing.name} src={pairing.logo_url} />
            </div>
            <div className="uk-width-1-3">
              <dl style={{ lineHeight: '26px' }}>
                <dt>Pasangan</dt>
                <dd>{pairing.name}</dd>
                <dt>Slogan</dt>
                <dd>{pairing.slogan}</dd>
                <dt>Website</dt>
                <dd><a href={pairing.website_url} target="_blank">{pairing.website_url}</a></dd>
                <dt>Sentimen Positif</dt>
                <dd>{pairing.overall_sentiments && pairing.overall_sentiments.positive_news_count}</dd>
                <dt>Sentimen Negatif</dt>
                <dd>{pairing.overall_sentiments && pairing.overall_sentiments.negative_news_count}</dd>
              </dl>
            </div>
            <div className="uk-width-1-3">
              <SocialMedia
                instagram={pairing.instagram_username}
                twitter={pairing.twitter_username}
                facebook={pairing.fbpage_username}
                style={{ float: 'right' }} />
            </div>
          </div>
        </Card>
        <Card style={{ margin: '10px auto' }}>
          <h2>Sentimen Media</h2>
          <SimpleList>
            <thead>
              <tr>
                <th>Nama</th>
                <th>Berita Positif</th>
                <th>Berita Negatif</th>
              </tr>
            </thead>
            <tbody>
              {sentiments}
            </tbody>
          </SimpleList>
        </Card>
        <br />
      </div>
    )
  }
}

const mapStateProps = state => ({
  pairing: state.pairings.pairing
})

export default connect(mapStateProps, { fetchPairing })(Pairing)
