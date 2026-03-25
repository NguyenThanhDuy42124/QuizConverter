"""
Google Gemini AI Service for automatic quiz answer marking.
Supports both real API mode and mock mode for development.
Uses the new google-genai SDK (2025+).
"""

import os
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Try to import Google AI SDK (new)
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    logger.warning("google-genai not installed. Running in mock mode.")


class GeminiService:
    """Service for AI-powered quiz answer analysis using google-genai SDK."""
    
    def __init__(self):
        """Initialize Gemini service with API key from environment."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        self.use_mock_mode = False
        # Try models in order of preference: lightweight → balanced → powerful
        self.models_to_try = [
            "gemini-3.1-flash-lite-preview",  # Latest, ultra-lightweight
            "gemini-2.5-flash-lite",          # Stable, lightweight
            "gemini-2.5-flash",               # Stable, balanced
            "gemini-3.1-flash-preview",       # Newer, more capable
        ]
        
        if self.api_key and HAS_GENAI:
            try:
                # Initialize client with new SDK
                self.client = genai.Client(api_key=self.api_key)
                logger.info(f"✅ Gemini API (google-genai) initialized. Trying models: {', '.join(self.models_to_try)}")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}. Falling back to mock mode.")
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
        if self.use_mock_mode or not self.client:
            return self._mock_analyze(questions)
        
        try:
            return self._real_analyze(questions)
        except Exception as e:
            logger.error(f"Error in real analysis: {e}. Falling back to mock mode.")
            return self._mock_analyze(questions)
    
    def _real_analyze(self, questions: List[Dict]) -> Dict:
        """Perform real analysis using Gemini API with new SDK."""
        predictions = {}
        answers_options = ['A', 'B', 'C', 'D']
        
        for q in questions:
            try:
                question_num = q.get('question_number', q.get('number', 0))
                question_text = q.get('question_text', q.get('text', ''))
                answers = q.get('answers', [])
                
                # Format the question for Gemini
                formatted_prompt = self._format_question_for_gemini(
                    question_text, answers
                )
                
                response = None
                last_error = None
                
                # Try each model until one works
                for model_name in self.models_to_try:
                    try:
                        logger.debug(f"[Q{question_num}] Trying model: {model_name}")
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=formatted_prompt
                        )
                        logger.info(f"✅ [Q{question_num}] Success with model: {model_name}")
                        break
                    except Exception as model_err:
                        last_error = model_err
                        logger.debug(f"❌ [{model_name}] Q{question_num}: {str(model_err)}")
                        continue
                
                # Process response
                if response and hasattr(response, 'text'):
                    predicted_answer = self._parse_gemini_response(
                        response.text, 
                        answers_options
                    )
                    
                    if predicted_answer:
                        predictions[question_num] = predicted_answer
                        logger.debug(f"Q{question_num}: Predicted answer = {predicted_answer}")
                    else:
                        predictions[question_num] = 'A'
                        logger.debug(f"Q{question_num}: No valid prediction, using 'A'")
                else:
                    predictions[question_num] = 'A'
                    if last_error:
                        logger.error(f"Q{question_num}: All models failed. Last error: {str(last_error)}")
                    else:
                        logger.warning(f"Q{question_num}: Empty response from API, using 'A'")
            
            except Exception as e:
                question_num = q.get('question_number', q.get('number', 0))
                logger.error(f"Error analyzing question {question_num}: {e}")
                predictions[question_num] = 'A'
        
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
        prompt = f"""Analyze this multiple choice question and determine the most likely correct answer.

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
