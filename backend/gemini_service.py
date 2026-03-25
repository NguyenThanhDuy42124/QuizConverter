"""
Google Gemini AI Service for automatic quiz answer marking.
Supports both real API mode and mock mode for development.
"""

import os
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    logger.warning("google-generativeai not installed. Running in mock mode.")


class GeminiService:
    """Service for AI-powered quiz answer analysis."""
    
    def __init__(self):
        """Initialize Gemini service with API key from environment."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        self.use_mock_mode = False
        
        if self.api_key and HAS_GENAI:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("✅ Gemini API configured successfully")
            except Exception as e:
                logger.warning(f"Failed to configure Gemini API: {e}. Falling back to mock mode.")
                self.use_mock_mode = True
        else:
            if not self.api_key:
                logger.warning("GEMINI_API_KEY not set. Running in mock mode.")
                logger.info("To enable real API: create .env.local file with GEMINI_API_KEY")
            self.use_mock_mode = True
    
    def analyze_quiz(self, questions: List[Dict]) -> Dict:
        """
        Analyze quiz questions and predict correct answers using AI.
        
        Args:
            questions: List of question dictionaries from parser
            
        Returns:
            Dictionary with predictions for each question
        """
        if self.use_mock_mode or not self.model:
            return self._mock_analyze(questions)
        
        try:
            return self._real_analyze(questions)
        except Exception as e:
            logger.error(f"Error in real analysis: {e}. Falling back to mock mode.")
            return self._mock_analyze(questions)
    
    def _real_analyze(self, questions: List[Dict]) -> Dict:
        """Perform real analysis using Gemini API."""
        predictions = {}
        answers_options = ['A', 'B', 'C', 'D']  # Common answer choices
        
        for q in questions:
            try:
                question_num = q.get('question_number', q.get('number', 0))
                question_text = q.get('question_text', q.get('text', ''))
                answers = q.get('answers', [])
                
                # Format the question for Gemini
                formatted_question = self._format_question_for_gemini(
                    question_text, answers
                )
                
                # Call Gemini API
                response = self.model.generate_content(formatted_question)
                
                # Parse response
                predicted_answer = self._parse_gemini_response(response.text, answers_options)
                
                if predicted_answer:
                    predictions[question_num] = predicted_answer
                    logger.debug(f"Q{question_num}: Predicted answer = {predicted_answer}")
                else:
                    # Fallback to first option if prediction fails
                    predictions[question_num] = 'A'
                    logger.debug(f"Q{question_num}: No valid prediction, using 'A'")
            
            except Exception as e:
                logger.error(f"Error analyzing question {question_num}: {e}")
                predictions[question_num] = 'A'  # Default fallback
        
        return predictions
    
    def _mock_analyze(self, questions: List[Dict]) -> Dict:
        """Mock analysis for development without API key."""
        predictions = {}
        cycle = ['A', 'B', 'C', 'D']
        
        for i, q in enumerate(questions):
            question_num = q.get('question_number', q.get('number', i + 1))
            # Cycle through answers based on question number for deterministic testing
            predicted_answer = cycle[(i) % len(cycle)]
            predictions[question_num] = predicted_answer
            logger.debug(f"[MOCK] Q{question_num}: Predicted answer = {predicted_answer}")
        
        return predictions
    
    def _format_question_for_gemini(self, question_text: str, answers: List[Dict]) -> str:
        """Format question for Gemini API."""
        prompt = f"""Analyze this quiz question and determine the most likely correct answer.

QUESTION: {question_text}

ANSWERS:
"""
        for ans in answers:
            letter = ans.get('letter', '')
            content = ans.get('content', '')
            prompt += f"{letter}. {content}\n"
        
        prompt += """Based on your knowledge, which answer is most likely correct?
Respond with ONLY the letter (A, B, C, or D) without explanation."""
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str, valid_options: List[str]) -> Optional[str]:
        """Parse Gemini response to extract answer letter."""
        # Clean response
        response_text = response_text.strip().upper()
        
        # Look for first valid letter
        for char in response_text:
            if char in valid_options:
                return char
        
        # If no valid letter found, return None
        return None


# Global service instance
_gemini_service = None


def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service


def analyze_quiz_with_ai(questions: List[Dict]) -> Dict:
    """Convenience function to analyze quiz."""
    service = get_gemini_service()
    return service.analyze_quiz(questions)
