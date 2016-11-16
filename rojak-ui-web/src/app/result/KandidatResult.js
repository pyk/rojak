import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router'

import ResultGateway from '../result/ResultGateway'
import Candidates from '../candidate/Candidates'
import styles from './result.css'

class KandidatResult extends React.Component {
  render() {
    return (
      <ResultGateway showIn={[/^(kandidat)$/]}>
        <Candidates />
      </ResultGateway>
    )
  }
}

export default KandidatResult
