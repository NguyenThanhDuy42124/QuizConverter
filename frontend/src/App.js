/**
 * Main App component - Layout and state management
 */

import React, { useState, useEffect } from 'react';
import './App.css';
import HtmlInputPanel from './components/HtmlInputPanel';
import TextResultPanel from './components/TextResultPanel';
import WordExport from './components/WordExport';
import AIAnalysisPanel from './components/AIAnalysisPanel';
import Footer from './components/Footer';
import { convertHTML, healthCheck } from './api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [textResult, setTextResult] = useState('');
  const [fileId, setFileId] = useState('');
  const [questionCount, setQuestionCount] = useState(0);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [apiConnected, setApiConnected] = useState(false);
  const [htmlInput, setHtmlInput] = useState('');  // Track current HTML input

  // Check API connection on mount
  useEffect(() => {
    const checkConnection = async () => {
      try {
        await healthCheck();
        setApiConnected(true);
      } catch (error) {
        console.error('API connection failed:', error);
        setApiConnected(false);
      }
    };

    checkConnection();
  }, []);

  const handleConvert = async (options) => {
    try {
      setIsLoading(true);
      setError(null);
      setSuccess(false);
      setHtmlInput(options.htmlContent);  // Store HTML input for AI analysis

      const result = await convertHTML(
        options.htmlContent,
        {
          shuffle: options.shuffle,
          shuffleCount: options.shuffleCount,
        }
      );

      if (result.success) {
        setTextResult(result.text_output);
        setFileId(result.file_id);
        setQuestionCount(result.question_count);
        setSuccess(true);

        // Clear success message after 3 seconds
        setTimeout(() => setSuccess(false), 3000);
      } else {
        setError(result.message || 'Chuyển đổi không thành công');
      }
    } catch (error) {
      setError(error.detail || error.message || 'Lỗi không xác định');
      console.error('Conversion error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🎓 Quiz Converter</h1>
          <p className="tagline">Chuyển đổi HTML Moodle → Word + Text</p>
          <div className="connection-status">
            {apiConnected ? (
              <span className="status connected">● Kết nối API</span>
            ) : (
              <span className="status disconnected">⚠ Chưa kết nối API</span>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="content-wrapper">
          {/* Alerts */}
          {error && (
            <div className="alert alert-error">
              <span>❌ {error}</span>
              <button onClick={() => setError(null)}>✕</button>
            </div>
          )}

          {success && (
            <div className="alert alert-success">
              <span>✓ Chuyển đổi thành công!</span>
            </div>
          )}

          {/* Layout: Top Input + AI Analysis + Middle Quick Copy/Download + Bottom Detailed */}
          <div className="panels-layout">
            {/* Top: HTML Input */}
            <div className="input-section">
              <HtmlInputPanel onConvert={handleConvert} isLoading={isLoading} />
            </div>

            {/* AI Analysis Section */}
            {htmlInput && (
              <AIAnalysisPanel 
                htmlContent={htmlInput}
                isLoading={isLoading}
              />
            )}

            {/* Middle: Quick Copy + Download */}
            {textResult && (
              <div className="quick-actions-grid">
                <div className="quick-copy-box">
                  <TextResultPanel 
                    textContent={textResult} 
                    isLoading={isLoading}
                    compactMode={true}
                  />
                </div>
                <div className="quick-download-box">
                  <WordExport
                    fileId={fileId}
                    questionCount={questionCount}
                    isLoading={isLoading}
                  />
                </div>
              </div>
            )}

            {/* Bottom: Detailed Preview */}
            {textResult && (
              <div className="detailed-preview-section">
                <TextResultPanel 
                  textContent={textResult} 
                  isLoading={isLoading}
                  compactMode={false}
                />
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;
