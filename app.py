import time
import streamlit as st

from ai_generator import generate_questions
from file_processor import extract_text
from quiz_engine import evaluate_quiz
from fuzzy_engine import recommend_difficulty


st.set_page_config(page_title="FuzzyQuiz", layout="centered")

# -------------------- SESSION STATE --------------------
defaults = {
    "page": "setup",
    "questions": [],
    "question_index": 0,
    "answers": [],
    "response_times": [],
    "question_start": None,
    "result": None,
    "fuzzy_result": None,
    "source_text": "",
    "source_type": "topic",
    "difficulty": "Easy",
    "count": 5,
    "round_number": 1,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_quiz():
    for key, value in defaults.items():
        st.session_state[key] = value
    st.rerun()


def start_quiz(questions, source_text, source_type, difficulty, count, round_number=1):
    st.session_state.questions = questions
    st.session_state.source_text = source_text
    st.session_state.source_type = source_type
    st.session_state.difficulty = difficulty
    st.session_state.count = count
    st.session_state.round_number = round_number
    st.session_state.question_index = 0
    st.session_state.answers = []
    st.session_state.response_times = []
    st.session_state.question_start = None
    st.session_state.result = None
    st.session_state.fuzzy_result = None
    st.session_state.page = "quiz"
    st.rerun()


def submit_answer(answer_index):
    index = st.session_state.question_index
    elapsed = time.perf_counter() - st.session_state.question_start

    st.session_state.answers.append(answer_index)
    st.session_state.response_times.append(elapsed)

    if index + 1 < len(st.session_state.questions):
        st.session_state.question_index += 1
        st.session_state.question_start = None
        st.rerun()
    else:
        result = evaluate_quiz(
            st.session_state.questions,
            st.session_state.answers,
            st.session_state.response_times,
        )
        fuzzy_result = recommend_difficulty(
            result["accuracy"], result["average_time"]
        )
        st.session_state.result = result
        st.session_state.fuzzy_result = fuzzy_result
        st.session_state.page = "results"
        st.rerun()


# -------------------- HEADER --------------------
st.title("FuzzyQuiz")


# -------------------- CREATE QUIZ --------------------
if st.session_state.page == "setup":
    st.subheader("Create a quiz")

    source_choice = st.radio(
        "Study material",
        ["Topic", "Upload lesson"],
        horizontal=True,
    )

    source_text = ""
    source_type = "topic"

    if source_choice == "Topic":
        source_text = st.text_input(
            "Enter a topic", placeholder="Example: Python programming"
        )
    else:
        source_type = "lesson"
        uploaded_file = st.file_uploader(
            "Choose a lesson file", type=["pdf", "docx", "txt"], max_upload_size=10
        )
        if uploaded_file is not None:
            try:
                source_text = extract_text(uploaded_file)
                st.success("Lesson ready")
            except Exception as error:
                st.error(f"Unable to read file: {error}")

    col1, col2 = st.columns(2)
    with col1:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    with col2:
        count = st.selectbox("Questions", [5, 10])

    if st.button("Generate quiz", type="primary", use_container_width=True):
        if not source_text.strip():
            st.warning("Enter a topic or upload a valid lesson first.")
        else:
            try:
                with st.spinner("Generating questions. This may take a while..."):
                    questions = generate_questions(
                        source_text, difficulty, count, source_type=source_type
                    )
                start_quiz(questions, source_text, source_type, difficulty, count)
            except Exception as error:
                st.error(f"Quiz generation failed: {error}")
                st.caption("Check that Ollama is running and Qwen is installed.")


# -------------------- TAKE QUIZ --------------------
elif st.session_state.page == "quiz":
    questions = st.session_state.questions
    index = st.session_state.question_index
    question = questions[index]

    if st.session_state.question_start is None:
        st.session_state.question_start = time.perf_counter()

    st.caption(
        f"Round {st.session_state.round_number} · {st.session_state.difficulty} · "
        f"Question {index + 1} of {len(questions)}"
    )
    st.progress((index + 1) / len(questions))
    st.subheader(question["question"])

    options = question["options"]
    with st.form(key=f"question_{st.session_state.round_number}_{index}"):
        answer = st.radio(
            "Select your answer",
            options=range(4),
            format_func=lambda i: f"{chr(65 + i)}. {options[i]}",
            index=None,
        )
        button_text = "Submit quiz" if index == len(questions) - 1 else "Next question"
        submitted = st.form_submit_button(
            button_text, type="primary", use_container_width=True
        )

    if submitted:
        if answer is None:
            st.warning("Select an answer to continue.")
        else:
            submit_answer(answer)

    if st.button("Restart quiz"):
        reset_quiz()


# -------------------- RESULTS --------------------
elif st.session_state.page == "results":
    result = st.session_state.result
    fuzzy_result = st.session_state.fuzzy_result

    st.subheader("Your results")
    st.caption(f"Round {st.session_state.round_number}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Score", f"{result['score']}/{result['total_questions']}")
    col2.metric("Accuracy", f"{result['accuracy']}%")
    col3.metric("Avg. time", f"{result['average_time']}s")

    st.divider()
    st.subheader("Recommended next difficulty")
    st.success(fuzzy_result["difficulty"])   

    st.subheader("Answer review")
    for i, review in enumerate(result["answer_review"], start=1):
        label = "Correct" if review["is_correct"] else "Incorrect"
        with st.expander(f"Question {i} · {label}"):
            st.write(review["question"])
            options = st.session_state.questions[i - 1]["options"]
            selected = review["student_answer"]
            correct = review["correct_answer"]
            student_text = "Skipped" if selected is None else f"{chr(65 + selected)}. {options[selected]}"
            correct_text = f"{chr(65 + correct)}. {options[correct]}"
            st.write(f"Your answer: {student_text}")
            st.write(f"Correct answer: {correct_text}")
            st.write(f"Explanation: {review['explanation']}")

    if st.button("Generate next quiz", type="primary", use_container_width=True):
        next_difficulty = fuzzy_result["difficulty"]
        try:
            with st.spinner("Generating your next quiz..."):
                new_questions = generate_questions(
                    st.session_state.source_text,
                    next_difficulty,
                    st.session_state.count,
                    source_type=st.session_state.source_type,
                )
            start_quiz(
                new_questions,
                st.session_state.source_text,
                st.session_state.source_type,
                next_difficulty,
                st.session_state.count,
                st.session_state.round_number + 1,
            )
        except Exception as error:
            st.error(f"Unable to generate the next quiz: {error}")

    if st.button("Create a new quiz", use_container_width=True):
        reset_quiz()

