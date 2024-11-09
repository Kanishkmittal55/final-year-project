import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Sitemap.css'; // Custom styling for the text colors

function YesStyleSitemap() {
  const navigate = useNavigate();
  const [expanded, setExpanded] = useState({
    beauty: false,
  });

  const toggleExpand = (section) => {
    setExpanded((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-1/4 p-4 bg-white shadow-lg overflow-y-auto">
        <h2 className="text-xl font-semibold mb-4">YesStyle Sitemap</h2>
        <ul className="space-y-2">
          <li>
            <button
              onClick={() => toggleExpand('beauty')}
              className="text-white font-semibold hover:text-gray-300"
            >
              Beauty
            </button>
            {expanded.beauty && (
              <ul className="pl-4 mt-2 space-y-1">
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-cheeks')} className="text-white hover:text-gray-300">Cheeks</button></li>
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-eyes')} className="text-white hover:text-gray-300">Eyes</button></li>
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-face')} className="text-white hover:text-gray-300">Face</button></li>
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-lips')} className="text-white hover:text-gray-300">Lips</button></li>
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-hair-treatments')} className="text-white hover:text-gray-300">Hair Treatments</button></li>
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-shampoos')} className="text-white hover:text-gray-300">Shampoos</button></li>
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-face_cleansers')} className="text-white hover:text-gray-300">Face Cleansers</button></li>
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-face-serums')} className="text-white hover:text-gray-300">Face Serums</button></li>
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-moisturizers')} className="text-white hover:text-gray-300">Moisturizers</button></li>
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-toners')} className="text-white hover:text-gray-300">Toners</button></li>
                <li><button onClick={() => handleNavigation('/yesstyle/beauty-sunscreens')} className="text-white hover:text-gray-300">Sunscreens</button></li>
              </ul>
            )}
          </li>
        </ul>
      </div>
      <div className="w-3/4 h-full bg-gray-50 border-l-2 border-gray-200 p-4">
        {/* Add routing here */}
      </div>
    </div>
  );
}

export default YesStyleSitemap;
