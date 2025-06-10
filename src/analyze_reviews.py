import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from collections import Counter

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

# Intialize spaCy
nlp = spacy.load('en_core_web_sm')

# Function to extract keywords and phrases, excluding stop words
def extract_keywords(text):
    doc = nlp(text.lower())
    # Extract noun chunks, filter out stop words
    keywords = []
    for chunk in doc.noun_chunks:
        # Keep chunks with at least one non-stop word
        if any(not token.is_stop and token.is_alpha for token in chunk):
            # Remove stop words from the chunk and join remaining tokens
            filtered_chunk = ' '.join(token.text for token in chunk if not token.is_stop and token.is_alpha)
            if filtered_chunk and len(filtered_chunk.split()) <= 3:
                keywords.append(filtered_chunk)
    return keywords


# Apply keyword extraction
df['keywords'] = df['review'].apply(extract_keywords)

# Group keywords by bank and count frequency
themes_by_bank = {}
for bank in df['bank'].unique():
    bank_reviews = df[df['bank'] == bank]
    all_keywords = []
    for keywords in bank_reviews['keywords']:
        all_keywords.extend(keywords)
    # Get top 20 keywords/phrases
    keyword_counts = Counter(all_keywords).most_common(20)
    
    # Manually group into themes (example grouping logic)
    themes = {
        'Account Access Issues': ['login error', 'login issue', 'access problem', 'authentication', 'pin issue', 'login access', 'security issue','bug'],
        'Transaction Performance': ['slow transfer', 'transfer issue', 'transaction error', 'money transfer', 'payment issue'],
        'User Interface & Experience': ['user interface', 'app design', 'ui', 'navigation', 'loading animation','ux', 'interface', 'design'],
        'Customer Support': ['support', 'customer service', 'help desk', 'response time'],
        'Feature Requests': ['fingerprint login', 'biometric', 'new feature', 'faster loading']
    }

    # Assign themes to reviews
    bank_themes = []
    for _, row in bank_reviews.iterrows():
        review_themes = []
        for theme, theme_keywords in themes.items():
            if any(keyword in row['keywords'] for keyword in theme_keywords):
                review_themes.append(theme)
        bank_themes.append(review_themes if review_themes else ['Other'])
    
    bank_reviews['themes'] = bank_themes
    themes_by_bank[bank] = bank_reviews[['bank', 'rating','date','source','review','sentiment_label', 'sentiment_score', 'keywords', 'themes']]

    # Print top keywords and themes
    print(f"\nTop Keywords for {bank}:")
    print(keyword_counts)
    print(f"Themes for {bank}:")
    theme_counts = Counter([theme for sublist in bank_themes for theme in sublist]).most_common()
    print(theme_counts)

# Concatenate results for all banks
df = pd.concat(themes_by_bank.values(), ignore_index=True)

# Save results with sentiment
df.to_csv('analyzed_reviews.csv', index=False)
print("Sentiment analysis results saved to analyzed_reviews.csv")