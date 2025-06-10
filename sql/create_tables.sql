-- Create Banks table
CREATE TABLE Banks (
    bank_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    bank_name VARCHAR2(100) NOT NULL UNIQUE
);

-- Create Reviews table
CREATE TABLE Reviews (
    review_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    bank_id NUMBER NOT NULL,
    review_text VARCHAR2(4000) NOT NULL,
    rating NUMBER(1) CHECK (rating BETWEEN 1 AND 5),
    review_date DATE NOT NULL,
    source VARCHAR2(50) DEFAULT 'Google Play',
    sentiment_label VARCHAR2(20) CHECK (sentiment_label IN ('positive', 'negative', 'neutral')),
    sentiment_score NUMBER,
    keywords VARCHAR2(4000),
    themes VARCHAR2(4000),
    FOREIGN KEY (bank_id) REFERENCES Banks(bank_id)
);