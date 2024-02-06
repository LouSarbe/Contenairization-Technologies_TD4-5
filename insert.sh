#!/bin/bash
docker exec -it db psql -U postgres -d CT_PW04-database
"""
Once inside the shell, you can create a table and insert values
For example:
CREATE TABLE example_table (id serial PRIMARY KEY, name VARCHAR(255));
INSERT INTO example_table (name) VALUES ('value1'), ('value2');

Type \q to exit the PostgreSQL shell
"""