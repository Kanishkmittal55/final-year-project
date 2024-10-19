import React from 'react';

function DocumentationPage() {
  return (
    <div>
      <h1>API Documentation</h1>
      <p>
        This page contains documentation for using the API. You can make requests to the following endpoints:
      </p>
      <ul>
        <li><code>/scrape/sephora</code> - Scrape data from Sephora</li>
        <li><code>/scrape/bloomage</code> - Scrape data from Bloomage</li>
        <li><code>/scrape/proya</code> - Scrape data from Proya</li>
        <li><code>/scrape/theordinary</code> - Scrape data from The Ordinary</li>
      </ul>
    </div>
  );
}

export default DocumentationPage;
