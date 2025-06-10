import pandas as pd
import oracledb
import json

# Load analyzed reviews
try:
    df = pd.read_csv('../data/analyzed_reviews.csv')
except FileNotFoundError:
    print("Error: data/analyzed_reviews.csv not found")
    exit(1)

# Oracle connection parameters
dsn = "//localhost:1521/XEPDB1"
user = "testuser"
password = "testuser"

try:
    connection = oracledb.connect(user=user, password=password, dsn=dsn)
    cursor = connection.cursor()

    # Insert unique banks
    banks = df['bank'].unique()
    for bank in banks:
        cursor.execute(
            """
            MERGE INTO Banks b
            USING (SELECT :1 AS bank_name FROM dual) src
            ON (b.bank_name = src.bank_name)
            WHEN NOT MATCHED THEN
            INSERT (bank_name) VALUES (src.bank_name)
            """,
            [bank]
        )
    connection.commit()

    # Get bank_id mapping
    cursor.execute("SELECT bank_name, bank_id FROM Banks")
    bank_id_map = {row[0]: row[1] for row in cursor.fetchall()}

    # Insert reviews
    for _, row in df.iterrows():
        keywords = json.dumps(row['keywords']) if isinstance(row['keywords'], list) else str(row['keywords'])
        themes = json.dumps(row['themes']) if isinstance(row['themes'], list) else str(row['themes'])
        
        cursor.execute(
            """
            INSERT INTO Reviews (
                bank_id, review_text, rating, review_date, source,
                sentiment_label, sentiment_score, keywords, themes
            ) VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, :7, :8, :9)
            """,
            [
                bank_id_map[row['bank']],
                row['review'],
                int(row['rating']),
                row['date'],
                row['source'],
                str(row['sentiment_label']),
                float(row['sentiment_score']) if pd.notnull(row['sentiment_score']) else None,
                keywords,
                themes
            ]
        )
    connection.commit()

    # Verify count
    cursor.execute("SELECT COUNT(*) FROM Reviews")
    row_count = cursor.fetchone()[0]
    print(f"Inserted {len(df)} reviews")
    print(f"Total reviews: {row_count}")
    if row_count < 1000:
        print("Warning: Fewer than 1000 reviews. Scrape more.")

except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    connection.close()