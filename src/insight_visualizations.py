import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import ast

# Load analyzed reviews
try:
    df = pd.read_csv('../data/analyzed_reviews.csv')
except FileNotFoundError:
    print("Error: data/analyzed_reviews.csv not found")
    exit(1)

# Ensure 'keywords' and 'themes' are lists
df['keywords'] = df['keywords'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
df['themes'] = df['themes'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Convert 'date' to datetime
df['date'] = pd.to_datetime(df['date'])

# --- Insights ---
# Drivers and Pain Points
banks = df['bank'].unique()
for bank in banks:
    bank_df = df[df['bank'] == bank]
    pos_reviews = bank_df[bank_df['sentiment_label'] == 'positive']
    neg_reviews = bank_df[bank_df['sentiment_label'] == 'negative']

    # Drivers (from positive reviews, top themes/keywords)
    pos_keywords = [kw for kws in pos_reviews['keywords'] for kw in kws]
    pos_themes = [th for ths in pos_reviews['themes'] for th in ths]
    top_pos_keywords = Counter(pos_keywords).most_common(5)
    top_pos_themes = Counter(pos_themes).most_common(3)
    print(f"\n{bank} Drivers:")
    print(f"Top Positive Keywords: {top_pos_keywords}")
    print(f"Top Positive Themes: {top_pos_themes}")

    # Pain Points (from negative reviews, top themes/keywords)
    neg_keywords = [kw for kws in neg_reviews['keywords'] for kw in kws]
    neg_themes = [th for ths in neg_reviews['themes'] for th in ths]
    top_neg_keywords = Counter(neg_keywords).most_common(5)
    top_neg_themes = Counter(neg_themes).most_common(3)
    print(f"\n{bank} Pain Points:")
    print(f"Top Negative Keywords: {top_neg_keywords}")
    print(f"Top Negative Themes: {top_neg_themes}")

# Bank Comparisons
# CBE vs. BOA
cbe_df = df[df['bank'] == 'Commercial Bank of Ethiopia']
boa_df = df[df['bank'] == 'Bank of Abyssinia']
cbe_sentiment = cbe_df['sentiment_label'].value_counts(normalize=True) * 100
boa_sentiment = boa_df['sentiment_label'].value_counts(normalize=True) * 100
print("\nSentiment Comparison (%):")
print(f"CBE vs. BOA:")
print(f"  CBE: {cbe_sentiment.to_dict()}")
print(f"  BOA: {boa_sentiment.to_dict()}")

# Dashen Bank vs. BOA
dashen_df = df[df['bank'] == 'Dashen Bank']
dashen_sentiment = dashen_df['sentiment_label'].value_counts(normalize=True) * 100
print(f"\nDashen Bank vs. BOA:")
print(f"  Dashen Bank: {dashen_sentiment.to_dict()}")
print(f"  BOA: {boa_sentiment.to_dict()}")

# CBE vs. Dashen Bank
print(f"\nCBE vs. Dashen Bank:")
print(f"  CBE: {cbe_sentiment.to_dict()}")
print(f"  Dashen Bank: {dashen_sentiment.to_dict()}")

# --- Visualizations ---
# Set Seaborn style
sns.set_style("whitegrid")

# 1. Sentiment Trend Over Time (Line Plot)
plt.figure(figsize=(15, 6))  # Increased width to accommodate more labels
for bank in banks:
    bank_df = df[df['bank'] == bank]
    trend = bank_df.groupby([bank_df['date'].dt.to_period('M'), 'sentiment_label']).size().unstack(fill_value=0)
    # Sort the index in descending order
    trend = trend.sort_index(ascending=False)
    for sentiment in trend.columns:
        plt.plot(trend.index.astype(str), trend[sentiment], label=f'{bank} - {sentiment}', marker='o')
plt.title('Sentiment Trend Over Time by Bank')
plt.xlabel('Month')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('../output/sentiment_trend.png')
plt.close()

# 2. Rating Distribution by Bank (Bar Plot)
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='rating', hue='bank')
plt.title('Rating Distribution by Bank')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.legend(title='Bank')
plt.tight_layout()
plt.savefig('../output/rating_distribution.png')
plt.close()

# 3. Sentiment Distribution by Bank (Stacked Bar Plot)
sentiment_dist = df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0)
sentiment_dist.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Sentiment Distribution by Bank')
plt.xlabel('Bank')
plt.ylabel('Number of Reviews')
plt.legend(title='Sentiment')
plt.tight_layout()
plt.savefig('../output/sentiment_bar.png')
plt.close()

# 4 & 5. Keyword Clouds for CBE and BOA
for bank in ['Bank of Abyssinia', 'Commercial Bank of Ethiopia', 'Dashen Bank']:
    bank_df = df[df['bank'] == bank]
    keywords = [kw for kws in bank_df['keywords'] for kw in kws]
    keyword_freq = dict(Counter(keywords))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(keyword_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Keyword Cloud for {bank}')
    plt.tight_layout()
    plt.savefig(f'../output/keyword_cloud_{bank.lower()}.png')
    plt.close()

print("\nVisualizations saved to output/ folder")