import React, {useState} from 'react';
import logo from '../logo.svg';
import GifDisplay from './GifDisplay.js'; // Adjust the import path as needed

function HomePage({handlePageChange, setOutput}) {
    const [isLoading, setIsLoading] = useState(false);
    const [location, setLocation] = useState("");
    const [lat, setLat] = useState("");
    const [long, setLong] = useState("");

    const handleSubmit = async (e) => {
        setIsLoading(true);
        e.preventDefault();
        try {
        const response = await fetch('http://localhost:5002/process_input', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input_data: [lat, long] }),
        });
        if (response.ok) {
            const data = await response.json();
            setOutput(data);
            setIsLoading(false);
            console.log("hello")
            console.log(data);
            handlePageChange('output')
        } else {
            console.error('Error:', response.status);
        }
        } catch (error) {
        console.error('Request failed:', error);
        }
    };

    if (isLoading) {
        return <div className='container'>
        <h1>Loading...</h1>
        </div>
    }
    return(
        <div className="container">
            <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <GifDisplay />
            <div className="form-container">
                <form className="lat-long-form" onSubmit={handleSubmit}>
                    {/* <label> Enter a location</label>
                    <input className= 'default-input'
                    type="location"
                    placeholder="your location"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    />
                    <br/> */}
                    
                    <label> Enter a latitude: </label>
                    <input className= 'default-input'
                    type="location"
                    value={lat}
                    onChange={(e) => setLat(e.target.value)}
                    />
                    <br/>

                    <label> Enter a longtitude: </label>
                    <input className= 'default-input'
                    type="location"
                    value={long}
                    onChange={(e) => setLong(e.target.value)}
                    />
                    <br/>
                    
                  <button class="submit-button" type="submit">
                            <span>Enter</span>
                            <div class="success">
                            
                            </div>
                        </button>
                </form>
            </div>
            <div className="App-link">
                <a
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={() => handlePageChange('info')}
                >
                    Learn about cloud seeding!
                </a>
            </div>

            <br/>
            
            </header>
        </div>
    );
}

export default HomePage;