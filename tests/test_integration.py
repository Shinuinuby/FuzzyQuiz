
print("FUZZYQUIZ INTEGRATION TEST")
print("--------------------------")

try:
    from ai_generator import generate_questions
    print("[PASS] AI Generator")

    from file_processor import extract_text
    print("[PASS] File Processor")

    from fuzzy_engine import recommend_difficulty
    print("[PASS] Fuzzy Logic Engine")

    from quiz_engine import evaluate_quiz
    print("[PASS] Quiz Evaluation Engine")

    import streamlit
    print("[PASS] Streamlit")

    print("\nAll modules imported successfully!")

except Exception as error:
    print("\n[FAIL] Integration error:")
    print(error)
    raise
