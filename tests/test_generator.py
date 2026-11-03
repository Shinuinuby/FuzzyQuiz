
from ai_generator import generate_questions

topic = "Python Programming"
difficulty = "Easy"
count = 5

print("Generating questions. Please wait...\n")

try:
    questions = generate_questions(
        topic,
        difficulty,
        count
    )

    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {q['question']}")

        for j, option in enumerate(q["options"]):
            letter = chr(65 + j)
            print(f"{letter}. {option}")

        answer_index = q["answer"]
        answer_letter = chr(65 + answer_index)

        print(f"Correct Answer: {answer_letter}")
        print(f"Explanation: {q['explanation']}")

except Exception as error:
    print("Error:", error)
