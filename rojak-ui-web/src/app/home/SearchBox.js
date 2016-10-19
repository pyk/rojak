import React from 'react'
import styles from './search-box.css'
import SearchCategory from './SearchCategory'

class SearchBox extends React.Component {
  static propTypes = {
    router: React.PropTypes.object.isRequired
  }

  constructor (props) {
    super(props)
    this.state = { keyword: '' }
    this.throttleKeyChange = null
  }

  get handleKeywordChange () {
    return (e) => {
      this.setState({ keyword: e.target.value }, this.updateRoute)
    }
  }

  get handleCategoryClick () {
    return (keyword) => {
      this.setState({ keyword }, this.updateRoute)
    }
  }

  updateRoute () {
    const { keyword } = this.state
    if (this.throttleKeyChange) {
      clearTimeout(this.throttleKeyChange)
    }
    this.throttleKeyChange = setTimeout(() => {
      this.props.router.push({
        pathname: `/search/${keyword}`
      })
    }, 300)
  }

  render () {
    const { keyword } = this.state
    return (
      <div>
        <form className="uk-form">
          <input
            type="text"
            placeholder="cari dari nama kandidat, pasangan, atau media"
            className="uk-form-large uk-form-width-large"
            value={keyword}
            onChange={this.handleKeywordChange} />
        </form>
        <div className={styles.searchCategories}>
          <SearchCategory keyword="media" onClick={this.handleCategoryClick}>Media</SearchCategory>
          <SearchCategory keyword="pasangan" onClick={this.handleCategoryClick}>Pasangan</SearchCategory>
          <SearchCategory keyword="kandidat" onClick={this.handleCategoryClick}>Kandidat</SearchCategory>
        </div>
      </div>
    )
  }
}

export default SearchBox
