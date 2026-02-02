COPY client(
    seniorcitizen, partner, dependents, tenure, phoneservice, multiplelines, 
    internetservice, onlinesecurity, onlinebackup, deviceprotection, techsupport, 
    streamingtv, streamingmovies, contract, paperlessbilling, paymentmethod, 
    monthlycharges, totalcharges
)
FROM '/docker-entrypoint-initdb.d/data_cleaned.csv'
DELIMITER ','
CSV HEADER;