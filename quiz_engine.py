
def evaluate_quiz(questions, answers, response_times):
    """
    Evaluate a completed multiple-choice quiz.

    questions: List of generated questions
    answers: List of selected answer indexes (0-3)
    response_times: List of seconds per question
    """

    if not questions:
        raise ValueError("Quiz must contain questions.")

    if len(questions) != len(answers):
        raise ValueError(
            "Number of answers does not match questions."
        )

    if len(questions) != len(response_times):
        raise ValueError(
            "Number of response times does not match questions."
        )

    correct_count = 0
    answer_review = []

    for i, question in enumerate(questions):

        correct_answer = question["answer"]
        student_answer = answers[i]
        time_taken = response_times[i]

        if type(correct_answer) is not int or correct_answer not in range(4):
            raise ValueError("Invalid correct answer index.")

        if (
            student_answer is not None
            and (
                type(student_answer) is not int
                or student_answer not in range(4)
            )
        ):
            raise ValueError("Invalid student answer.")

        if (
            not isinstance(time_taken, (int, float))
            or isinstance(time_taken, bool)
            or not 0 <= time_taken < float("inf")
        ):
            raise ValueError("Invalid response time.")

        is_correct = student_answer == correct_answer

        if is_correct:
            correct_count += 1

        answer_review.append({
            "question": question["question"],
            "student_answer": student_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "time_taken": round(time_taken, 2),
            "explanation": question["explanation"]
        })

    total_questions = len(questions)

    accuracy = (
        correct_count / total_questions
    ) * 100

    average_time = (
        sum(response_times) / total_questions
    )

    return {
        "score": correct_count,
        "total_questions": total_questions,
        "accuracy": round(accuracy, 2),
        "average_time": round(average_time, 2),
        "answer_review": answer_review
    }
