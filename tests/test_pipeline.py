import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src import analyze_jobs


class SkillSummaryPipelineTests(unittest.TestCase):
    def _run_with_skills(self, skills):
        count = len(skills)
        source = pd.DataFrame({
            "job_title_short": ["Data Analyst"] * count,
            "salary_year_avg": [50000] * count,
            "salary_hour_avg": [30] * count,
            "job_work_from_home": [False] * count,
            "job_no_degree_mention": [False] * count,
            "job_health_insurance": [False] * count,
            "job_country": ["United Kingdom"] * count,
            "job_posted_date": ["2026-01-01"] * count,
            "job_skills": skills,
        })
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "insights"
            with patch.object(analyze_jobs.pd, "read_excel", return_value=source):
                with patch.object(analyze_jobs, "OUTPUT_DIR", out):
                    analyze_jobs.main()
            summary = pd.read_csv(out / "skill_salary_summary.csv")
            self.assertEqual(len(list(out.glob("*.csv"))), 5)
            return summary

    def test_no_qualifying_skill_produces_header_only_csv(self):
        result = self._run_with_skills(["['python']", "['sql']", "[]"])
        self.assertTrue(result.empty)
        self.assertEqual(result.columns.tolist(), ["skill", "job_count", "median_year_salary", "median_hour_salary"])

    def test_qualifying_skill_is_still_reported(self):
        result = self._run_with_skills(["['python']"] * 500)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.loc[0, "skill"], "python")
        self.assertEqual(result.loc[0, "job_count"], 500)


if __name__ == "__main__":
    unittest.main()
