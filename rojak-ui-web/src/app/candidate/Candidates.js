import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router'
import SimpleList from '../kit/SimpleList'
import { fetchCandidates } from '../candidate/actions'

class Candidates extends React.Component {
  static propTypes = {
    candidates: React.PropTypes.object,
    fetchCandidates: React.PropTypes.func.isRequired
  }

  componentWillMount () {
    this.props.fetchCandidates()
  }

  getCandidatList () {
    const { candidates } = this.props
    return candidates.list.map((candidate, index) => (
      <tr key={`candidate-${index}`}>
        <td>
          <Link to={`/search/${candidate.alias_name.toLowerCase()}`}>
            <span>{candidate.alias_name} ({candidate.full_name}) </span> →
          </Link>
        </td>
      </tr>
    ))
  }

  render () {
    return (
      <div>
        <h2>Kandidat</h2>
        <SimpleList>
          <thead>
            <tr>
              <th>Nama</th>
            </tr>
          </thead>
          <tbody>
            {this.getCandidatList()}
          </tbody>
        </SimpleList>
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  candidates: state.candidates
})

export default connect(mapStateToProps, { fetchCandidates })(Candidates)
