import React from 'react'
import ResultGateway from './ResultGateway'
import Pairings from '../pairing/Pairings'

const PasanganResult = () => {
  return (
    <ResultGateway showIn={[/^(pasangan)$/]}>
      <Pairings />
    </ResultGateway>
  )
}

export default PasanganResult
