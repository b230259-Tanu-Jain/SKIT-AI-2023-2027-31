import os
import pandas as pd
from recommendation import recommend_companies
from user_profile import UserProfile
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
COMPANY_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "company_insights.csv"
)
def main():
    company_df = pd.read_csv(COMPANY_FILE)
    user = UserProfile(
        skills=[
            "Python",
            "SQL",
            "Machine Learning"
        ],
        work_life_balance=5,
        culture_values=5,
        career_opp=4,
        comp_benefits=4
    )
    recommendations = recommend_companies(
        company_df,
        user,
        top_n=5
    )
    columns = [
        "rank",
        "firm",
        "company_intelligence_score",
        "preference_score",
        "recommendation_score"
    ]
    columns = [
        column
        for column in columns
        if column in recommendations.columns
    ]
    print("\nRecommended Companies:\n")
    print(
        recommendations[columns].to_string(
            index=False
        )
    )
if __name__ == "__main__":
    main()