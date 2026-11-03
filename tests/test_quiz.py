
from quiz_engine import evaluate_quiz

# Sample questions
questions = [
    {
        "question": "Which keyword defines a function?",
        "options": ["function", "define", "def", "func"],
        "answer": 2,
        "explanation": "Python uses the def keyword."
    },
    {
        "question": "Which symbol starts a comment?",
        "options": ["//", "#", "/*", "--"],
        "answer": 1,
        "explanation": "Python uses # for comments."
    },
    {
        "question": "Which function displays output?",
        "options": ["input()", "show()", "print()", "display()"],
        "answer": 2,
        "explanation": "print() displays output."
    },
    {
        "question": "Which data type stores True or False?",
        "options": ["str", "bool", "int", "float"],
        "answer": 1,
        "explanation": "bool stores Boolean values."
    },
    {
        "question": "Which keyword creates a loop?",
        "options": ["for", "repeat", "loop", "iterate"],
        "answer": 0,
        "explanation": "for is used to create loops."
    }
]

# Student's selected answers
# Index: 0=A, 1=B, 2=C, 3=D
answers = [2, 0, 2, 1, 0]

# Time spent on each question
response_times = [10, 15, 12, 8, 15]

result = evaluate_quiz(
    questions,
    answers,
    response_times
)

print("QUIZ RESULTS")
print("---------------------")
print(f"Score: {result['score']}/{result['total_questions']}")
print(f"Accuracy: {result['accuracy']}%")
print(f"Average Time: {result['average_time']} seconds")

print("\nANSWER REVIEW")

for i, review in enumerate(
    result["answer_review"],
    start=1
):
    status = "Correct" if review["is_correct"] else "Incorrect"

    print(f"Question {i}: {status}")
    print(f"Time: {review['time_taken']} seconds")
