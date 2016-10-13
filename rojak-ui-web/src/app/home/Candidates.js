import React from 'react';
import { connect } from 'react-redux';
import Card from '../kit/Card';

const Candidates = (props) => {
    const candidateList = props
        .candidates
        .map(candidate => (
            <li key={candidate.id} style={{ letterSpacing: 5 }}>
                <a
                    target="_blank"
                    rel="noopener noreferrer"
                    href={candidate.website_url}
                >
                    {candidate.full_name} ({candidate.alias_name})
                </a>
            </li>
        ));
    return (
        <Card style={{ textAlign: 'left' }}>
            <div className="uk-grid">
                <div className="uk-width-1-1" style={{ textAlign: 'center' }}>
                    <span className="ion-ios-people-outline" style={{ fontSize: 100 }} />
                    <h2 style={{ fontSize: 22, fontWeight: 600 }}>Kandidat</h2>
                </div>
            </div>
            <p>
                Hasil analisa Rojak akan memberi pandangan objektif ke
                semua pasangan Cagub-Cawagub DKI Jakarta.
            </p>
            <ol>
                {candidateList}
            </ol>
        </Card>
    );
};

Candidates.propTypes = {
    candidates: React.PropTypes.array,
};

const mapStateToProps = state => ({
    candidates: state.candidates,
});

export default connect(mapStateToProps)(Candidates);
