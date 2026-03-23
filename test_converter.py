"""
Quick test script to verify converter functionality
"""

from converter import parse_html_to_text_and_doc, QuizParser, QuizConverter

# Sample HTML for testing
SAMPLE_HTML = """
<div class="que multichoice">
    <div class="content">
        <div class="qtext">
            <p>What is Python?</p>
        </div>
    </div>
    <div class="answer">
        <div>
            <span class="answernumber">A.</span>
            <div class="flex-fill">A programming language</div>
        </div>
        <div>
            <span class="answernumber">B.</span>
            <div class="flex-fill">A type of snake</div>
        </div>
        <div>
            <span class="answernumber">C.</span>
            <div class="flex-fill">A software tool</div>
        </div>
    </div>
</div>

<div class="que multichoice">
    <div class="content">
        <div class="qtext">
            <p>What does HTML stand for?</p>
        </div>
    </div>
    <div class="answer">
        <div>
            <span class="answernumber">A.</span>
            <div class="flex-fill">Hyper Text Markup Language</div>
        </div>
        <div>
            <span class="answernumber">B.</span>
            <div class="flex-fill">High Tech Modern Language</div>
        </div>
        <div>
            <span class="answernumber">C.</span>
            <div class="flex-fill">Home Tool Markup Language</div>
        </div>
    </div>
</div>
"""


def test_parser():
    """Test HTML parser"""
    print("Testing HTML Parser...")
    parser = QuizParser()
    questions = parser.parse_questions(SAMPLE_HTML)
    
    print(f"✓ Found {len(questions)} questions\n")
    
    for q in questions:
        print(f"Câu {q['question_number']}: {q['question_text'][:50]}...")
        for a in q['answers']:
            print(f"  {a['letter']}. {a['content'][:40]}...")
        print()
    
    return questions


def test_converter(questions):
    """Test converter"""
    print("\nTesting Converter...")
    converter = QuizConverter()
    
    # Text conversion
    text = converter.to_plain_text(questions)
    print("✓ Text conversion successful")
    print(f"  Output length: {len(text)} characters\n")
    
    # Word conversion
    doc = converter.to_word_document(questions)
    print("✓ Word document conversion successful")
    print(f"  Paragraphs: {len(doc.paragraphs)}\n")


def test_combinatorics():
    """Test combinatorics"""
    print("Testing Combinatorics...")
    from combinatorics import QuizShuffler
    
    parser = QuizParser()
    questions = parser.parse_questions(SAMPLE_HTML)
    
    shuffler = QuizShuffler(questions)
    info = shuffler.get_variation_info()
    
    print(f"✓ Variation info:")
    print(f"  Total questions: {info['total_questions']}")
    print(f"  Max variations: {info['max_variations']}")
    print(f"  Formula: {info['formula']}\n")
    
    # Generate variations
    variations = shuffler.generate_variations(3)
    print(f"✓ Generated {len(variations)} variations")


def test_end_to_end():
    """End-to-end test"""
    print("\nTesting End-to-End Conversion...")
    text, doc, count = parse_html_to_text_and_doc(SAMPLE_HTML)
    
    print(f"✓ Questions parsed: {count}")
    print(f"✓ Text output: {len(text)} characters")
    print(f"✓ Document created with {len(doc.paragraphs)} paragraphs")


if __name__ == "__main__":
    print("=" * 50)
    print("Quiz Converter Test Suite")
    print("=" * 50 + "\n")
    
    try:
        questions = test_parser()
        test_converter(questions)
        test_combinatorics()
        test_end_to_end()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
    
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
