import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import DocumentationPage from './pages/DocumentationPage';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/documentation">Documentation</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/documentation" element={<DocumentationPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
