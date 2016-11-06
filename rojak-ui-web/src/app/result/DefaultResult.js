import React from 'react'
import ResultGateway from './ResultGateway'
import styles from './result.css'

const DefaultResult = () => {
  return (
    <ResultGateway hideIn={[/media: /, /kandidat: /, /pasangan: /]}>
      <div className={styles.resultWrapper}>
      THIS IS DEFAULT RESULT
        <div className="uk-grid-collapse" style={{ paddingTop: '20px' }}>
          <img className="uk-width-1-5 uk-thumbnail" src="http://placehold.it/100x100"/>
        </div>
      </div>
    </ResultGateway>
  )
}

export default DefaultResult
