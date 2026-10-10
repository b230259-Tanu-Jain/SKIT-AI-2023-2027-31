import pandas as pd


RATING_COLUMNS = {
    "overall_rating": "Overall Rating",
    "work_life_balance": "Work-Life Balance",
    "culture_values": "Culture & Values",
    "diversity_inclusion": "Diversity & Inclusion",
    "career_opp": "Career Opportunities",
    "comp_benefits": "Compensation & Benefits",
    "senior_mgmt": "Senior Management"
}
MIN_REVIEWS = 10
def calculate_company_insights(df):
    df = df.copy()
    # Convert BERT star score to 0-100 scale
    df["bert_score"] = (
        (df["bert_star_score"] - 1) / 4 * 100
    )
    available_ratings = [
        column
        for column in RATING_COLUMNS
        if column in df.columns
    ]

    grouped = df.groupby("firm")

    company_df = grouped[available_ratings].mean()

    # Average BERT sentiment score
    company_df["bert_sentiment_score"] = (
        grouped["bert_score"].mean()
    )

    # Number of reviews
    company_df["review_count"] = grouped.size()

    company_df = company_df.reset_index()

    # Remove companies with too few reviews
    company_df = company_df[
        company_df["review_count"] >= MIN_REVIEWS
    ].copy()

    # Convert ratings from 1-5 to 0-100
    for column in available_ratings:
        company_df[column] = (
            company_df[column] / 5 * 100
        )

    # Average structured rating
    company_df["rating_score"] = (
        company_df[available_ratings]
        .mean(axis=1)
    )

    # Final Company Intelligence Score
    company_df["company_intelligence_score"] = (
        company_df["rating_score"] * 0.60
        + company_df["bert_sentiment_score"] * 0.40
    )

    # Round scores
    company_df["company_intelligence_score"] = (
        company_df["company_intelligence_score"]
        .round(2)
    )

    company_df["rating_score"] = (
        company_df["rating_score"]
        .round(2)
    )

    company_df["bert_sentiment_score"] = (
        company_df["bert_sentiment_score"]
        .round(2)
    )

    return company_df


def rank_companies(company_df):
    company_df = company_df.sort_values(
        by=[
            "company_intelligence_score",
            "review_count"
        ],
        ascending=[
            False,
            False
        ]
    ).reset_index(drop=True)

    company_df["rank"] = (
        company_df.index + 1
    )

    return company_df