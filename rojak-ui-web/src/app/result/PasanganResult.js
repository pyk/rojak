import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'

const PasanganResult = () => {
  return (
    <ResultGateway showIn={[/^(pasangan: )/]}>
      <div className={styles.resultWrapper}>
        THIS IS PASANGAN RESULT
      </div>
    </ResultGateway>
  )
}

export default PasanganResult
