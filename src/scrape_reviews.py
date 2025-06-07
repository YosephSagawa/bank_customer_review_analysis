import pandas as pd
from google_play_scraper import reviews, Sort
from datetime import datetime

# Define app package names and bank names
apps = [
    {"package": "com.combanketh.mobilebanking", "bank": "Commercial Bank of Ethiopia"},
    {"package": "com.bankofabyssinia.boamobile.retail", "bank": "Bank of Abyssinia"},
    {"package": "com.dashen.dashensuperapp", "bank": "Dashen Bank"}
]

# Function to scrape reviews for a given app
def scrape_app_reviews(package, bank_name, count=3000):
    try:
        result, _ = reviews(
            package,
            lang='en',  
            country='us',  
            sort=Sort.NEWEST, 
            count=count  
        )
        # Process reviews into a list of dictionaries
        reviews_list = []
        for review in result:
            reviews_list.append({
                'review': review['content'],
                'rating': review['score'],
                'date': review['at'].strftime('%Y-%m-%d'),  # Format date as YYYY-MM-DD
                'bank': bank_name,
                'source': 'Google Play'
            })
        return reviews_list
    except Exception as e:
        print(f"Error scraping {bank_name}: {e}")
        return []

# Scrape reviews for all apps
all_reviews = []
for app in apps:
    print(f"Scraping reviews for {app['bank']}...")
    app_reviews = scrape_app_reviews(app['package'], app['bank'])
    all_reviews.extend(app_reviews)

# Convert to DataFrame
df = pd.DataFrame(all_reviews)

# Save to CSV
df.to_csv('raw_reviews.csv', index=False)
print("Reviews saved to raw_reviews.csv")
print(f"Total reviews collected: {len(df)}")