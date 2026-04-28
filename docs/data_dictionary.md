# Data Dictionary

| Column | Description |
|---|---|
| `job_title_short` | Standardized job family used for high-level comparisons. |
| `job_title` | Original job title from the posting. |
| `job_location` | Location string from the source posting. |
| `job_via` | Source platform where the role was found. |
| `job_schedule_type` | Employment type, such as full-time or contractor. |
| `job_work_from_home` | Boolean flag indicating remote/work-from-home availability. |
| `search_location` | Search geography used when collecting the posting. |
| `job_posted_date` | Posting timestamp. |
| `job_no_degree_mention` | Boolean flag indicating the posting did not explicitly mention a degree requirement. |
| `job_health_insurance` | Boolean flag indicating health insurance information was present. |
| `job_country` | Country associated with the posting. |
| `salary_rate` | Salary cadence, typically yearly or hourly. |
| `salary_year_avg` | Average annualized salary in USD where available. |
| `salary_hour_avg` | Average hourly salary in USD where available. |
| `company_name` | Hiring company name. |
| `job_skills` | List-like text field containing extracted skills. |
| `job_type_skills` | JSON-like skill taxonomy grouped by type. |

## Notes
- `job_skills` and `job_type_skills` are semi-structured text fields and should be parsed before analysis.
- Salary fields contain nulls and should be handled carefully when calculating medians or comparisons.
- The provided spreadsheet appears to represent a monthly slice, so timeline claims should be framed accordingly.
