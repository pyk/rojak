import React from 'react'
import style from './SimpleList.css'

class SimpleList extends React.Component {
  static propTypes = {
    data: React.PropTypes.object,
    children: React.PropTypes.any,
    style: React.PropTypes.object
  }

  render () {
    return (
      <table className={`uk-table ${style.simpleList}`} style={this.props.style}>
        {this.props.children}
      </table>
    )
  }
}

export default SimpleList
