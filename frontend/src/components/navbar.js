import React from 'react';
import './navbar.css';

const Navbar = ({ userData, handlePageChange, setUserData }) => {
  return (
    <nav className="navbar">
      <div className="navbar-buttons">
        <button className="navbar-button" onClick={() => handlePageChange('home')}>Home</button>
        <button className="navbar-button" onClick={() => handlePageChange('info')}> Learn About Cloud Seeding </button>
      </div>
      
    </nav>
  );
};

export default Navbar;