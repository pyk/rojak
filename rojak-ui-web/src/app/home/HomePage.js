import React from 'react';
import rojak from '../../assets/images/rojak-black.svg';
import styles from './HomePage.css';

const Card = ({ children }) => {
    return (
        <div className={`uk-grid ${styles.cardWrapper}`}>
            <div className={`uk-width-1-1 ${styles.card}`}>{children}</div>
        </div>
    );
};

const HomePage = () => (
    <div id="HomePage" className={`uk-grid ${styles.homepageWrapper}`}>
        <div className="uk-width-1-10" />
        <div className="uk-width-8-10">
            <h1 className={styles.halo}>Halo!</h1>
            <Card>
                <img className={styles.rojakLogo} src={rojak} alt="rojak" />
                <p style={{ backgroundColor: '#fff' }}>
                    Saya Rojak, saya akan membantu Anda memilih kandidat Pilkada dengan bijak
                    secara objektif tanpa terpengaruh media bayaran.
                </p>
                <br />
                <a
                    className={`uk-button uk-button-large ${styles.learnMoreButton}`}
                    type="button"
                    href="https://github.com/pyk/rojak"
                >
                    Pelajari selengkapnya →
                </a>
            </Card>
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
