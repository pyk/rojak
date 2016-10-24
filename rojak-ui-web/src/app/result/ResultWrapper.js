import React from 'react'
import { connect } from 'react-redux'
import styles from './result.css'

class ResultWrapper extends React.Component {
  static propTypes = {
    children: React.PropTypes.any.isRequired,
    expanded: React.PropTypes.bool.isRequired
  }

  get managedChildren () {
    const { children, expanded } = this.props

    if (!expanded) return null

    return children
  }

  render () {
    const { expanded } = this.props
    return (
      <div className={expanded ? styles.resultWrapper : ''}>
        {this.managedChildren}
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  expanded: state.root.expanded
})

export default connect(mapStateToProps)(ResultWrapper)
