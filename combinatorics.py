"""
Combinatorics module for generating shuffled quiz variations.
Uses combinatorial math to ensure low duplication between variations.
"""

import random
from typing import List, Dict
from math import factorial
from itertools import permutations


class QuizShuffler:
    """
    Handles shuffling of questions and answers to create quiz variations.
    Uses combinatorics to calculate possible variations and generate unique sets.
    """
    
    def __init__(self, questions: List[Dict]):
        """
        Initialize shuffler with questions.
        
        Args:
            questions: List of question dictionaries with structure:
                      {
                          'question_number': int,
                          'question_text': str,
                          'answers': [
                              {'letter': 'A', 'content': str},
                              {'letter': 'B', 'content': str},
                              ...
                          ]
                      }
        """
        self.questions = questions
        self.total_questions = len(questions)
        self._calculate_variation_count()
    
    def _calculate_variation_count(self):
        """Calculate theoretical maximum number of unique quiz variations."""
        if self.total_questions == 0:
            self.max_variations = 0
            self.question_permutations = 0
            self.answer_permutations = 0
            return
        
        # Calculate question permutations: n!
        self.question_permutations = factorial(self.total_questions)
        
        # Calculate answer permutations for each question
        # Each question can have answers shuffled: m! where m is number of answers
        self.answer_permutations = 1
        for question in self.questions:
            num_answers = len(question.get('answers', []))
            self.answer_permutations *= factorial(num_answers)
        
        # Total possible variations
        self.max_variations = self.question_permutations * self.answer_permutations
    
    def get_variation_info(self) -> Dict:
        """
        Get information about possible quiz variations.
        
        Returns:
            Dictionary with variation statistics
        """
        return {
            'total_questions': self.total_questions,
            'question_permutations': self.question_permutations,
            'answer_permutations': self.answer_permutations,
            'max_variations': self.max_variations,
            'formula': f"{self.total_questions}! × (answer_permutations) = {self.max_variations}"
        }
    
    def shuffle_answers(self, question: Dict) -> Dict:
        """
        Shuffle answers within a question while preserving structure.
        
        Args:
            question: A single question dictionary
            
        Returns:
            Question with shuffled answers
        """
        shuffled_question = question.copy()
        answers = shuffled_question.get('answers', []).copy()
        
        if len(answers) > 1:
            random.shuffle(answers)
        
        shuffled_question['answers'] = answers
        return shuffled_question
    
    def shuffle_questions(self, questions: List[Dict]) -> List[Dict]:
        """
        Shuffle the order of questions.
        
        Args:
            questions: List of questions to shuffle
            
        Returns:
            Shuffled questions list
        """
        shuffled = questions.copy()
        random.shuffle(shuffled)
        
        # Renumber questions
        for idx, question in enumerate(shuffled, 1):
            question['question_number'] = idx
        
        return shuffled
    
    def generate_variation(self) -> List[Dict]:
        """
        Generate a single variation with shuffled questions and answers.
        
        Returns:
            New question set with both questions and answers shuffled
        """
        # Shuffle question order
        shuffled_questions = self.shuffle_questions(self.questions)
        
        # Shuffle answers for each question
        for question in shuffled_questions:
            question = self.shuffle_answers(question)
        
        return shuffled_questions
    
    def generate_variations(self, count: int) -> List[List[Dict]]:
        """
        Generate multiple unique quiz variations with low duplication guarantee.
        
        Uses a simple but effective strategy:
        - For small counts (< max_variations): Generate random variations
        - Tracks generated variations to minimize duplicates
        
        Args:
            count: Number of variations to generate (1-100)
            
        Returns:
            List of quiz variations, each containing shuffled questions
        """
        if count <= 0:
            return []
        
        if count > self.max_variations:
            # Warn but allow (will have duplicates)
            print(f"Warning: Requested {count} variations but max possible is {self.max_variations}")
            count = self.max_variations
        
        variations = []
        generated_hashes = set()
        
        # Try to generate unique variations
        max_attempts = count * 10  # Allow multiple attempts per variation
        attempts = 0
        
        while len(variations) < count and attempts < max_attempts:
            variation = self.generate_variation()
            
            # Create hash of variation to detect duplicates
            variation_hash = self._hash_variation(variation)
            
            if variation_hash not in generated_hashes:
                variations.append(variation)
                generated_hashes.add(variation_hash)
            
            attempts += 1
        
        if len(variations) < count:
            print(f"Generated {len(variations)} unique variations (requested {count})")
        
        return variations
    
    @staticmethod
    def _hash_variation(questions: List[Dict]) -> str:
        """
        Create a hash representing a quiz variation.
        Used to detect duplicate variations.
        
        Args:
            questions: Question list
            
        Returns:
            Hash string representing this variation
        """
        parts = []
        for q in questions:
            # Question order
            parts.append(str(q['question_number']))
            # Answer order
            for a in q['answers']:
                parts.append(a['letter'])
        
        return '_'.join(parts)
    
    def generate_balanced_variations(
        self,
        count: int,
        seed: int = None
    ) -> List[List[Dict]]:
        """
        Generate balanced variations with controlled randomness.
        
        Args:
            count: Number of variations
            seed: Random seed for reproducibility
            
        Returns:
            List of balanced quiz variations
        """
        if seed is not None:
            random.seed(seed)
        
        return self.generate_variations(count)


def shuffle_quiz(
    questions: List[Dict],
    num_variations: int = 1,
    seed: int = None
) -> List[List[Dict]]:
    """
    Utility function to quickly shuffle quiz questions.
    
    Args:
        questions: Original questions list
        num_variations: Number of variations to create
        seed: Optional random seed for reproducibility
        
    Returns:
        List of shuffled question sets
    """
    shuffler = QuizShuffler(questions)
    return shuffler.generate_balanced_variations(num_variations, seed)
