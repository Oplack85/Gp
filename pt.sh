#!/bin/bash

# Set new variables
DB_DIR="/app/db_files"
OUTPUT_FILE="db_details.txt"

# Create the directory
mkdir -p "$DB_DIR"
initdb "$DB_DIR"

# Start the service
pg_ctl -D "$DB_DIR" start

# Clear the previous file if it exists
> "$OUTPUT_FILE"

# Create 5 new databases
for i in {1..5}; do
    RANDOM_NUMBER=$((RANDOM % 10000))
    NEW_DB_NAME="ScorpionDatas$RANDOM_NUMBER"  # Database name
    NEW_USER="DataScoR"       # Unique username
    NEW_PASSWORD="Scorpass$RANDOM_NUMBER"  # Random password

    # Create the new user and set password
    psql -U postgres -d postgres -c "CREATE USER $NEW_USER WITH PASSWORD '$NEW_PASSWORD';"

    # Create the database
    psql -U postgres -d postgres -c "CREATE DATABASE $NEW_DB_NAME OWNER $NEW_USER;"

    # Save connection details to the file
    echo "postgresql://$NEW_USER:$NEW_PASSWORD@localhost:5432/$NEW_DB_NAME" >> "$OUTPUT_FILE"
done

# Display connection details
echo "5 new databases have been created. Check the details in the file: $OUTPUT_FILE"

# Status
pg_ctl -D "$DB_DIR" status
