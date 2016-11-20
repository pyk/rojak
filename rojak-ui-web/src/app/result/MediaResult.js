import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'

const MediaResult = () => {
  return (
    <ResultGateway showIn={[/^(media)$/]}>
      <p>THIS IS MEDIA</p>
    </ResultGateway>
  )
}

export default MediaResult
