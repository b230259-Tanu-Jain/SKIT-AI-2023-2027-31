import pandas as pd
def calculate_preference_score(row, preferences):
    score = 0
    total_weight = 0

    for attribute, weight in preferences.items():

        if attribute in row.index:
            value = pd.to_numeric(
                row[attribute],
                errors="coerce"
            )

            if pd.notna(value):
                score += value * weight
                total_weight += weight

    if total_weight == 0:
        return 0
    return score / total_weight
def recommend_companies(
    company_df,
    user_profile,
    top_n=5
):
    df = company_df.copy()

    preferences = user_profile.get_preferences()

    df["preference_score"] = df.apply(
        lambda row: calculate_preference_score(
            row,
            preferences
        ),
        axis=1
    )

    df["recommendation_score"] = (
        df["company_intelligence_score"] * 0.7
        + df["preference_score"] * 0.3
    )

    df = df.sort_values(
        "recommendation_score",
        ascending=False
    )

    return df.head(top_n)