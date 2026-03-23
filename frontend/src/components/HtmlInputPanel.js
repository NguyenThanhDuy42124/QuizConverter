/**
 * HtmlInputPanel - Component for HTML input and conversion
 * Allows users to paste HTML code, upload files, or drag & drop
 */

import React, { useState, useRef } from 'react';
import '../styles/HtmlInputPanel.css';

const HtmlInputPanel = ({ onConvert, isLoading }) => {
  const [htmlContent, setHtmlContent] = useState('');
  const [shuffle, setShuffle] = useState(false);
  const [shuffleCount, setShuffleCount] = useState(1);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleConvert = async () => {
    if (!htmlContent.trim()) {
      alert('Vui lòng dán mã HTML hoặc tải lên file');
      return;
    }

    try {
      await onConvert({
        htmlContent,
        shuffle,
        shuffleCount: shuffle ? shuffleCount : 1,
      });
    } catch (error) {
      alert(`Lỗi: ${error.message || 'Không thể chuyển đổi'}`);
    }
  };

  const handlePaste = async (event) => {
    const items = (event.clipboardData || window.clipboardData).items;
    for (let item of items) {
      if (item.type.indexOf('text/html') !== -1) {
        item.getAsString((str) => {
          setHtmlContent(str);
        });
      }
    }
  };

  const readFile = (file) => {
    if (!file.type.includes('html') && !file.type.includes('text')) {
      alert('Vui lòng chọn file HTML');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      setHtmlContent(event.target.result);
    };
    reader.onerror = () => {
      alert('Lỗi đọc file');
    };
    reader.readAsText(file);
  };

  const handleFileSelect = (event) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      // Read all selected files
      let loadedCount = 0;
      let combinedHTML = '';

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (!file.type.includes('html') && !file.type.includes('text')) {
          alert(`File "${file.name}" không phải HTML. Bỏ qua.`);
          continue;
        }

        const reader = new FileReader();
        reader.onload = (event) => {
          combinedHTML += event.target.result;
          loadedCount++;

          // When all files are loaded, update state
          if (loadedCount === files.length) {
            setHtmlContent(combinedHTML);
          }
        };
        reader.onerror = () => {
          alert(`Lỗi đọc file: ${file.name}`);
        };
        reader.readAsText(file);
      }
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      // Treat drop as file select
      const fakeEvent = { target: { files } };
      handleFileSelect(fakeEvent);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);
  };

  return (
    <div className="html-input-panel">
      <div className="panel-header">
        <h2>📋 Dán Hoặc Tải HTML</h2>
        <p className="subtitle">Dán mã HTML, tải file, hoặc kéo thả file HTML vào</p>
      </div>

      {/* File Upload & Drag Drop Area */}
      <div
        className={`drop-zone ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".html,.htm,.txt"
          onChange={handleFileSelect}
          multiple
          style={{ display: 'none' }}
          disabled={isLoading}
        />

        {htmlContent ? (
          <div className="drop-zone-content">
            <span className="drop-icon">✓</span>
            <p>File(s) đã được tải</p>
            <span className="file-size">
              {(htmlContent.length / 1024).toFixed(1)} KB
            </span>
          </div>
        ) : (
          <div className="drop-zone-content">
            <span className="drop-icon">📁</span>
            <p>Kéo thả file HTML tại đây</p>
            <p className="drop-hint">hoặc nhấp để chọn file (hỗ trợ nhiều file)</p>
          </div>
        )}
      </div>

      <textarea
        className="html-textarea"
        value={htmlContent}
        onChange={(e) => setHtmlContent(e.target.value)}
        onPaste={handlePaste}
        placeholder="Dán HTML tại đây, tải file, hoặc kéo thả..."
        disabled={isLoading}
      />

      <div className="options-section">
        <label className="checkbox-option">
          <input
            type="checkbox"
            checked={shuffle}
            onChange={(e) => setShuffle(e.target.checked)}
            disabled={isLoading}
          />
          <span>Xáo trộn câu hỏi</span>
        </label>

        {shuffle && (
          <div className="shuffle-options">
            <label htmlFor="shuffle-count">Số mã đề:</label>
            <input
              id="shuffle-count"
              type="number"
              min="1"
              max="100"
              value={shuffleCount}
              onChange={(e) => setShuffleCount(Math.max(1, parseInt(e.target.value) || 1))}
              disabled={isLoading}
              className="shuffle-input"
            />
          </div>
        )}
      </div>

      <button
        className={`convert-button ${isLoading ? 'loading' : ''}`}
        onClick={handleConvert}
        disabled={isLoading}
      >
        {isLoading ? '⏳ Đang xử lý...' : '🔄 Phân tích & Chuyển đổi'}
      </button>

      {htmlContent && (
        <div className="info-text">
          ✓ Đã tải: {htmlContent.length} ký tự ({(htmlContent.length / 1024).toFixed(1)} KB)
        </div>
      )}
    </div>
  );
};

export default HtmlInputPanel;
