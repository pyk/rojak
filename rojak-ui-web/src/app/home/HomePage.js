import React, { Component } from 'react';
import Link from 'react-router/lib/Link';
import withRouter from 'react-router/lib/withRouter';
import rojak from '../../assets/images/rojak-black.svg';
import Card from '../kit/Card';
import Medias from './Medias';
import Candidates from './Candidates';
import styles from './HomePage.css';
import SearchBox from './SearchBox';

class HomePage extends Component {

    render() {
        const { router } = this.props

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
                        <SearchBox router={router} />
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
