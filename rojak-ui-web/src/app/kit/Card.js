import React from 'react';
import styles from './Card.css';

const Card = ({ children, style, className }) => {
    return (
        <div className={`${className} ${styles.cardWrapper} `} style={style}>
            <div className={styles.card}>{children}</div>
        </div>
    );
};

export default Card;
