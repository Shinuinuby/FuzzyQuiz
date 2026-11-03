
import json
from ollama import chat


# ---------------------------------------
# 1. AI MODEL CONFIGURATION
# ---------------------------------------

MODEL = "qwen3:4b-instruct"


# ---------------------------------------
# 2. GENERATE QUESTIONS
# ---------------------------------------

def generate_questions(
    source_text,
    difficulty,
    count,
    source_type="topic"
):
    """
    Generate multiple-choice questions using Qwen.

    Parameters:
        source_text: Topic or extracted lesson text
        difficulty: Easy, Medium, or Hard
        count: 5 or 10
        source_type: "topic" or "lesson"

    Returns:
        List of validated multiple-choice questions
    """

    # ---------------------------------------
    # 3. VALIDATE USER INPUT
    # ---------------------------------------

    if not isinstance(source_text, str) or not source_text.strip():
        raise ValueError(
            "Please provide a topic or lesson."
        )

    if difficulty not in ["Easy", "Medium", "Hard"]:
        raise ValueError(
            "Difficulty must be Easy, Medium, or Hard."
        )

    if type(count) is not int or count not in [5, 10]:
        raise ValueError(
            "Question count must be 5 or 10."
        )

    if source_type not in ["topic", "lesson"]:
        raise ValueError(
            "Source type must be 'topic' or 'lesson'."
        )

    # ---------------------------------------
    # 4. DEFINE SOURCE INSTRUCTIONS
    # ---------------------------------------

    if source_type == "lesson":
        source_instruction = (
            "Generate questions using ONLY the lesson "
            "material provided below. Do not introduce "
            "facts that are not supported by the lesson."
        )

    else:
        source_instruction = (
            "Generate questions about the topic "
            "provided below."
        )

    # ---------------------------------------
    # 5. DEFINE DIFFICULTY INSTRUCTIONS
    # ---------------------------------------

    difficulty_instructions = {
        "Easy": (
            "Create basic questions that test simple "
            "facts, definitions, and understanding."
        ),

        "Medium": (
            "Create questions that test understanding "
            "and the application of concepts."
        ),

        "Hard": (
            "Create challenging questions that require "
            "analysis, reasoning, or problem-solving."
        )
    }

    # ---------------------------------------
    # 6. CREATE AI PROMPT
    # ---------------------------------------

    prompt = f"""
You are an educational multiple-choice quiz generator.

TASK:
Generate exactly {count} {difficulty} multiple-choice
questions.

SOURCE INSTRUCTION:
{source_instruction}

DIFFICULTY INSTRUCTION:
{difficulty_instructions[difficulty]}

TOPIC OR LESSON:
{source_text}

QUESTION REQUIREMENTS:
1. Generate exactly {count} questions.
2. Each question must have exactly four choices.
3. Only one choice must be correct.
4. Each question must have a short explanation.
5. Avoid duplicate questions.
6. Avoid duplicate answer choices.
7. Match the requested difficulty.
8. Make the questions clear and understandable.
9. Do not reveal the correct answer in the question text.
10. Use the same language as the topic or lesson.

OUTPUT FORMAT:
Return a valid JSON object containing a "questions" array.

Each question must have these fields:

- "question": Question text
- "options": Array containing four answer choices
- "answer": Correct answer index (0, 1, 2, or 3)
- "explanation": Short explanation of the answer

EXAMPLE JSON STRUCTURE:

{{
    "questions": [
        {{
            "question": "Which keyword defines a function in Python?",
            "options": [
                "function",
                "define",
                "def",
                "func"
            ],
            "answer": 2,
            "explanation": "Python uses the def keyword."
        }}
    ]
}}

IMPORTANT:
- Return JSON only.
- Do not include Markdown formatting.
- Do not include text outside the JSON object.
- The "answer" value must be an integer from 0 to 3.
"""

    # ---------------------------------------
    # 7. SEND REQUEST TO OLLAMA
    # ---------------------------------------

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an educational quiz generator. "
                    "Follow the requested JSON structure "
                    "and return valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json",
        options={
                "temperature": 0.2,
                "num_predict": 1500,
                "num_thread": 6
        }
    )

    # ---------------------------------------
    # 8. CONVERT AI RESPONSE TO JSON
    # ---------------------------------------

    data = json.loads(response.message.content)

    if not isinstance(data, dict):
        raise ValueError(
            "AI output must be a JSON object."
        )

    questions = data.get("questions")

    if not isinstance(questions, list):
        raise ValueError(
            "Missing questions list."
        )

    if len(questions) != count:
        raise ValueError(
            f"Expected {count} questions, "
            f"but received {len(questions)}."
        )

    # ---------------------------------------
    # 9. VALIDATE GENERATED QUESTIONS
    # ---------------------------------------

    seen_questions = set()

    for q in questions:

        # Check question object
        if not isinstance(q, dict):
            raise ValueError(
                "Invalid question object."
            )

        # Check required fields
        required = [
            "question",
            "options",
            "answer",
            "explanation"
        ]

        if any(key not in q for key in required):
            raise ValueError(
                "Missing question field."
            )

        # Check question text
        if (
            not isinstance(q["question"], str)
            or not q["question"].strip()
        ):
            raise ValueError(
                "Question text is empty."
            )

        # Check answer choices
        if (
            not isinstance(q["options"], list)
            or len(q["options"]) != 4
            or any(
                not isinstance(option, str)
                or not option.strip()
                for option in q["options"]
            )
        ):
            raise ValueError(
                "Invalid options."
            )

        # Check duplicate answer choices
        normalized_options = [
            option.strip().casefold()
            for option in q["options"]
        ]

        if len(set(normalized_options)) != 4:
            raise ValueError(
                "Duplicate answer choices."
            )

        # Check correct answer index
        if (
            type(q["answer"]) is not int
            or q["answer"] not in range(4)
        ):
            raise ValueError(
                "Invalid correct answer."
            )

        # Check explanation
        if (
            not isinstance(q["explanation"], str)
            or not q["explanation"].strip()
        ):
            raise ValueError(
                "Missing explanation."
            )

        # Check duplicate questions
        normalized_question = (
            q["question"].strip().casefold()
        )

        if normalized_question in seen_questions:
            raise ValueError(
                "Duplicate question."
            )

        seen_questions.add(
            normalized_question
        )

    # ---------------------------------------
    # 10. RETURN VALIDATED QUESTIONS
    # ---------------------------------------

    return questions
