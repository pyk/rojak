import React from 'react'
import { connect } from 'react-redux'

class ResultGateway extends React.Component {
  static propTypes = {
    showIn: React.PropTypes.array,
    hideIn: React.PropTypes.array,
    keyword: React.PropTypes.string.isRequired,
    children: React.PropTypes.any.isRequired
  }

  get managedChildren () {
    const { keyword, children, showIn, hideIn } = this.props

    if (!keyword || (showIn && showIn.indexOf(keyword) === -1) || (hideIn && hideIn.indexOf(keyword) > -1)) {
      return null
    }

    return children
  }

  render () {
    return this.managedChildren
  }
}

const mapStateToProps = (state) => ({
  keyword: state.root.keyword
})

export default connect(mapStateToProps)(ResultGateway)
