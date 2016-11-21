import React from 'react'
import { Link } from 'react-router'
import { connect } from 'react-redux'
import SimpleList from '../kit/SimpleList'
import { fetchPairings } from './actions'

class Pairings extends React.Component {
  static propTypes = {
    pairings: React.PropTypes.object,
    fetchPairings: React.PropTypes.func.isRequired
  }

  componentWillMount () {
    this.props.fetchPairings()
  }

  render () {
    const pairings = this.props.pairings.list.map(pair => (
      <tr key={pair.id}>
        <td>
          <Link to={`/search/${pair.name}`}>
            <span>{pair.name}</span> →
          </Link>
        </td>
      </tr>
    ))
    return (
      <div>
        <h2>Pasangan</h2>
        <SimpleList>
          <thead>
            <tr>
              <th>Nama</th>
            </tr>
          </thead>
          <tbody>
            {pairings}
          </tbody>
        </SimpleList>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  pairings: state.pairings
})

export default connect(mapStateToProps, { fetchPairings })(Pairings)
