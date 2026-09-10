import pandas as pd
import re


TEXT_COLUMNS = ["headline", "pros", "cons"]

RATING_COLUMNS = [
    "overall_rating",
    "work_life_balance",
    "culture_values",
    "diversity_inclusion",
    "career_opp",
    "comp_benefits",
    "senior_mgmt"
]


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Remove HTML
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_and_prepare_data(file_path):

    df = pd.read_csv(file_path)

    # Make column names consistent
    df.columns = df.columns.str.strip().str.lower()

    required_columns = [
        "firm",
        "headline",
        "pros",
        "cons",
        "overall_rating"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    # Clean company name
    df["firm"] = df["firm"].fillna("").astype(str).str.strip()

    # Clean text columns
    for column in TEXT_COLUMNS:
        df[column] = df[column].apply(clean_text)

    # Combine review text
    df["review_text"] = (
        "Headline: " + df["headline"] +
        " Pros: " + df["pros"] +
        " Cons: " + df["cons"]
    )

    # Remove rows without useful text
    df = df[
        (df["review_text"].str.strip() != "") &
        (df["firm"].str.strip() != "")
    ].copy()

    # Convert ratings to numeric
    for column in RATING_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df