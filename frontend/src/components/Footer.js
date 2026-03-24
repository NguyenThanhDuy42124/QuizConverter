/**
 * Footer Component
 */

import React from 'react';
import '../styles/Footer.css';

const Footer = () => {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <p className="footer-tech">
          Built with FastAPI + React. Powered by Python & BeautifulSoup4.
        </p>
        <p className="footer-credit">
          Made by @DaoTacVoSi05 | GitHub:{' '}
          <a href="https://github.com/NguyenThanhDuy42124" target="_blank" rel="noopener noreferrer">
            NguyenThanhDuy42124
          </a>
        </p>
      </div>
    </footer>
  );
};

export default Footer;
