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

def calculate_company_insights(df):
    pass
    
def rank_companies(company_df):
    company_df = company_df.sort_values(
        by="company_intelligence_score",
        ascending=False
    ).reset_index(drop=True)

    company_df["rank"] = (
        company_df.index + 1
    )
    return company_df