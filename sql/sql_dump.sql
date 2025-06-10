SET HEADING OFF
SET FEEDBACK OFF
SET LINESIZE 4000
SPOOL sql\bank_reviews_dump.sql
SELECT 'CREATE TABLE Banks (bank_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, bank_name VARCHAR2(100) NOT NULL UNIQUE);' FROM dual;
SELECT 'CREATE TABLE Reviews (review_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, bank_id NUMBER NOT NULL, review_text VARCHAR2(4000) NOT NULL, rating NUMBER(1) CHECK (rating BETWEEN 1 AND 5), review_date DATE NOT NULL, source VARCHAR2(50) DEFAULT ''Google Play'', sentiment_label VARCHAR2(20) CHECK (sentiment_label IN (''positive'', ''negative'', ''neutral'')), sentiment_score NUMBER, keywords VARCHAR2(4000), themes VARCHAR2(4000), FOREIGN KEY (bank_id) REFERENCES Banks(bank_id));' FROM dual;
SELECT 'INSERT INTO Banks (bank_id, bank_name) VALUES (' || bank_id || ', ''' || REPLACE(bank_name, '''', '''''') || ''');' FROM Banks;
SELECT 'INSERT INTO Reviews (review_id, bank_id, review_text, rating, review_date, source, sentiment_label, sentiment_score, keywords, themes) VALUES (' || 
       review_id || ', ' || bank_id || ', ''' || REPLACE(review_text, '''', '''''') || ''', ' || rating || ', TO_DATE(''' || TO_CHAR(review_date, 'YYYY-MM-DD') || ''', ''YYYY-MM-DD''), ''' || 
       source || ''', ''' || sentiment_label || ''', ' || NVL(TO_CHAR(sentiment_score), 'NULL') || ', ''' || REPLACE(keywords, '''', '''''') || ''', ''' || 
       REPLACE(themes, '''', '''''') || ''');' FROM Reviews;
SPOOL OFF