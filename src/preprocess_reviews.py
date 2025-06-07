import pandas as pd
from dateutil.parser import parse

# Load raw reviews
try:
    df = pd.read_csv('raw_reviews.csv')
except FileNotFoundError:
    print("Error: raw_reviews.csv not found")
    exit(1)

# Remove duplicates based on review text and bank
df = df.drop_duplicates(subset=['review', 'bank'], keep='first')

# Handle missing data
# Drop rows where 'review' or 'rating' is missing
df = df.dropna(subset=['review', 'rating'])

# Validate and normalize dates
def normalize_date(date_str):
    try:
        # Parse date and format as YYYY-MM-DD
        return parse(date_str).strftime('%Y-%m-%d')
    except:
        return None

df['date'] = df['date'].apply(normalize_date)
# Drop rows with invalid dates
df = df.dropna(subset=['date'])

# Ensure rating is an integer between 1 and 5
df = df[df['rating'].isin([1, 2, 3, 4, 5])]
df['rating'] = df['rating'].astype(int)

# Reset index
df = df.reset_index(drop=True)

# Save cleaned data
df.to_csv('cleaned_reviews.csv', index=False)
print("Cleaned reviews saved to cleaned_reviews.csv")
print(f"Total reviews after preprocessing: {len(df)}")
print(f"Missing data percentage: {((1800 - len(df)) / 1800 * 100):.2f}%")