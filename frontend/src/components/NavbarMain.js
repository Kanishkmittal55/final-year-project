import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-blue-500 p-4 text-white"> {/* Tailwind classes for styling */}
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-2xl font-bold">
          <Link to="/" className="hover:text-gray-200">Scrapy</Link> {/* Brand/Logo */}
        </div>
        <ul className="flex space-x-4">
          <li>
            <Link to="/" className="hover:text-gray-200">Home</Link>
          </li>
          <li>
            <Link to="/documentation" className="hover:text-gray-200">Documentation</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
