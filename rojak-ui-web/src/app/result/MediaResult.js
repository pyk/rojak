import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'

const MediaResult = () => {
  return (
    <ResultGateway showIn={[/^(media)$/]}>
      THIS IS MEDIA
    </ResultGateway>
  )
}

export default MediaResult
