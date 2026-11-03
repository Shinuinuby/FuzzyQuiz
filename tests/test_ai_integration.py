
from ai_generator import generate_questions
from quiz_engine import evaluate_quiz
from fuzzy_engine import recommend_difficulty

print("Generating questions...")

questions = generate_questions(
    "Python Programming",
    "Easy",
    5
)

print(f"Generated {len(questions)} questions.")

# Simulated student answers
# Uses the first option for every question
answers = [0] * len(questions)

# Simulated response times in seconds
response_times = [10, 12, 15, 11, 14]

result = evaluate_quiz(
    questions,
    answers,
    response_times
)

recommendation = recommend_difficulty(
    result["accuracy"],
    result["average_time"]
)

print("\nQUIZ RESULTS")
print("-----------------------")
print(f"Score: {result['score']}/{result['total_questions']}")
print(f"Accuracy: {result['accuracy']}%")
print(f"Average Time: {result['average_time']} seconds")

print("\nFUZZY RECOMMENDATION")
print("-----------------------")
print(f"Next Difficulty: {recommendation['difficulty']}")
print(f"Fuzzy Score: {recommendation['fuzzy_score']}")

print("\nIntegration test completed!")

