import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import DocumentationPage from './pages/DocumentationPage';
import YesStyleDataPage from './pages/YesstyleData';
import YesStyleSitemap from './pages/YesstyleSitemap'; // Import the Sitemap component
import Navbar from './components/NavbarMain'; // Import Navbar component

function App() {
  return (
    <Router>
      <div>
        <Navbar /> {/* Use Navbar component */}
        
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/documentation" element={<DocumentationPage />} />
          <Route path="/yesstyle/:category" element={<YesStyleDataPage />} />
          <Route path="/yesstyle/sitemap" element={<YesStyleSitemap />} /> {/* New route for Sitemap */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
