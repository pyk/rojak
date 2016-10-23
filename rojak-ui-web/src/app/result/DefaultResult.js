import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'

const DefaultResult = () => {
  return (
    <ResultGateway hideIn={['media', 'kandidat', 'pasangan']}>
      <div className={styles.resultWrapper}>
        THIS IS DEFAULT RESULT
      </div>
    </ResultGateway>
  )
}

export default DefaultResult
