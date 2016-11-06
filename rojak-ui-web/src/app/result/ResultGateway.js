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
    const shouldShow = (showIn || []).find(shw => shw.test(keyword));
    const shouldHide = (hideIn || []).find(hid => hid.test(keyword));

    if (shouldHide) {
      return null;
    }

    if (shouldShow) {
      return children;
    }

    return null
  }

  render () {
    return this.managedChildren
  }
}

const mapStateToProps = (state) => ({
  keyword: state.root.keyword
})

export default connect(mapStateToProps)(ResultGateway)
