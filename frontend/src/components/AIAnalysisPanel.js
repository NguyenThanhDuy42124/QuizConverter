/**
 * AIAnalysisPanel - Component for analyzing quizzes with Gemini AI
 */

import React, { useState } from 'react';
import '../styles/AIAnalysisPanel.css';
import InteractiveQuiz from './InteractiveQuiz';

const AIAnalysisPanel = ({ htmlContent, onAnalysisComplete, isLoading: parentLoading = false }) => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const analyzeWithAI = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('/api/analyze-with-ai/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          html_content: htmlContent,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Lỗi phân tích AI');
      }

      const data = await response.json();
      setResults(data);
      setShowResults(true);
      
      if (onAnalysisComplete) {
        onAnalysisComplete(data);
      }
    } catch (err) {
      setError(err.message || 'Lỗi không xác định');
      console.error('AI Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const downloadMarkdText = async () => {
    try {
      const response = await fetch('/api/export-marked-text/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          html_content: htmlContent,
        }),
      });

      if (!response.ok) throw new Error('Lỗi tải file');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'quiz_marked.txt';
      document.body.appendChild(a);
      a.click();
      a.parentNode.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Lỗi khi tải file: ' + err.message);
    }
  };

  const downloadMarkedDocx = async () => {
    try {
      const response = await fetch('/api/export-marked-docx/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          html_content: htmlContent,
        }),
      });

      if (!response.ok) throw new Error('Lỗi tải file');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'quiz_marked.docx';
      document.body.appendChild(a);
      a.click();
      a.parentNode.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Lỗi khi tải file: ' + err.message);
    }
  };

  const downloadUnmarkedDocx = async () => {
    try {
      const response = await fetch('/api/export-unmarked-docx/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          html_content: htmlContent,
        }),
      });

      if (!response.ok) throw new Error('Lỗi tải file');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'quiz_unmarked.docx';
      document.body.appendChild(a);
      a.click();
      a.parentNode.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Lỗi khi tải file: ' + err.message);
    }
  };

  const isDisabled = loading || parentLoading || !htmlContent;

  return (
    <div className="ai-analysis-panel">
      <div className="ai-header">
        <h3>🤖 Phân Tích với AI</h3>
        <p className="ai-description">Sử dụng Google Gemini để tự động đánh dấu đáp án đúng</p>
      </div>

      {error && (
        <div className="ai-error">
          <span>❌ {error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      <div className="ai-actions">
        <button
          onClick={analyzeWithAI}
          disabled={isDisabled}
          className="btn-ai-analyze"
          title={isDisabled ? 'Vui lòng dán HTML trước' : 'Phân tích với AI'}
        >
          {loading ? '⏳ Đang phân tích...' : '🤖 Phân tích ngay'}
        </button>
      </div>

      {results && showResults && (
        <div className="ai-results">
          <div className="results-header">
            <h4>📊 Kết Quả Phân Tích ({results.total_questions} câu)</h4>
            <div className="export-buttons">
              <button onClick={downloadMarkdText} className="btn-export-text">
                📄 Tải TXT
              </button>
              <button onClick={downloadMarkedDocx} className="btn-export-docx">
                📘 Tải Word (có đáp án)
              </button>
              <button onClick={() => downloadUnmarkedDocx()} className="btn-export-docx">
                📗 Tải Word (không đáp án)
              </button>
            </div>
          </div>

          <InteractiveQuiz
            questions={results.questions}
            predictions={results.questions.reduce((acc, q) => {
              acc[q.question_number] = q.predicted_answer;
              return acc;
            }, {})}
            onUserAnswersChange={(userAnswers) => {
              console.log('User answers:', userAnswers);
            }}
          />
        </div>
      )}
    </div>
  );
};

export default AIAnalysisPanel;
