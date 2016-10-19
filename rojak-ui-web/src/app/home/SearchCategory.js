import React from 'react'

class SearchCategory extends React.Component {
  static propTypes = {
    keyword: React.PropTypes.string,
    children: React.PropTypes.string,
    onClick: React.PropTypes.func
  }

  static defaultProps = {
    keyword: '',
    onClick: (keyword) => { console.debug(`${keyword} category is clicked`) }
  }

  get handleClick () {
    const { onClick, keyword } = this.props
    return () => {
      onClick(keyword)
    }
  }

  render () {
    const { children } = this.props
    return (
      <div onClick={this.handleClick}>{children}</div>
    )
  }
}

export default SearchCategory
