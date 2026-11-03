
from fuzzy_engine import recommend_difficulty

test_cases = [
    (20, 45),
    (50, 30),
    (80, 12),
    (95, 50),
    (70, 25)
]

for accuracy, avg_time in test_cases:

    result = recommend_difficulty(
        accuracy,
        avg_time
    )

    print("\n-------------------------")
    print(f"Accuracy: {accuracy}%")
    print(f"Average Time: {avg_time}s")
    print(f"Fuzzy Score: {result['fuzzy_score']}")
    print(
        f"Next Difficulty: {result['difficulty']}"
    )
