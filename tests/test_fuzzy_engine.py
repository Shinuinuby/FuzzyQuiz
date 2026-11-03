
import unittest

from fuzzy_engine import recommend_difficulty


class TestFuzzyEngine(unittest.TestCase):

    def test_low_accuracy(self):
        result = recommend_difficulty(20, 45)

        self.assertEqual(
            result["difficulty"], "Easy"
        )

    def test_medium_accuracy(self):
        result = recommend_difficulty(60, 30)

        self.assertEqual(
            result["difficulty"], "Medium"
        )

    def test_high_accuracy_fast(self):
        result = recommend_difficulty(100, 10)

        self.assertEqual(
            result["difficulty"], "Hard"
        )

    def test_high_accuracy_slow(self):
        result = recommend_difficulty(100, 55)

        self.assertEqual(
            result["difficulty"], "Medium"
        )

    def test_invalid_accuracy(self):
        with self.assertRaises(ValueError):
            recommend_difficulty(120, 20)

    def test_negative_time(self):
        with self.assertRaises(ValueError):
            recommend_difficulty(80, -10)

    def test_all_input_ranges(self):
        for accuracy in range(0, 101, 5):
            for seconds in range(0, 61, 5):

                with self.subTest(
                    accuracy=accuracy,
                    seconds=seconds
                ):
                    result = recommend_difficulty(
                        accuracy, seconds
                    )

                    self.assertIn(
                        result["difficulty"],
                        ["Easy", "Medium", "Hard"]
                    )

                    self.assertGreaterEqual(
                        result["fuzzy_score"], 0
                    )

                    self.assertLessEqual(
                        result["fuzzy_score"], 100
                    )


if __name__ == "__main__":
    unittest.main()
