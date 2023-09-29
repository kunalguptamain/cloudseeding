
import React from 'react';

function OutputPage({output}) {
    return(
        <div className="container">   
            <header className="info-text">
                Percent chance of cum: {output}
            </header>
        </div>
    );
}

export default OutputPage;