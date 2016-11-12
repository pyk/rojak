import React from 'react'
import ResultGateway from './ResultGateway'
import SearchEngine from '../utils/SearchEngine'

const DefaultResult = () => {
  return (
    <ResultGateway showIn={[/./]} hideIn={[/^(media)$/, /^(kandidat)$/, /^(pasangan)$/]}>
      <SearchEngine />
    </ResultGateway>
  )
}

export default DefaultResult
