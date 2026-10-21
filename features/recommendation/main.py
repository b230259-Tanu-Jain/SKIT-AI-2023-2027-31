import pandas as pd
from features.company_data.mongodb import companies, job_roles
from features.recommendation.user_profile import UserProfile
from features.recommendation.recommendation import (
    recommend_companies,
    recommend_job_roles
)
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

    skills = input("Enter your skills separated by commas: ")

    profile = UserProfile(
        skills=skills,
        work_life_balance=get_rating("Desired work-life balance (0-100): "),
        culture_values=get_rating("Desired culture rating (0-100): "),
        career_opp=get_rating("Desired career opportunities (0-100): "),
        comp_benefits=get_rating("Desired compensation and benefits (0-100): ")
    )

    company_df = pd.DataFrame(list(companies.find({}, {"_id": 0})))

    if company_df.empty:
        print("No company data found in MongoDB.")
    else:
        results = recommend_companies(company_df, profile, top_n=5)

        if results.empty:
            print("No companies have valid intelligence scores.")
        else:
            columns = [
                "firm", "company_intelligence_score",
                "preference_score", "recommendation_score"
            ]
            columns = [col for col in columns if col in results.columns]

            print("\n--- Top 5 Recommended Companies ---\n")
            print(results[columns].to_string(index=False))

    job_df = pd.DataFrame(list(job_roles.find({}, {"_id": 0})))

    if job_df.empty:
        print("\nNo job-role data found in MongoDB.")
        return

    role_results = recommend_job_roles(job_df, profile, top_n=5)

    role_columns = [
        col for col in [
            "job_role", "role", "title",
            "skill_match_score", "matched_skills", "missing_skills"
        ]
        if col in role_results.columns
    ]
    print("\n--- Top 5 Job-Role Matches ---\n")
    if role_results.empty:
        print("No matching job roles found.")
    elif not role_columns:
        print("No recognized job-role display columns found.")
        print(role_results.to_string(index=False))
    else:
        print(role_results[role_columns].to_string(index=False))

if __name__ == "__main__":
    main()
