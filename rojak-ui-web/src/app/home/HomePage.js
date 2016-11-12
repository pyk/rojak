import React, { Component } from 'react'
import SearchBox from './SearchBox'
import { ResultWrapper, DefaultResult, MediaResult, PasanganResult, KandidatResult } from '../result'

class HomePage extends Component {
  render () {
    return (
      <div>
        <SearchBox />
        <ResultWrapper>
          <DefaultResult />
          <KandidatResult />
          <MediaResult />
          <PasanganResult />
        </ResultWrapper>
      </div>
    )
  }
}

export default HomePage
