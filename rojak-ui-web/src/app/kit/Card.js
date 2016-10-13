import React from 'react';
import styles from './Card.css';

const Card = ({ children, style }) => {
    return (
        <div className={`uk-grid ${styles.cardWrapper}`} style={style}>
            <div className={`uk-width-1-1 ${styles.card}`}>{children}</div>
        </div>
    );
};

export default Card;
