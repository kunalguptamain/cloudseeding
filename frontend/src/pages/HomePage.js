import React, {useState} from 'react';
import logo from '../logo.svg';

function HomePage() {
    const [location, setLocation] = useState("");

    return(
        <div className="container">
            <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <form className="form" onSubmit>
                <label> Enter a location</label>
                <input className= 'default-input'
                type="location"
                placeholder="your location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                />
                <br/>
                <button className="submit-button" type="submit"> Enter </button>
            </form>
            <br/>
            <a
                className="App-link"
                href="https://reactjs.org"
                target="_blank"
                rel="noopener noreferrer"
            >
                Learn about cloud seeding!
            </a>
            </header>
        </div>
    );
}

export default HomePage;