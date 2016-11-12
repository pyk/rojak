import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'

const PasanganResult = () => {
  return (
    <ResultGateway showIn={[/^(pasangan)$/]}>
      THIS IS PASANGAN RESULT
    </ResultGateway>
  )
}

export default PasanganResult
