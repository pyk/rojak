import React from 'react';
import { connect } from 'react-redux';
import Card from '../kit/Card';

const Medias = (props) => {
    const mediaList = props
        .medias
        .map(media => (
            <li key={media.id} style={{ letterSpacing: 5 }}>
                <a
                    target="_blank"
                    rel="noopener noreferrer"
                    href={media.website_url}
                >
                    {media.name}
                </a>
            </li>
        ));
    return (
        <Card style={{ textAlign: 'left' }}>
            <div className="uk-grid">
                <div className="uk-width-1-1" style={{ textAlign: 'center' }}>
                    <span className="ion-ios-pulse" style={{ fontSize: 100 }} />
                    <h2 style={{ fontSize: 22, fontWeight: 600 }}>Media</h2>
                </div>
            </div>
            <p>
                Saat ini Rojak sedang menganalisa beberapa muatan media berikut
                terhadap semua pasangan Cagub-Cawagub DKI Jakarta.
            </p>
            <ol>
                {mediaList}
            </ol>
        </Card>
    );
};

Medias.propTypes = {
    medias: React.PropTypes.array,
};

const mapStateToProps = state => ({
    medias: state.medias,
});

export default connect(mapStateToProps)(Medias);
