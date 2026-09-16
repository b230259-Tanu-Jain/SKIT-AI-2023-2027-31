import pandas as pd
import torch
from transformers import pipeline
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
class BertSentimentAnalyzer:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        print("Loading BERT model...")
        self.classifier = pipeline(
            "sentiment-analysis",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            device=self.device
        )
        print("BERT model loaded successfully.")

    def predict(self, texts, batch_size=16):
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            predictions = self.classifier(
                batch,
                truncation=True,
                max_length=512
            )
            results.extend(predictions)
            print(
                f"Processed {min(i + batch_size, len(texts))}"
                f"/{len(texts)} reviews"
            )
        return results
    def add_sentiment(self, df):
        texts = df["review_text"].tolist()
        predictions = self.predict(texts)
        df = df.copy()
        df["bert_sentiment"] = [
            prediction["label"]
            for prediction in predictions
        ]
        df["bert_confidence"] = [
            round(prediction["score"], 4)
            for prediction in predictions
        ]

        # Convert BERT star prediction to numerical score
        df["bert_star_score"] = [
            int(prediction["label"][0])
            for prediction in predictions
        ]
        
        # Convert to sentiment category
        def sentiment_category(stars):
            if stars <= 2:
                return "Negative"
            elif stars == 3:
                return "Neutral"
            else:
                return "Positive"
            
        df["sentiment"] = df["bert_star_score"].apply(
            sentiment_category
        )
        return df