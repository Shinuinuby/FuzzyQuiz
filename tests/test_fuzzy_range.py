
from fuzzy_engine import recommend_difficulty

errors = []

for accuracy in range(0, 101, 5):
    for seconds in range(0, 61, 5):

        try:
            result = recommend_difficulty(
                accuracy,
                seconds
            )

            if result["difficulty"] not in [
                "Easy", "Medium", "Hard"
            ]:
                errors.append((accuracy, seconds))

        except Exception as error:
            errors.append(
                (accuracy, seconds, str(error))
            )

print("FUZZY RANGE TEST")
print("-------------------------")
print("Test cases:", 21 * 13)
print("Errors:", len(errors))

if errors:
    for error in errors[:20]:
        print(error)
else:
    print("All tested combinations passed!")
