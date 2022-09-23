import React from 'react';
import './Header.css';

function Header(): JSX.Element {
    return (
        <div className="Header">
            <img className="clg_logo" src={'clg_logo.jpg'} />
            <img className="haifa_logo" src={'haifa_logo.jpg'} />
        </div>
    );
}

export default Header;
