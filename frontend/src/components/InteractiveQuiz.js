import React, { useState } from 'react';
import '../styles/InteractiveQuiz.css';

export default function InteractiveQuiz({ questions, predictions, onUserAnswersChange }) {
  const [userAnswers, setUserAnswers] = useState({});
  const [expandedQuestion, setExpandedQuestion] = useState(null);

  const handleAnswerSelect = (questionNum, selectedAnswer) => {
    if (!predictions) return; // Can't select if no AI predictions yet
    
    const newAnswers = { ...userAnswers, [questionNum]: selectedAnswer };
    setUserAnswers(newAnswers);
    
    if (onUserAnswersChange) {
      onUserAnswersChange(newAnswers);
    }
  };

  const toggleQuestion = (questionNum) => {
    setExpandedQuestion(expandedQuestion === questionNum ? null : questionNum);
  };

  const getAnswerStatus = (questionNum, userAnswer) => {
    if (!predictions || !userAnswer) return null;
    
    const aiAnswer = predictions[`question_${questionNum}`];
    if (userAnswer === aiAnswer) return 'correct';
    if (userAnswer && aiAnswer) return 'incorrect';
    return null;
  };

  return (
    <div className="interactive-quiz">
      {/* Expandable Details Section */}
      <div className="quiz-details">
        <h4>📋 Xem Chi Tiết Trắc Nghiệm</h4>
        <div className="questions-container">
          {questions.map((q, idx) => {
            const questionNum = idx + 1;
            const isExpanded = expandedQuestion === questionNum;
            const userAnswer = userAnswers[questionNum];
            const status = getAnswerStatus(questionNum, userAnswer);
            const isAnswered = userAnswer !== undefined;

            return (
              <div key={questionNum} className={`quiz-item status-${status || 'unanswered'}`}>
                {/* Question Header */}
                <div 
                  className="question-header"
                  onClick={() => toggleQuestion(questionNum)}
                  style={{ cursor: 'pointer' }}
                >
                  <div className="header-left">
                    <span className="question-number">Câu {questionNum}</span>
                    <span className="question-text-preview">
                      {q.question_text.substring(0, 60)}...
                    </span>
                  </div>
                  <div className="header-right">
                    {predictions && (
                      <>
                        <span className="ai-answer">
                          AI: <strong>{predictions[`question_${questionNum}`]}</strong>
                        </span>
                        {isAnswered && (
                          <span className={`user-answer status-${status}`}>
                            Bạn: <strong>{userAnswer}</strong>
                          </span>
                        )}
                      </>
                    )}
                    <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
                  </div>
                </div>

                {/* Question Details - Expandable */}
                {isExpanded && (
                  <div className="question-details">
                    <div className="full-question-text">
                      <p>{q.question_text}</p>
                    </div>

                    {/* Answer Options */}
                    <div className="answer-options">
                      {q.answers.map((answer, ansIdx) => {
                        const isSelected = userAnswer === answer.letter;
                        const isAIAnswer = predictions && predictions[`question_${questionNum}`] === answer.letter;
                        const answerStatus = isSelected ? status : null;

                        return (
                          <div
                            key={ansIdx}
                            className={`answer-option ${isSelected ? 'selected' : ''} ${answerStatus ? `status-${answerStatus}` : ''}`}
                            onClick={() => handleAnswerSelect(questionNum, answer.letter)}
                            style={{
                              opacity: predictions ? 1 : 0.5,
                              cursor: predictions ? 'pointer' : 'not-allowed',
                              pointerEvents: predictions ? 'auto' : 'none'
                            }}
                          >
                            <div className="option-content">
                              <input
                                type="radio"
                                name={`question_${questionNum}`}
                                value={answer.letter}
                                checked={isSelected}
                                onChange={() => handleAnswerSelect(questionNum, answer.letter)}
                                disabled={!predictions}
                              />
                              <label>
                                <strong>{answer.letter}.</strong> {answer.content}
                              </label>
                            </div>
                            
                            {/* Status Indicators */}
                            {isAIAnswer && (
                              <span className="ai-indicator">🤖 AI chọn</span>
                            )}
                            {isSelected && answerStatus === 'correct' && (
                              <span className="correct-indicator">✓ Đúng</span>
                            )}
                            {isSelected && answerStatus === 'incorrect' && (
                              <span className="incorrect-indicator">✗ Sai</span>
                            )}
                          </div>
                        );
                      })}
                    </div>

                    {/* Feedback */}
                    {predictions && (
                      <div className="answer-feedback">
                        {!isAnswered && (
                          <p style={{ color: '#ff9800' }}>👆 Chọn đáp án của bạn</p>
                        )}
                        {isAnswered && (
                          <p style={{ color: '#ffffff', marginBottom: '0.5rem' }}>
                            Câu trả lời của bạn: <strong style={{ color: '#0066cc', fontSize: '1.1rem' }}>{userAnswer}</strong>
                          </p>
                        )}
                        {isAnswered && status === 'correct' && (
                          <p style={{ color: '#28a745' }}>🎉 Câu trả lời đúng!</p>
                        )}
                        {isAnswered && status === 'incorrect' && (
                          <p style={{ color: '#dc3545' }}>
                            ❌ Sai rồi! Đáp án đúng là: <strong>{predictions[`question_${questionNum}`]}</strong>
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Stats */}
      {predictions && Object.keys(userAnswers).length > 0 && (
        <div className="quiz-stats">
          <h4>📈 Thống Kê</h4>
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Tổng câu:</span>
              <span className="stat-value">{questions.length}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Đã làm:</span>
              <span className="stat-value">{Object.keys(userAnswers).length}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Đúng:</span>
              <span className="stat-value correct">
                {Object.entries(userAnswers).filter(
                  ([qNum, ans]) => getAnswerStatus(parseInt(qNum), ans) === 'correct'
                ).length}
              </span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Sai:</span>
              <span className="stat-value incorrect">
                {Object.entries(userAnswers).filter(
                  ([qNum, ans]) => getAnswerStatus(parseInt(qNum), ans) === 'incorrect'
                ).length}
              </span>
            </div>
          </div>

          {/* Summary Results Table - Số câu + Đáp án */}
          <div style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '2px solid #e0e0e0' }}>
            <h5 style={{ marginBottom: '1rem', color: '#000', fontSize: '1rem' }}>📊 Kết Quả Phân Tích ({questions.length} câu)</h5>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))',
              gap: '0.8rem'
            }}>
              {questions.map((q, idx) => {
                const questionNum = idx + 1;
                const aiAnswer = predictions[`question_${questionNum}`] || '?';
                
                return (
                  <div key={questionNum} style={{
                    background: '#f9f9f9',
                    border: '2px solid #0066cc',
                    borderRadius: '6px',
                    padding: '0.8rem',
                    textAlign: 'center',
                    fontSize: '0.95rem'
                  }}>
                    <span style={{ display: 'block', color: '#666', fontSize: '0.85rem', marginBottom: '0.3rem' }}>Câu {questionNum}</span>
                    <span style={{ display: 'block', fontSize: '1.2rem', fontWeight: 'bold', color: '#0066cc' }}>{aiAnswer}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
