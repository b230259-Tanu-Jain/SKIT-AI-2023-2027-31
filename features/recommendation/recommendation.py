import ast
import pandas as pd
PREFERENCE_WEIGHT = 0.30
INTELLIGENCE_WEIGHT = 0.70

def calculate_preference_score(row, preferences):
    scores = []

    for attribute, desired_rating in preferences.items():
        if attribute not in row.index:
            continue

        actual_rating = pd.to_numeric(row[attribute], errors="coerce")

        if pd.notna(actual_rating):
            actual_rating = max(0, min(100, actual_rating))
            scores.append(100 - abs(actual_rating - desired_rating))

    return sum(scores) / len(scores) if scores else 0


def recommend_companies(company_df, user_profile, top_n=5):
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    if "company_intelligence_score" not in company_df.columns:
        raise ValueError("Missing company_intelligence_score column.")

    df = company_df.copy()
    df["company_intelligence_score"] = pd.to_numeric(
        df["company_intelligence_score"], errors="coerce"
    )
    df = df.dropna(subset=["company_intelligence_score"]).copy()

    if df.empty:
        return df

    df["preference_score"] = df.apply(
        lambda row: calculate_preference_score(
            row, user_profile.get_preferences()
        ),
        axis=1
    )
    df["recommendation_score"] = (
        df["company_intelligence_score"] * INTELLIGENCE_WEIGHT
        + df["preference_score"] * PREFERENCE_WEIGHT
    ).round(2)

    sort_columns = ["recommendation_score"]
    if "review_count" in df.columns:
        df["review_count"] = pd.to_numeric(
            df["review_count"], errors="coerce"
        ).fillna(0)
        sort_columns.append("review_count")

    return df.sort_values(
        sort_columns, ascending=False
    ).head(top_n).reset_index(drop=True)


def _parse_skills(value):
    if isinstance(value, (list, tuple, set)):
        skills = value
    elif isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)
            skills = parsed if isinstance(parsed, (list, tuple, set)) else value.split(",")
        except (ValueError, SyntaxError):
            skills = value.split(",")
    else:
        skills = []

    return {
        str(skill).strip().lower()
        for skill in skills
        if str(skill).strip()
    }


def recommend_job_roles(job_df, user_profile, top_n=5):
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    if "job_skill_set" not in job_df.columns:
        raise ValueError("Missing job_skill_set column.")

    if job_df.empty:
        return job_df.copy()

    user_skills = user_profile.get_skills()
    df = job_df.copy()

    df["required_skills"] = df["job_skill_set"].apply(_parse_skills)
    df["matched_skills"] = df["required_skills"].apply(
        lambda skills: sorted(user_skills & skills)
    )
    df["missing_skills"] = df["required_skills"].apply(
        lambda skills: sorted(skills - user_skills)
    )
    df["skill_match_score"] = df["required_skills"].apply(
        lambda skills: round(
            100 * len(user_skills & skills) / len(skills), 2
        ) if skills else 0
    )

    return df.sort_values(
        ["skill_match_score"], ascending=False
    ).head(top_n).reset_index(drop=True)
