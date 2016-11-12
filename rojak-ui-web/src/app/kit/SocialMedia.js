import React from 'react'
import { Link } from 'react-router'
import styles from './SocialMedia.css'

class SocialMedia extends React.Component {
  static propTypes = {
    instagram: React.PropTypes.string,
    twitter: React.PropTypes.string,
    facebook: React.PropTypes.string,
    style: React.PropTypes.object
  }

  render () {
    const { instagram, twitter, facebook, style } = this.props

    return (
      <div className={styles.socialMedia} style={style}>
        <Link
          to={`//instagram.com/${instagram}`}
          target="_blank"
          className={`ion-social-instagram-outline ${styles.socialIcon}`} />
        <Link
          to={`//twitter.com/${twitter}`}
          target="_blank"
          className={`ion-social-twitter-outline ${styles.socialIcon}`}
          />
        <Link
          to={`//facebook.com/${facebook}`}
          target="_blank"
          className={`ion-social-facebook-outline ${styles.socialIcon}`}
          />
      </div>
    )
  }
}

export default SocialMedia
