import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy

# Load cleaned reviews
try:
    df = pd.read_csv('cleaned_reviews.csv')
except FileNotFoundError:
    print("Error: cleaned_reviews.csv not found")
    exit(1)

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to get sentiment label and score
def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound > 0.05:
        return 'positive', compound
    elif compound < -0.05:
        return 'negative', compound
    else:
        return 'neutral', compound

# Apply sentiment analysis
df[['sentiment_label', 'sentiment_score']] = df['review'].apply(lambda x: pd.Series(get_sentiment(x)))

# Aggregate sentiment by bank and rating
sentiment_summary = df.groupby(['bank', 'rating', 'sentiment_label']).size().unstack(fill_value=0)
print("Sentiment Summary by Bank and Rating:")
print(sentiment_summary)

# Save results with sentiment
df.to_csv('analyzed_reviews.csv', index=False)
print("Sentiment analysis results saved to analyzed_reviews.csv")