#!/bin/bash

# # Run the Python script to generate SQL files
# python3 script.py

# # Move the SQL files to the PostgreSQL initialization directory
# mv schema.sql /docker-entrypoint-initdb.d/
# mv data.sql /docker-entrypoint-initdb.d/

# # Start PostgreSQL service
# service postgresql start

# Keep the container running
tail -f /dev/null
