import pandas as pd
PREFERENCE_WEIGHT = 0.30
INTELLIGENCE_WEIGHT = 0.70
def calculate_preference_score(row, preferences):
    scores = []

    for attribute, desired_rating in preferences.items():
        if attribute not in row.index:
            continue

        actual_rating = pd.to_numeric(
            row[attribute], errors="coerce"
        )

        if pd.notna(actual_rating):
            actual_rating = max(0, min(100, actual_rating))
            scores.append(
                100 - abs(actual_rating - desired_rating)
            )

    return sum(scores) / len(scores) if scores else 0

def recommend_companies(company_df, user_profile, top_n=5):
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    if "company_intelligence_score" not in company_df.columns:
        raise ValueError(
            "Missing company_intelligence_score column."
        )

    df = company_df.copy()
    df["company_intelligence_score"] = pd.to_numeric(
        df["company_intelligence_score"], errors="coerce"
    )
    df = df.dropna(
        subset=["company_intelligence_score"]
    ).copy()
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

    return df.sort_values(
        ["recommendation_score", "review_count"]
        if "review_count" in df.columns
        else ["recommendation_score"],
        ascending=False
    ).head(top_n).reset_index(drop=True)
