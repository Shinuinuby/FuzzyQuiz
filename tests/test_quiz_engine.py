
import unittest

from quiz_engine import evaluate_quiz


class TestQuizEngine(unittest.TestCase):

    def setUp(self):
        self.questions = [
            {
                "question": f"Question {i + 1}",
                "answer": i % 4,
                "explanation": "Sample explanation"
            }
            for i in range(5)
        ]

    def test_all_correct(self):
        answers = [0, 1, 2, 3, 0]
        times = [10, 10, 10, 10, 10]

        result = evaluate_quiz(
            self.questions, answers, times
        )

        self.assertEqual(result["score"], 5)
        self.assertEqual(result["accuracy"], 100)
        self.assertEqual(result["average_time"], 10)

    def test_all_incorrect(self):
        answers = [1, 2, 3, 0, 1]
        times = [10, 10, 10, 10, 10]

        result = evaluate_quiz(
            self.questions, answers, times
        )

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["accuracy"], 0)

    def test_partial_score(self):
        answers = [0, 1, 2, 0, 1]
        times = [5, 10, 15, 10, 10]

        result = evaluate_quiz(
            self.questions, answers, times
        )

        self.assertEqual(result["score"], 3)
        self.assertEqual(result["accuracy"], 60)
        self.assertEqual(result["average_time"], 10)

    def test_skipped_question(self):
        answers = [0, None, 2, 3, 0]
        times = [10, 10, 10, 10, 10]

        result = evaluate_quiz(
            self.questions, answers, times
        )

        self.assertEqual(result["score"], 4)
        self.assertEqual(result["accuracy"], 80)

    def test_invalid_answer_count(self):
        with self.assertRaises(ValueError):
            evaluate_quiz(
                self.questions,
                [0, 1],
                [10, 10]
            )

    def test_negative_response_time(self):
        with self.assertRaises(ValueError):
            evaluate_quiz(
                self.questions,
                [0, 1, 2, 3, 0],
                [10, -5, 10, 10, 10]
            )


if __name__ == "__main__":
    unittest.main()
