from transformers import pipeline
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

import ssl
import nltk

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')
nltk.download('punkt_tab')

def analyze_sentiment(text):
    """
    Uses the CardiffNLP twitter-roberta-base-sentiment-latest model for sentiment analysis.
    Returns a dictionary with 'label' and 'score'.
    """
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest"
    )
    result = sentiment_pipeline(text)
    return result[0]

def explain_sentiment_vader(text):
    """
    Explains the sentiment based on VADER's lexicon.
    Tokenizes the text and collects words that have non-zero sentiment scores.
    Returns a string listing positive and negative contributors.
    """
    sia = SentimentIntensityAnalyzer()
    tokens = word_tokenize(text)
    pos_contributors = []
    neg_contributors = []
    for token in tokens:
        lower_token = token.lower()
        if lower_token in sia.lexicon:
            score = sia.lexicon[lower_token]
            if score > 0:
                pos_contributors.append((lower_token, score))
            elif score < 0:
                neg_contributors.append((lower_token, score))
    
    pos_contributors = sorted(pos_contributors, key=lambda x: x[1], reverse=True)
    neg_contributors = sorted(neg_contributors, key=lambda x: x[1])
    
    pos_explanation = ", ".join([f"{word}({score:.2f})" for word, score in pos_contributors]) if pos_contributors else "None"
    neg_explanation = ", ".join([f"{word}({score:.2f})" for word, score in neg_contributors]) if neg_contributors else "None"
    
    explanation = f"Positive contributors: {pos_explanation}. Negative contributors: {neg_explanation}."
    return explanation

if __name__ == "__main__":
    sample_text = "The property market is booming with significant growth and rising prices."
    sentiment = analyze_sentiment(sample_text)
    explanation = explain_sentiment_vader(sample_text)
    print("Sentiment:", sentiment)
    print("Explanation:", explanation)