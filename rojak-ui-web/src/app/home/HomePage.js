import React, { Component } from 'react';
import Link from 'react-router/lib/Link';
import withRouter from 'react-router/lib/withRouter';
import rojak from '../../assets/images/rojak-black.svg';
import Card from '../kit/Card';
import Medias from './Medias';
import Candidates from './Candidates';
import styles from './HomePage.css';

class HomePage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            keyword: ''
        };

        this.onKeywordChanged = this.onKeywordChanged.bind(this);
    }

    onKeywordChanged(e) {
        this.setState({
            keyword: e.target.value
        }, () => {
            const { keyword } = this.state;

            this.props.router.push({
                pathname: `/browse/?keyword=${keyword}`
            });
        });
    }

    render() {
        const { keyword } = this.state;

        return (
            <div id="HomePage" className={`uk-grid ${styles.homepageWrapper}`}>
                <div className="uk-width-1-10" />
                <div className="uk-width-8-10">
                    <h1 className={styles.halo}>Halo!</h1>
                    <Card>
                        <img className={styles.rojakLogo} src={rojak} alt="rojak" />
                        <p className={styles.rojakDescription}>
                            Saya Rojak, saya akan membantu Anda memilih kandidat Pilkada dengan bijak
                            secara objektif tanpa terpengaruh media bayaran.
                        </p>
                        <br />
                        <form className="uk-form">
                            <input
                                type="text"
                                placeholder="cari dari nama kandidat, pasangan, atau media"
                                className="uk-form-large uk-form-width-large"
                                value={keyword}
                                onChange={this.onKeywordChanged} />
                        </form>
                        <div className={styles.categoryContainer}>
                            <Link to="/browse/?keyword=media" className={styles.category}>Media</Link>
                            <Link to="/browse/?keyword=pasangan" className={styles.category}>Pasangan</Link>
                            <Link to="/browse/?keyword=kandidat" className={styles.category}>Kandidat</Link>
                        </div>
                        <div className={styles.description}>
                            <div>
                                <b>Pada kotak pencarian di atas</b>, masukkan kata kunci dari media, berita, atau kandidat yang ingin ditelusuri.
                            </div>
                            <div className={styles.subDescription}>
                                Anda juga dapat mencari menggunakan url dari sebuah media online
                            </div>
                        </div>
                    </Card>
                    <p>
                        Project <b>Rojak</b> adalah sebuah non-profit project untuk
                        membantu jalannya Pilkada DKI Jakarta 2017 dalam hal pengawasan media daring.
                    </p>
                </div>
                <div className="uk-width-1-10" />
            </div>
        );
    }
}

export default withRouter(HomePage);
