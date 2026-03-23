/**
 * API service module using Axios
 * Handles communication with FastAPI backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Convert HTML quiz to text and Word document
 */
export async function convertHTML(htmlContent, options = {}) {
  try {
    const payload = {
      html_content: htmlContent,
      shuffle: options.shuffle || false,
      shuffle_count: options.shuffleCount || 1,
    };

    const response = await apiClient.post('/api/convert/', payload);
    return response.data;
  } catch (error) {
    console.error('Error converting HTML:', error);
    throw error.response?.data || error.message;
  }
}

/**
 * Download Word document by file ID
 */
export async function downloadDocument(fileId) {
  try {
    const response = await apiClient.get(`/api/download/${fileId}`, {
      responseType: 'blob',
    });

    // Create blob and download
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `quiz_${fileId.substring(0, 8)}.docx`);
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
    window.URL.revokeObjectURL(url);

    return true;
  } catch (error) {
    console.error('Error downloading document:', error);
    throw error.response?.data || error.message;
  }
}

/**
 * Get conversion history
 */
export async function getHistory(limit = 10) {
  try {
    const response = await apiClient.get('/api/history/', {
      params: { limit },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error.response?.data || error.message;
  }
}

/**
 * Health check
 */
export async function healthCheck() {
  try {
    const response = await apiClient.get('/api/health/');
    return response.data;
  } catch (error) {
    console.error('Error in health check:', error);
    throw error.response?.data || error.message;
  }
}

export default apiClient;
