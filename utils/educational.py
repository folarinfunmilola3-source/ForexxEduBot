import random

# Quiz questions database
QUIZ_QUESTIONS = [
    {
        'question': 'What does "Forex" stand for?',
        'options': ['Foreign Exchange', 'Foreign Export', 'Formal Exchange', 'Fixed Exchange'],
        'correct': 'Foreign Exchange'
    },
    {
        'question': 'What is the most traded currency pair?',
        'options': ['GBP/USD', 'USD/JPY', 'EUR/USD', 'AUD/USD'],
        'correct': 'EUR/USD'
    },
    {
        'question': 'What is a pip in Forex?',
        'options': ['Point in Percentage', 'Price Interest Point', 'Percentage in Point', 'Price in Pips'],
        'correct': 'Point in Percentage'
    },
    {
        'question': 'Which session is known as the most volatile?',
        'options': ['Asia Session', 'London Session', 'New York Session', 'Sydney Session'],
        'correct': 'London Session'
    },
    {
        'question': 'What is a stop-loss order?',
        'options': ['Lock in profits', 'Limit losses', 'Open a trade', 'Close all positions'],
        'correct': 'Limit losses'
    }
]

def get_quiz_question():
    """Get a random quiz question."""
    return random.choice(QUIZ_QUESTIONS)

def check_quiz_answer(answer):
    """Check if the quiz answer is correct."""
    for q in QUIZ_QUESTIONS:
        if answer == q['correct']:
            return True
    return False
