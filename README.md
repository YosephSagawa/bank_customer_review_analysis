# Ethiopian Bank Reviews Analysis

This repository contains code for scraping, preprocessing, and analyzing Google Play Store reviews for mobile banking apps of Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank.

## Methodology

Data Collection: Scrape reviews using google-play-scraper.
Preprocessing: Clean data by removing duplicates, normalizing dates, and handling missing values.
Analysis: Perform sentiment analysis with VADER and thematic analysis with spaCy.
Storage: Save results in CSV files.
Visualization: Create plots to highlight insights.

## Setup

Clone the repository: git clone https://github.com/your-username/ethiopian-bank-reviews.git
Install dependencies: pip install -r requirements.txt

Run scripts in the following order: scrape_reviews.py, preprocess_reviews.py, analyze_reviews.py.
