import ast
import collections
import itertools
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "job_postings_monthly.xlsx"
OUTPUT_DIR = ROOT / "insights"


def parse_list(value):
    if isinstance(value, list):
        return value
    if pd.isna(value):
        return []
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, list):
            return [str(x).strip().lower() for x in parsed if str(x).strip()]
    except Exception:
        pass
    return []


def main():
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    df = pd.read_excel(DATA_FILE)
    df["job_posted_date"] = pd.to_datetime(df["job_posted_date"], errors="coerce")
    df["skills_list"] = df["job_skills"].apply(parse_list)

    role_summary = (
        df.groupby("job_title_short")
        .agg(
            job_count=("job_title_short", "size"),
            median_year_salary=("salary_year_avg", "median"),
            median_hour_salary=("salary_hour_avg", "median"),
            remote_pct=("job_work_from_home", "mean"),
            no_degree_pct=("job_no_degree_mention", "mean"),
            health_insurance_pct=("job_health_insurance", "mean"),
        )
        .sort_values("job_count", ascending=False)
        .reset_index()
    )
    role_summary.to_csv(OUTPUT_DIR / "role_summary.csv", index=False)

    skill_counts = collections.Counter(itertools.chain.from_iterable(df["skills_list"]))
    top_skills = pd.DataFrame(skill_counts.items(), columns=["skill", "job_count"])
    if not top_skills.empty:
        top_skills = top_skills.sort_values("job_count", ascending=False)
    top_skills.to_csv(OUTPUT_DIR / "top_skills.csv", index=False)

    skill_salary_rows = []
    for skill, count in skill_counts.items():
        if count < 500:
            continue
        mask = df["skills_list"].apply(lambda values, s=skill: s in values)
        skill_salary_rows.append(
            {
                "skill": skill,
                "job_count": int(count),
                "median_year_salary": df.loc[mask, "salary_year_avg"].median(),
                "median_hour_salary": df.loc[mask, "salary_hour_avg"].median(),
            }
        )
    skill_salary_summary = pd.DataFrame(skill_salary_rows, columns=["skill", "job_count", "median_year_salary", "median_hour_salary"])
    if not skill_salary_summary.empty:
        skill_salary_summary = skill_salary_summary.sort_values(["job_count", "median_year_salary"], ascending=[False, False])
    skill_salary_summary.to_csv(OUTPUT_DIR / "skill_salary_summary.csv", index=False)

    country_summary = (
        df.groupby("job_country")
        .agg(
            job_count=("job_country", "size"),
            median_year_salary=("salary_year_avg", "median"),
            remote_pct=("job_work_from_home", "mean"),
        )
        .query("job_count >= 200")
        .sort_values("job_count", ascending=False)
        .reset_index()
    )
    country_summary.to_csv(OUTPUT_DIR / "country_summary.csv", index=False)

    posting_trend = (
        df.groupby(df["job_posted_date"].dt.to_period("D"))
        .size()
        .rename("job_count")
        .reset_index()
    )
    posting_trend["job_posted_date"] = posting_trend["job_posted_date"].astype(str)
    posting_trend.to_csv(OUTPUT_DIR / "posting_trend_daily.csv", index=False)

    print("Analysis files created in insights/")


if __name__ == "__main__":
    main()
