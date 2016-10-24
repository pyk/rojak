import React, { Component } from 'react';
import Link from 'react-router/lib/Link';
import withRouter from 'react-router/lib/withRouter';
import SearchBox from './SearchBox';
import { ResultWrapper, DefaultResult, MediaResult, KandidatResult, PasanganResult } from '../result'

class HomePage extends Component {
    render() {
        const { params } = this.props

        return (
            <div>
                <SearchBox params={params} />
                <ResultWrapper>
                    <DefaultResult />
                    <MediaResult />
                    <KandidatResult />
                    <PasanganResult />
                </ResultWrapper>
            </div>
        );
    }
}

export default withRouter(HomePage);
