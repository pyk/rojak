import React from 'react'
import SimpleList from '../kit/SimpleList'

class PairingSentimentBox extends React.Component {
  static propTypes = {
    news: React.PropTypes.array
  }

  static defaultProps = {
    news: []
  }

  render () {
    const { news } = this.props

    const newsItem = news.map((newsItem, index) => (
      <NewsItem key={`news-item-${index}`} newsItem={newsItem} />
    ))

    return (
      <div>
        <h3>Latest News</h3>
        <SimpleList style={{ fontSize: '14px' }}>
          <thead>
            <tr>
              <th>News</th>
            </tr>
          </thead>
          <tbody>
            {newsItem}
          </tbody>
        </SimpleList>
      </div>
    )
  }
}

const NewsItem = ({ newsItem }) => (
  <tr>
    <td>
      {newsItem.title}
      <a
        href={newsItem.url}
        target="_blank"
        style={{ marginLeft: '7px', marginTop: '1px', fontWeight: '600', color: 'green' }}>
        <span className="uk-icon-external-link" />
      </a>
    </td>
  </tr>
)

NewsItem.propTypes = {
  newsItem: React.PropTypes.object
}

export default PairingSentimentBox
