import React from 'react'
import { connect } from 'react-redux'
import { fetchMedia } from './actions'
import Card from '../kit/Card'
import SocialMedia from '../kit/SocialMedia'
import PairingSentiments from './PairingSentiments'
import LatestNews from './LatestNews'

class Media extends React.Component {
  static propTypes = {
    id: React.PropTypes.number.isRequired,
    media: React.PropTypes.object.isRequired,
    fetchMedia: React.PropTypes.func.isRequired
  }

  componentWillMount () {
    const { id, fetchMedia } = this.props
    fetchMedia(id)
  }

  componentWillReceiveProps (nextProps) {
    const { id, fetchMedia } = nextProps
    if (this.props.id !== id) {
      fetchMedia(id)
    }
  }

  render () {
    const { media } = this.props

    return (
      <div>
        <div>
          <img alt={media.name} src={media.logo_url} style={{ maxWidth: '200px', marginBottom: '15px' }} />
          <SocialMedia
            instagram={media.instagram_username}
            twitter={media.twitter_username}
            facebook={media.fbpage_username}
            style={{ float: 'right' }} />
        </div>
        <Card style={{ margin: '10px auto' }}>
          <PairingSentiments sentiments={media.sentiments_on_pairings} />
        </Card>
        <Card style={{ margin: '10px auto' }}>
          <LatestNews news={media.latest_news} />
        </Card>
        <br />
      </div>
    )
  }
}

const mapStateProps = (state) => ({
  media: state.medias.media
})

export default connect(mapStateProps, { fetchMedia })(Media)
