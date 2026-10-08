import os
import pandas as pd

from .preprocessing import load_and_prepare_data
from .sentiment import BertSentimentAnalyzer
from .company_insights import (
    calculate_company_insights,
    rank_companies
)


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
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

SAMPLE_SIZE = 20000


def main():

    print(
        "\nStarting WorkSphere "
        "Company Intelligence...\n"
    )

    os.makedirs(
        PROCESSED_DIR,
        exist_ok=True
    )

    # Load and preprocess data
    print(
        "Loading and preprocessing data..."
    )

    df = load_and_prepare_data(
        INPUT_FILE
    )

    print(
        f"Reviews loaded: {len(df)}"
    )

    # Select reproducible sample
    if len(df) > SAMPLE_SIZE:

        df = (
            df.sample(
                n=SAMPLE_SIZE,
                random_state=42
            )
            .reset_index(drop=True)
        )

    print(
        f"Reviews selected for BERT: "
        f"{len(df)}"
    )

    # Reuse existing BERT results
    use_existing = False

    if os.path.exists(REVIEW_OUTPUT):

        existing_df = pd.read_csv(
            REVIEW_OUTPUT
        )

        if (
            len(existing_df) == len(df)
            and "bert_star_score" in existing_df.columns
        ):

            df = existing_df
            use_existing = True

            print(
                "\nExisting BERT results found."
            )

            print(
                "Skipping BERT processing."
            )

    # Run BERT only when required
    if not use_existing:

        print(
            "\nRunning BERT sentiment analysis..."
        )

        analyzer = BertSentimentAnalyzer()

        df = analyzer.add_sentiment(
            df
        )

        df.to_csv(
            REVIEW_OUTPUT,
            index=False
        )

        print(
            "\nReview sentiment saved to:"
        )

        print(
            REVIEW_OUTPUT
        )

    # Calculate company-level insights
    print(
        "\nCalculating company insights..."
    )

    company_df = calculate_company_insights(
        df
    )

    # Rank companies
    company_df = rank_companies(
        company_df
    )

    # Save company insights
    company_df.to_csv(
        COMPANY_OUTPUT,
        index=False
    )

    print(
        "\nCompany insights saved to:"
    )

    print(
        COMPANY_OUTPUT
    )

    # Display top companies
    columns = [
        "rank",
        "firm",
        "company_intelligence_score",
        "review_count"
    ]

    columns = [
        column
        for column in columns
        if column in company_df.columns
    ]

    print(
        "\nTop 10 Companies:\n"
    )

    if len(company_df) > 0:

        print(
            company_df[columns]
            .head(10)
            .to_string(index=False)
        )

    else:

        print(
            "No companies have enough reviews "
            "to meet the minimum review threshold."
        )

    print(
        "\nCompany Intelligence "
        "completed successfully!"
    )


if __name__ == "__main__":
    main()