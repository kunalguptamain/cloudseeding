import React,  { useState} from 'react';
import HomePage from './pages/HomePage.js';
import InfoPage from './pages/InfoPage.js';
import NavBar from './components/navbar';
import './App.css';

function  App() {
  const [currentPage, setCurrentPage] = useState('home');

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'info':
        return <InfoPage/>
      default:
        return <HomePage/>
    }
  }

  return (
    <div className="App">
      <NavBar handlePageChange={handlePageChange} />
      {renderPage()}
    </div>
  );
}

export default App;
