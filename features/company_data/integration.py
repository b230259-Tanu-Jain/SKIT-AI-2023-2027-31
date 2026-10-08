import os
import pandas as pd
from .mongodb import (
    companies,
    reviews,
    job_roles
)
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)
def store_companies():
    file = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "company_insights.csv"
    )
    if not os.path.exists(file):
        print(
            "company_insights.csv not found."
        )
        return

    df = pd.read_csv(file)
    df = df.fillna("")
    records = df.to_dict(
        "records"
    )
    companies.delete_many({})
    if records:
        companies.insert_many(records)
    print(
        f"{len(records)} companies stored."
    )
def store_reviews():
    file = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "review_sentiment.csv"
    )
    if not os.path.exists(file):
        print(
            "review_sentiment.csv not found."
        )
        return

    df = pd.read_csv(file)
    df = df.fillna("")
    records = df.to_dict(
        "records"
    )
    reviews.delete_many({})
    if records:
        reviews.insert_many(records)
    print(
        f"{len(records)} reviews stored."
    )
def store_job_roles():
    file = os.path.join(
        BASE_DIR,
        "data",
        "raw",
        "all_job_post.csv"
    )
    if not os.path.exists(file):
        print(
            "all_job_post.csv not found."
        )
        return

    df = pd.read_csv(file)
    df = df.fillna("")
    records = df.to_dict(
        "records"
    )
    job_roles.delete_many({})
    if records:
        job_roles.insert_many(records)
    print(
        f"{len(records)} job roles stored."
    )
def integrate_data():

    print(
        "\nStoring company data..."
    )
    store_companies()
    print(
        "\nStoring review data..."
    )
    store_reviews()
    print(
        "\nStoring job-role data..."
    )
    store_job_roles()