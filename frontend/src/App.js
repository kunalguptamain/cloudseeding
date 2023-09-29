import React,  { useState} from 'react';
import HomePage from './pages/HomePage.js';
import InfoPage from './pages/InfoPage.js';
import OutputPage from './pages/OutputPage.js';
import NavBar from './components/navbar';
import DataTable from './table.js';
import './App.css';

function  App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [output, setOutput] = useState('');

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'info':
        return <InfoPage/>
      case 'output':
        return <OutputPage
        output={output}
        />
      default:
        return <HomePage 
        setOutput={setOutput}
        handlePageChange={handlePageChange}/>
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
