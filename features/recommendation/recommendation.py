import pandas as pd
def recommend_companies(
    company_df,
    user_skills,
    preferred_attributes=None,
    top_n=5
):
    user_skills = {
        skill.strip().lower()
        for skill in user_skills
    }

    if preferred_attributes is None:
        preferred_attributes = {}

    df = company_df.copy()

    # Start with company intelligence score
    df["recommendation_score"] = (
        df["company_intelligence_score"] * 0.7
    )

    # Add preference-based score
    for attribute, weight in preferred_attributes.items():

        if attribute in df.columns:
            values = pd.to_numeric(
                df[attribute],
                errors="coerce"
            )

            if values.notna().any():

                min_value = values.min()
                max_value = values.max()

                if max_value != min_value:

                    normalized = (
                        values - min_value
                    ) / (max_value - min_value)

                    df["recommendation_score"] += (
                        normalized.fillna(0) * weight
                    )

    df = df.sort_values(
        "recommendation_score",
        ascending=False
    )

    return df.head(top_n)