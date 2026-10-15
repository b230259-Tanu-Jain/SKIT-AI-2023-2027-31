import pandas as pd
from features.company_data.mongodb import companies
from features.recommendation.user_profile import UserProfile
from features.recommendation.recommendation import recommend_companies
def get_rating(prompt):
    while True:
        try:
            value = float(input(prompt))
            if 0 <= value <= 100:
                return value

            print("Enter a value between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")
def main():
    print("\n=== WorkSphere Personalised Recommendation ===\n")

    skills = input(
        "Enter your skills separated by commas: "
    )
    profile = UserProfile(
        skills=skills,
        work_life_balance=get_rating(
            "Desired work-life balance (0-100): "
        ),
        culture_values=get_rating(
            "Desired culture rating (0-100): "
        ),
        career_opp=get_rating(
            "Desired career opportunities (0-100): "
        ),
        comp_benefits=get_rating(
            "Desired compensation and benefits (0-100): "
        )
    )

    company_df = pd.DataFrame(
        list(companies.find({}, {"_id": 0}))
    )

    if company_df.empty:
        print("No company data found in MongoDB.")
        return

    results = recommend_companies(
        company_df, profile, top_n=5
    )

    if results.empty:
        print("No companies have valid intelligence scores.")
        return

    print("\n--- Top 5 Recommended Companies ---\n")

    display_columns = [
        "firm",
        "company_intelligence_score",
        "preference_score",
        "recommendation_score"
    ]
    display_columns = [
        column for column in display_columns
        if column in results.columns
    ]
    print(
        results[display_columns].to_string(index=False)
    )
if __name__ == "__main__":
    main()
