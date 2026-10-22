import unittest

import pandas as pd

from src.analyze_jobs import parse_list


class ParseListTests(unittest.TestCase):
    def test_existing_lists_are_returned_unchanged(self):
        for value in [[], ["Python"], ["Python", "SQL"]]:
            with self.subTest(value=value):
                self.assertIs(parse_list(value), value)

    def test_serialised_lists_are_normalised(self):
        self.assertEqual(parse_list("[' Python ', 'SQL', '', '   ']"), ["python", "sql"])

    def test_missing_values_return_empty_lists(self):
        for value in [None, float("nan"), pd.NA]:
            with self.subTest(value=value):
                self.assertEqual(parse_list(value), [])

    def test_invalid_or_non_list_values_return_empty_lists(self):
        for value in ["broken[", "{'sql': 1}", "('sql',)", "42", 42, True, ""]:
            with self.subTest(value=value):
                self.assertEqual(parse_list(value), [])

    def test_text_is_not_executed(self):
        self.assertEqual(parse_list("__import__('os').getcwd()"), [])


if __name__ == "__main__":
    unittest.main()
