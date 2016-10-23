import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'

const MediaResult = () => {
  return (
    <ResultGateway showIn={['media']}>
      <div className={styles.resultWrapper}>
        THIS IS MEDIA
      </div>
    </ResultGateway>
  )
}

export default MediaResult
