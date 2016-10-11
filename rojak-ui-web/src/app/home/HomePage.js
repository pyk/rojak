import React from 'react';
import rojak from '../../assets/images/rojak-black.svg';
import Card from '../kit/Card';
import Medias from './Medias';
import Candidates from './Candidates';


const styles = {
    homepageWrapper: {
        textAlign: 'center',
    },
    halo: {
        fontSize: 34,
        fontWeight: 700,
        letterSpacing: 2,
    },
    rojakLogo: {
        width: 200,
        height: 200,
        backgroundColor: '#fff',
    },
    cardWrapper: {
        padding: 20,
        margin: '20px 10px',
        borderRadius: 4,
        backgroundColor: '#fff',
        boxShadow: '0 2px 2px 0 rgba(0,0,0,0.1)',
    },
    card: {
        backgroundColor: '#fff',
        padding: 20,
    },
    learnMoreButton: {
        color: 'rgb(51, 51, 51)',
        border: '2px solid rgb(51, 51, 51)',
        backgroundColor: 'transparent',
        borderRadius: 0,
    },
};

const HomePage = () => (
    <div id="HomePage" className="uk-grid" style={styles.homepageWrapper}>
        <div className="uk-width-1-10" />
        <div className="uk-width-8-10">
            <h1 style={styles.halo}>Halo!</h1>
            <Card>
                <img style={styles.rojakLogo} src={rojak} alt="rojak" />
                <p style={{ backgroundColor: '#fff' }}>
                    Saya Rojak, saya akan membantu Anda memilih kandidat Pilkada dengan bijak
                    secara objektif tanpa terpengaruh media bayaran.
                </p>
                <br />
                <a
                    className="uk-button uk-button-large"
                    style={styles.learnMoreButton}
                    type="button"
                    href="https://github.com/pyk/rojak"
                >
                    Pelajari selengkapnya →
                </a>
            </Card>
            <div className="uk-grid">
                <div className="uk-width-1-2">
                    <Medias />
                </div>
                <div className="uk-width-1-2">
                    <Candidates />
                </div>
            </div>
            <br />
            <br />
            <p>
                Project <b>Rojak</b> adalah sebuah non-profit project untuk
                membantu jalannya Pilkada DKI Jakarta 2017 dalam hal pengawasan media daring.
            </p>
        </div>
        <div className="uk-width-1-10" />
    </div>
);

export default HomePage;
