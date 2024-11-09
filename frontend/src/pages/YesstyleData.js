import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './YesstyleData.css';

function YesStyleDataPage() {
  const { category } = useParams();
  const [data, setData] = useState([]);
  const [query, setQuery] = useState('');
  const [queryResult, setQueryResult] = useState(null);

  // Fetch initial data based on the category from the URL
  useEffect(() => {
    axios.get(`http://localhost:5000/yesstyle/${category}`)
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error(`Error fetching data for category ${category}:`, error);
      });
  }, [category]);

  const handleQuerySubmit = () => {
    axios.post('http://localhost:5000/run-query', { query })
      .then(response => {
        setQueryResult(response.data);
      })
      .catch(error => {
        console.error("Error running query:", error);
      });
  };

  return (
    <div className="yesstyle-data-page">
      <h1>YesStyle Products - {category.replace('-', ' ')}</h1>

      <div className="query-section">
        <h2>Run SQL Query</h2>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter SQL query here"
        />
        <button onClick={handleQuerySubmit}>Run Query</button>

        {queryResult && (
          <div className="query-result">
            <h3>Query Result</h3>
            <pre>{JSON.stringify(queryResult, null, 2)}</pre>
          </div>
        )}
      </div>

      <div className="products-container">
        {data.map((product, index) => (
          <div className="product-card" key={index}>
            <img src={product.image_url} alt={product.name} className="product-image" />
            <h3 className="product-name">{product.name}</h3>
            <p className="product-brand">Brand: {product.brand_name}</p>
            <p className="product-price">
              <span className="sell-price">{product.sell_price}</span>
              {product.discount && <span className="discount"> {product.discount}</span>}
            </p>
            <p className="product-ingredients">
              <strong>Ingredients:</strong> {product.ingredients}
            </p>
            <a href={product.url} target="_blank" rel="noopener noreferrer" className="product-link">
              View Product
            </a>
          </div>
        ))}
      </div>

      
    </div>
  );
}

export default YesStyleDataPage;
