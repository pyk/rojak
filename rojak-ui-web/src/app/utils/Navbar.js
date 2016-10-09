import React from 'react';
import { Link } from 'react-router';
import rojakBlack from '../../assets/images/rojak-black.svg';

const styles = {
    navbar: {
        backgroundColor: 'transparent',
        border: 0,
        padding: 10,
    },
    homeLink: {
        backgroundColor: 'transparent',
        border: 0,
    },
    logo: {
        height: 50,
    },
};
const Navbar = () => (
    <nav className="uk-navbar" style={styles.navbar}>
        <ul className="uk-navbar-nav">
            <li className="uk-active">
                <Link style={styles.homeLink} to="/">
                    <img style={styles.logo} src={rojakBlack} alt="logo" />
                </Link>
            </li>
        </ul>
    </nav>
);

export default Navbar;
