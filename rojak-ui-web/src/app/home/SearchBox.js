import React from 'react'
import { connect } from 'react-redux'
import { setKeyword } from '../root/actions'
import Card from '../kit/Card';
import SearchForm from './SearchForm';
import SearchCategory from './SearchCategory'
import styles from './search-box.css'
import rojak from '../../assets/images/rojak-black.svg';

class SearchBox extends React.Component {
  static propTypes = {
    keyword: React.PropTypes.string.isRequired,
    expanded: React.PropTypes.bool.isRequired,
    setKeyword: React.PropTypes.func.isRequired
  }

  get handleKeywordChange () {
    const { setKeyword } = this.props
    return (keyword) => {
      setKeyword(keyword)
    }
  }

  get searchBoxCardStyle () {
    const { expanded } = this.props
    if (!expanded) return { maxWidth: '800px', margin: 'auto' }

    return {
      position: 'fixed',
      top: 0,
      left: 0,
      bottom: 0,
      margin: 0,
      padding: 0,
      maxWidth: '400px',
      zIndex: '1'
    }
  }

  render () {
    const { keyword, expanded } = this.props
    return (
      <div className={styles.searchBox} style={{ textAlign: 'center' }}>
        <ExpandedHidden expanded={expanded}>
          <h1>Halo!</h1>
        </ExpandedHidden>
        <Card style={this.searchBoxCardStyle} className={styles.searchBoxCard}>
          <SearchBoxHeader expanded={expanded} />

          <SearchForm keyword={keyword} onKeywordChange={this.handleKeywordChange} />

          <div className={styles.searchCategories}>
            <SearchCategory keyword="media: " onClick={this.handleKeywordChange}>Media</SearchCategory>
            <SearchCategory keyword="pasangan: " onClick={this.handleKeywordChange}>Pasangan</SearchCategory>
            <SearchCategory keyword="kandidat: " onClick={this.handleKeywordChange}>Kandidat</SearchCategory>
          </div>

          <ExpandedHidden expanded={expanded}>
            <div className={`uk-width-8-10 uk-push-1-10 uk-text-left ${styles.description}`}>
              <p>
                <strong>Pada kotak pencarian di atas</strong>, masukkan kata kunci dari media, berita, atau kandidat yang ingin ditelusuri.
              </p>
              <p>
                Anda juga dapat mencari menggunakan url dari sebuah media online
              </p>
            </div>
          </ExpandedHidden>
        </Card>
        <ExpandedHidden expanded={expanded}>
          <footer style={{ marginTop: '30px', marginBottom: '15px' }} >
            <p>
              Project <strong>Rojak</strong> adalah sebuah non-profit project untuk
              membantu jalannya Pilkada DKI Jakarta 2017 dalam hal pengawasan media daring.
            </p>
          </footer>
        </ExpandedHidden>
      </div>
    )
  }
}

function SearchBoxHeader ({ expanded }) {
  if (expanded) {
    return <img className={styles.rojakLogo} src={rojak} alt="rojak" style={{ marginBottom: '20px', maxWidth: '150px' }} />
  }
  return (
    <div>
      <img className={styles.rojakLogo} src={rojak} alt="rojak" />
      <p className={styles.rojakDescription}>
        Saya Rojak, saya akan membantu Anda memilih kandidat Pilkada dengan bijak <br />
        secara objektif tanpa terpengaruh media bayaran.
      </p>
      <br />
    </div>
  )
}

function ExpandedHidden ({ children, expanded }) {
  if (expanded) return null
  return children
}

const mapStateToProps = (state) => ({
  keyword: state.root.keyword,
  expanded: state.root.expanded
})

export default connect(mapStateToProps, { setKeyword })(SearchBox)
