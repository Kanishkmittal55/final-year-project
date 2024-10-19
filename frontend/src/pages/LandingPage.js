import React, { useState } from 'react';
import axios from 'axios';
import './LandingPage.css'; // Add custom styling

function LandingPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedScraper, setSelectedScraper] = useState('');

  const handleScrape = (scraperName) => {
    setLoading(true);
    setSelectedScraper(scraperName);
    axios.get(`http://localhost:5000/scrape/${scraperName}`)
      .then(response => {
        setData(response.data.data);  // Access the scraped data from response
        setLoading(false);
      })
      .catch(error => {
        console.error("There was an error fetching the data!", error);
        setLoading(false);
      });
  };

  return (
    <div className="landing-page">
      <h1>Welcome to the Scraper Dashboard</h1>
      
      <div className="button-container">
        <button onClick={() => handleScrape('sephora')}>Scrape Sephora</button>
        <button onClick={() => handleScrape('bloomage')}>Scrape Bloomage</button>
        <button onClick={() => handleScrape('proya')}>Scrape Proya</button>
        <button onClick={() => handleScrape('theordinary')}>Scrape The Ordinary</button>
      </div>

      {loading ? (
        <p className="loading-text">Loading {selectedScraper} data...</p>
      ) : (
        <div className="data-display">
          <h2>Scraped Data from {selectedScraper}</h2>
          {data ? (
            <pre>{JSON.stringify(data, null, 2)}</pre>
          ) : (
            <p>No data to display. Click a button to start scraping!</p>
          )}
        </div>
      )}
    </div>
  );
}

export default LandingPage;
