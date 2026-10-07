import os
import pandas as pd
from .mongodb import companies, reviews, job_roles
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

def store_companies():

    file = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "company_insights.csv"
    )
    df = pd.read_csv(file)
    df = df.fillna("")

    companies.delete_many({})

    records = df.to_dict("records")

    if records:
        companies.insert_many(records)

    print(f"{len(records)} companies stored.")

def store_reviews():

    file = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "review_sentiment.csv"
    )
    df = pd.read_csv(file)
    df = df.fillna("")
    reviews.delete_many({})
    records = df.to_dict("records")
    if records:
        reviews.insert_many(records)

    print(f"{len(records)} reviews stored.")

def store_job_roles():

    file = os.path.join(
        BASE_DIR,
        "data",
        "raw",
        "job_roles.csv"
    )

    if not os.path.exists(file):
        print("job_roles.csv not found.")
        return

    df = pd.read_csv(file)
    df = df.fillna("")
    job_roles.delete_many({})
    records = df.to_dict("records")
    if records:
        job_roles.insert_many(records)

    print(f"{len(records)} job-role records stored.")

def integrate_data():

    store_companies()
    store_reviews()
    store_job_roles()