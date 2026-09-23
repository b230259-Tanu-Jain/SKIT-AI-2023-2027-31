import os
from preprocessing import load_and_prepare_data
from sentiment import BertSentimentAnalyzer
from company_insights import calculate_company_insights, rank_companies
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "glassdoor_reviews.csv"
)
PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)
REVIEW_OUTPUT = os.path.join(
    PROCESSED_DIR,
    "review_sentiment.csv"
)
COMPANY_OUTPUT = os.path.join(
    PROCESSED_DIR,
    "company_insights.csv"
)
