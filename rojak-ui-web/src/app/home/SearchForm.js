import React from 'react'

class SearchForm extends React.Component {
  static propTypes = {
    keyword: React.PropTypes.string,
    onKeywordChange: React.PropTypes.func.isRequired
  }

  constructor (props) {
    super(props)
    this.state = { keyword: '' }
    this.throttleKeyChange = null
  }

  componentDidMount () {
    const { keyword } = this.props
    keyword && this.setState({ keyword })
  }

  componentWillReceiveProps (nextProps) {
    const { keyword } = this.props
    if (nextProps.keyword !== keyword) {
      this.setState({ keyword: nextProps.keyword })
    }
  }

  get handleKeywordChange () {
    const { onKeywordChange } = this.props
    return (e) => {
      const keyword = e.target.value

      this.setState({ keyword })

      if (this.throttleKeyChange) {
        clearTimeout(this.throttleKeyChange)
      }
      this.throttleKeyChange = setTimeout(() => {
        onKeywordChange(keyword)
      }, 300)
    }
  }

  render () {
    const { keyword } = this.state
    return (
      <form className="uk-form">
        <input
          type="text"
          placeholder="cari dari nama kandidat, pasangan, atau media"
          className="uk-form-large uk-form-width-large"
          value={keyword}
          onChange={this.handleKeywordChange}
          style={{ padding: '10px 15px', borderRadius: '0px' }} />
      </form>
    )
  }
}

export default SearchForm
