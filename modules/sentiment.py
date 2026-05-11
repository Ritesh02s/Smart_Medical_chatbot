from textblob import TextBlob


def detect_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.2:
        return "positive"

    elif polarity < -0.2:
        return "negative"

    else:
        return "neutral"