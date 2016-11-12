import React from 'react'
import SimpleList from '../kit/SimpleList'
import styles from './PairingSentiments.css'

class PairingSentiments extends React.Component {
  static propTypes = {
    sentiments: React.PropTypes.array
  }

  static defaultProps = {
    sentiments: []
  }

  render () {
    const { sentiments } = this.props

    const sentimentItems = sentiments.map((sentiment, index) => (
      <SentimentItem key={`sentiment-${index}`} sentiment={sentiment} />
    ))

    return (
      <div>
        <h3>News Sentiments</h3>
        <SimpleList style={{ fontSize: '14px' }}>
          <thead>
            <tr>
              <th>Pasangan</th>
              <th>Positive News</th>
              <th>Negative News</th>
            </tr>
          </thead>
          <tbody>
            {sentimentItems}
          </tbody>
        </SimpleList>
      </div>
    )
  }
}

const SentimentItem = ({ sentiment }) => (
  <tr>
    <td>
      <div className={styles.iconBox}>
        <img src={sentiment.pairing.logo_url} alt={sentiment.pairing.name} />
      </div>
      {sentiment.pairing.name}
    </td>
    <td>{sentiment.positive_news_count}</td>
    <td>{sentiment.negative_news_count}</td>
  </tr>
)

SentimentItem.propTypes = {
  sentiment: React.PropTypes.object
}

export default PairingSentiments
