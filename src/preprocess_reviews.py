import pandas as pd
from dateutil.parser import parse
import re

# Load raw reviews
try:
    df = pd.read_csv('raw_reviews.csv')
except FileNotFoundError:
    print("Error: raw_reviews.csv not found")
    exit(1)

# Store initial review count for data loss calculation
initial_count = len(df)

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

# Function to check if review is too short
def is_too_short(text):
    #Remoe reviews with fewer than 5 words or 10 characters
    word_count = len(text.split())
    char_count = len(text.split())
    return word_count < 1 or char_count < 3

# Function to check if review is non-informative (e.g., repetitive characters)
def is_non_informative(text):
    # Check for repetitive characters (e.g., "aaa...", "!!!!")
    if re.match(r'^(.)\1{2,}$', text.strip()) or re.match(r'^[!?.]{3,}$', text.strip()):
        return True
    # Check for low word diversity (e.g., same word repeated)
    words = text.lower().split()
    unique_words = len(set(words))
    return unique_words <= 2 and len(words) >= 3

# Apply filters
# Keep reviews that are not too short and not non-informative
df = df[
    (~df['review'].apply(is_too_short)) & 
    (~df['review'].apply(is_non_informative))]

# Reset index
df = df.reset_index(drop=True)

# Save cleaned data
df.to_csv('cleaned_reviews.csv', index=False)

# Calculate and report data loss
final_count = len(df)
data_loss_percent = ((initial_count - final_count) / initial_count) * 100
print("Cleaned reviews saved to cleaned_reviews.csv")
print(f"Total reviews after preprocessing: {final_count}")
print(f"Data loss percentage: {data_loss_percent:.2f}%")
if data_loss_percent > 5:
    print("Warning: Data loss exceeds 5%. Consider scraping more reviews.")
if final_count < 1200:
    print(f"Warning: Only {final_count} reviews remain. Need at least 1200. Scrape more reviews.")