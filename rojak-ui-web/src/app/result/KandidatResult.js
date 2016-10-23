import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'

const KandidatResult = () => {
  return (
    <ResultGateway showIn={['kandidat']}>
      <div className={styles.resultWrapper}>
        THIS IS KANDIDAT
      </div>
    </ResultGateway>
  )
}

export default KandidatResult
