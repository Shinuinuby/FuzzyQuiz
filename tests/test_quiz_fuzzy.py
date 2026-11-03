
from quiz_engine import evaluate_quiz
from fuzzy_engine import recommend_difficulty

# Simple sample questions
questions = [
    {
        "question": f"Question {i + 1}",
        "answer": answer,
        "explanation": "Sample explanation"
    }
    for i, answer in enumerate([2, 1, 2, 1, 0])
]

answers = [2, 0, 2, 1, 0]

response_times = [10, 15, 12, 8, 15]

# STEP 1: Evaluate quiz
result = evaluate_quiz(
    questions,
    answers,
    response_times
)

# STEP 2: Send results to fuzzy engine
fuzzy_result = recommend_difficulty(
    result["accuracy"],
    result["average_time"]
)

# STEP 3: Display results
print("QUIZ PERFORMANCE")
print("------------------------")
print(f"Score: {result['score']}/{result['total_questions']}")
print(f"Accuracy: {result['accuracy']}%")
print(f"Average Time: {result['average_time']} seconds")

print("\nFUZZY LOGIC RESULT")
print("------------------------")
print(f"Fuzzy Score: {fuzzy_result['fuzzy_score']}")
print(f"Recommended Difficulty: {fuzzy_result['difficulty']}")
