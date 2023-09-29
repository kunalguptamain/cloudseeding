
import React from 'react';
import DataTable from '../table';

function OutputPage({output}) {
    console.log(output)
    console.log(output[0])
    console.log(output[1])
    console.log(output[1]["cloudcover_75"])

    return(
        <div className="container">   
            <header className="info-text">
                Percent chance of successful cloudseeding: {output[0]}.
                Based off the following data gathered about your location:
                
            </header>

            <div>
                <h1>Data Table</h1>
                <DataTable data={output[1]} />
            </div>
        </div>
    );
}

export default OutputPage;