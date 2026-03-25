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
      {/* Summary Table */}
      {predictions && (
        <div className="quiz-summary">
          <h4>📊 Kết Quả Phân Tích</h4>
          <div className="summary-table">
            {questions.map((q, idx) => {
              const questionNum = idx + 1;
              const aiAnswer = predictions[`question_${questionNum}`] || '?';
              const userAnswer = userAnswers[questionNum];
              const status = getAnswerStatus(questionNum, userAnswer);
              
              return (
                <div key={questionNum} className={`summary-cell status-${status || 'pending'}`}>
                  <span className="cell-number">{questionNum}</span>
                  <span className="cell-answer">{aiAnswer}</span>
                  {userAnswer && <span className="cell-user-answer">{userAnswer}</span>}
                </div>
              );
            })}
          </div>
        </div>
      )}

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
        </div>
      )}
    </div>
  );
}
