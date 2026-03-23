/**
 * WordExport - Component for Word document download button
 */

import React, { useState } from 'react';
import { downloadDocument } from '../api';
import '../styles/WordExport.css';

const WordExport = ({ fileId, questionCount, isLoading }) => {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    if (!fileId) {
      alert('Không có file để tải');
      return;
    }

    try {
      setDownloading(true);
      await downloadDocument(fileId);
    } catch (error) {
      alert(`Lỗi tải file: ${error.message || 'Vui lòng thử lại'}`);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="word-export-container">
      <button
        className={`download-button ${downloading ? 'loading' : ''}`}
        onClick={handleDownload}
        disabled={!fileId || isLoading || downloading}
        title={fileId ? 'Tải file Word (.docx)' : 'Chuyển đổi trước để tải file'}
      >
        {downloading ? '⏳ Đang tải...' : '📥 Tải File Word'}
      </button>

      {fileId && questionCount > 0 && (
        <div className="export-info">
          <span className="file-info">
            ✓ Sẵn sàng: {questionCount} câu hỏi
          </span>
        </div>
      )}
    </div>
  );
};

export default WordExport;
