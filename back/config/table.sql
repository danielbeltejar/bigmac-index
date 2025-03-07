CREATE TABLE IF NOT EXISTS bigmac_prices
(
    id
    INT
    NOT
    NULL
    auto_increment,
    country
    VARCHAR
(
    255
) NOT NULL,
    date DATE NOT NULL,
    price DECIMAL
(
    10,
    2
) NOT NULL,
    PRIMARY KEY
(
    id
)
    );

CREATE INDEX IF NOT EXISTS idx_date ON bigmac_prices (date);

CREATE INDEX IF NOT EXISTS idx_country ON bigmac_prices (country);