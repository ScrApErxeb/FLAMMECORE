from core.signal import Signal, Action, SignalType
from transformers import pipeline

class SentimentPlugin:
    def __init__(self):
        self.name = "sentiment"
        # Modèle compatible PyTorch (multilingue)
        self.analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

    def handle_signal(self, signal: Signal):
        text = signal.payload.get("text", "")
        if not text:
            return None

        result = self.analyzer(text)[0]  # {'label': '5 stars', 'score': 0.95}

        # Mapper label étoiles vers sentiment simplifié
        stars = int(result['label'][0])
        if stars >= 4:
            sentiment = "positif"
        elif stars == 3:
            sentiment = "neutre"
        else:
            sentiment = "negatif"

        return Action(id="action_sentiment_1", params={"sentiment": sentiment})
