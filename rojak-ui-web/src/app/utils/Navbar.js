import React from 'react';
import { Link } from 'react-router';
import rojakBlack from '../../assets/images/rojak-black.svg';
import styles from './Navbar.css';

const Navbar = () => (
    <nav className={`uk-navbar ${styles.navbar}`}>
        <ul className="uk-navbar-nav">
            <li className="uk-active">
                <Link className={styles.homeLink} to="/">
                    <img className={styles.logo} src={rojakBlack} alt="logo" />
                </Link>
            </li>
        </ul>
    </nav>
);

export default Navbar;
