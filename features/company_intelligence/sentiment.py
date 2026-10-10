import torch
from transformers import pipeline
MODEL_NAME = (
    "nlptown/bert-base-multilingual-uncased-sentiment"
)
class BertSentimentAnalyzer:
    def __init__(self):
        self.device = (
            0 if torch.cuda.is_available()
            else -1
        )

        print("Loading BERT model...")
        self.classifier = pipeline(
            "sentiment-analysis",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            device=self.device
        )
        print(
            "BERT model loaded successfully "
            f"({'GPU' if self.device == 0 else 'CPU'})."
        )
    def predict(self, texts, batch_size=32):
        results = []
        total = len(texts)
        print(
            f"\nStarting BERT inference on "
            f"{total} reviews..."
        )
        for i in range(0, total, batch_size):

            batch = texts[i:i + batch_size]
            predictions = self.classifier(
                batch,
                truncation=True,
                max_length=256
            )
            results.extend(predictions)
            print(
                f"Processed "
                f"{min(i + batch_size, total)}/{total}"
                f" reviews"
            )
        return results

    def add_sentiment(self, df):
        df = df.copy()
        texts = df["review_text"].tolist()
        predictions = self.predict(
            texts,
            batch_size=32
        )
        df["bert_sentiment"] = [
            prediction["label"]
            for prediction in predictions
        ]
        df["bert_confidence"] = [
            round(prediction["score"], 4)
            for prediction in predictions
        ]
        df["bert_star_score"] = [
            int(prediction["label"][0])
            for prediction in predictions
        ]
        def sentiment_category(stars):
            if stars <= 2:
                return "Negative"

            if stars == 3:
                return "Neutral"

            return "Positive"
        df["sentiment"] = (
            df["bert_star_score"]
            .apply(sentiment_category)
        )
        return df