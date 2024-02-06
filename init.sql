CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price NUMERIC(10, 2)
);

INSERT INTO products (name, price) VALUES
    ('Product 1', 10.99),
    ('Product 2', 19.99);