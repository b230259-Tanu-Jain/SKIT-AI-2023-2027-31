import re
import pandas as pd
TEXT_COLUMNS = [
    "headline",
    "pros",
    "cons"
]

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
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    required_columns = [
        "firm",
        "headline",
        "pros",
        "cons",
        "overall_rating"
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    for column in TEXT_COLUMNS:
        df[column] = df[column].apply(clean_text)

    df["firm"] = (
        df["firm"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["review_text"] = (
        df["headline"] + " "
        + df["pros"] + " "
        + df["cons"]
    ).str.strip()

    df = df[
        (df["firm"] != "")
        & (df["review_text"] != "")
    ].copy()

    for column in RATING_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df