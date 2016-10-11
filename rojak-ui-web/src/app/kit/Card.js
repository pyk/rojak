import React from 'react';

const styles = {
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
};

const Card = ({ children, style }) => {
    return (
        <div className="uk-grid" style={Object.assign({}, styles.cardWrapper, style)}>
            <div style={styles.card} className="uk-width-1-1">{children}</div>
        </div>
    );
};

export default Card;
