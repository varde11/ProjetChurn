CREATE TABLE Client(
    id_client SERIAL PRIMARY KEY,
    seniorcitizen VARCHAR(5),
    partner VARCHAR(5),
    dependents VARCHAR (5),
    phoneservice VARCHAR(5),
    paperlessbilling VARCHAR(5),
    multiplelines VARCHAR(20),
    internetservice VARCHAR(20),
    onlinesecurity VARCHAR(20),
    onlinebackup VARCHAR(20),
    deviceprotection VARCHAR (20),
    techsupport VARCHAR (20),
    streamingtv VARCHAR (20),
    streamingmovies VARCHAR(20),
    contract VARCHAR (20),
    paymentmethod VARCHAR (25),
    monthlycharges FLOAT,
    tenure INT,
    totalcharges FLOAT

);

CREATE TABLE Prediction(
    id_prediction SERIAL PRIMARY KEY,
    id_client INT REFERENCES Client(id_client) NOT NULL,
    option_model VARCHAR (10),
    score DOUBLE PRECISION,
    label VARCHAR(10),
    time_stamp TIMESTAMP --  mettez plûtot TIMESTAMP à la place de DATE

);
