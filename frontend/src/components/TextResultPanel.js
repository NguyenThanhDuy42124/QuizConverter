/**
 * TextResultPanel - Component for displaying text output and copy button
 */

import React, { useState } from 'react';
import '../styles/TextResultPanel.css';

const TextResultPanel = ({ textContent, isLoading, compactMode = false }) => {
  const [copied, setCopied] = useState(false);
  const [viewMode, setViewMode] = useState('formatted'); // 'formatted' or 'raw'

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(textContent);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      alert('Lỗi sao chép: ' + error.message);
    }
  };

  const handleSelectAll = () => {
    const textarea = document.querySelector('.text-result-content');
    if (textarea) {
      textarea.select();
    }
  };

  // Parse and format the text content for preview
  const formatForDisplay = (text) => {
    if (!text) return null;

    const lines = text.split('\n').filter(line => line.trim());
    const questions = [];
    let currentQuestion = null;

    for (const line of lines) {
      if (line.match(/^Câu \d+:/)) {
        if (currentQuestion) questions.push(currentQuestion);
        currentQuestion = { text: line, answers: [] };
      } else if (line.match(/^[A-Z]\./)) {
        if (currentQuestion) {
          currentQuestion.answers.push(line);
        }
      }
    }

    if (currentQuestion) questions.push(currentQuestion);

    return questions;
  };

  const questions = formatForDisplay(textContent);

  if (!textContent) {
    return (
      <div className="text-result-panel empty">
        <div className="panel-header">
          <h2>📄 Kết Quả</h2>
        </div>
        <div className="empty-state">
          <p>Dán HTML và nhấn "Phân tích & Chuyển đổi" để xem kết quả</p>
        </div>
      </div>
    );
  }

  // Compact mode - just show quick copy panel
  if (compactMode) {
    return (
      <div className="text-result-panel compact-mode">
        <div className="panel-header compact">
          <h3>📋 Sao Chép Văn Bản</h3>
          <button
            className={`action-button copy ${copied ? 'copied' : ''}`}
            onClick={handleCopy}
            disabled={isLoading}
            title="Sao chép vào clipboard"
          >
            {copied ? '✓ Đã Sao Chép!' : '📋 Sao Chép'}
          </button>
        </div>
        <textarea
          className="text-result-content compact"
          value={textContent}
          readOnly
          placeholder="Kết quả sẽ hiển thị ở đây..."
        />
        <div className="result-info compact">
          <span className="char-count">
            {textContent.length} ký tự | {textContent.split('\n').length} dòng
          </span>
        </div>
      </div>
    );
  }

  // Full mode - show detailed preview
  return (
    <div className="text-result-panel">
      <div className="panel-header">
        <h2>📄 Xem Chi Tiết Trắc Nghiệm</h2>
        <div className="button-group">
          <div className="view-mode-tabs">
            <button
              className={`tab-button ${viewMode === 'formatted' ? 'active' : ''}`}
              onClick={() => setViewMode('formatted')}
            >
              👁 Xem Trước
            </button>
            <button
              className={`tab-button ${viewMode === 'raw' ? 'active' : ''}`}
              onClick={() => setViewMode('raw')}
            >
              📝 Văn Bản
            </button>
          </div>
        </div>
      </div>

      {viewMode === 'formatted' ? (
        <div className="formatted-preview">
          {questions && questions.length > 0 ? (
            <div className="questions-list">
              {questions.map((q, idx) => (
                <div key={idx} className="question-card">
                  <div className="question-text">{q.text}</div>
                  <div className="answers-list">
                    {q.answers.map((ans, ansIdx) => (
                      <div key={ansIdx} className="answer-item">
                        {ans}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-format">
              Không thể phân tích định dạng. Chuyển sang chế độ Văn Bản để xem raw text.
            </p>
          )}
        </div>
      ) : (
        <textarea
          className="text-result-content"
          value={textContent}
          readOnly
          placeholder="Kết quả sẽ hiển thị ở đây..."
        />
      )}

      <div className="result-info">
        <span className="char-count">
          {textContent.length} ký tự | {textContent.split('\n').length} dòng |{' '}
          {questions?.length || 0} câu hỏi
        </span>
      </div>
    </div>
  );
};

export default TextResultPanel;
