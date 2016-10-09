import React from 'react';
import Navbar from './Navbar';

const Container = ({ children }) => (
    <div id="container">
        <Navbar />
        <div className="uk-container uk-container-center">
            {children}
        </div>
    </div>
);

export default Container;
