import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';
import yesstyleImage from '../assets/yesstyle.png';

function LandingPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedScraper, setSelectedScraper] = useState('');
  const navigate = useNavigate();

  const handleScrape = (scraperName) => {
    setSelectedScraper(scraperName);

    // Check if the YesStyle scraper is selected
    if (scraperName === 'yesstyle') {
      navigate('/yesstyle/sitemap'); // Navigate to the sitemap page
    } else {
      // For other scrapers, perform the scrape and display data
      setLoading(true);
      axios.get(`http://localhost:5000/scrape/${scraperName}`)
        .then(response => {
          setData(response.data.data);
          setLoading(false);
        })
        .catch(error => {
          console.error("There was an error fetching the data!", error);
          setLoading(false);
        });
    }
  };

  return (
    <div className="landing-page">
      <h1>Welcome to the Scraper Dashboard</h1>
      <div className="scraper-card" onClick={() => handleScrape('yesstyle')}>
        <img src={yesstyleImage} alt="YesStyle" className="scraper-image" />
        <h2>YesStyle Scraper</h2>
        <p>Click to view and analyze YesStyle data.</p>
      </div>
    </div>
  );
}

export default LandingPage;
