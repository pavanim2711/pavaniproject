#!/bin/bash
# Quick Tym Database Initialization Script
# Creates SQLite database, applies schema, inserts seed data, and verifies integrity
# Version: 1.0

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
DB_PATH="./quick_tym.db"
SCHEMA_FILE="./schema.sql"
SEED_FILE="./seed.sql"
VERIFY_FILE="./verify.sql"

echo -e "${BLUE}═════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Quick Tym SQLite Database Initialization${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if SQLite3 is installed
if ! command -v sqlite3 &> /dev/null; then
    echo -e "${RED}✗ Error: sqlite3 is not installed${NC}"
    echo "Please install sqlite3 and try again"
    exit 1
fi

echo -e "${GREEN}✓ sqlite3 is installed${NC}"

# Check if required SQL files exist
if [ ! -f "$SCHEMA_FILE" ]; then
    echo -e "${RED}✗ Error: $SCHEMA_FILE not found${NC}"
    exit 1
fi

if [ ! -f "$SEED_FILE" ]; then
    echo -e "${RED}✗ Error: $SEED_FILE not found${NC}"
    exit 1
fi

if [ ! -f "$VERIFY_FILE" ]; then
    echo -e "${RED}✗ Error: $VERIFY_FILE not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All SQL files found${NC}"
echo ""

# Remove existing database if requested
if [ -f "$DB_PATH" ]; then
    echo -e "${YELLOW}⚠ Database file already exists: $DB_PATH${NC}"
    read -p "Do you want to recreate the database? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm "$DB_PATH"
        echo -e "${GREEN}✓ Old database removed${NC}"
    else
        echo "Skipping database recreation"
        exit 0
    fi
fi

echo ""
echo -e "${BLUE}Step 1: Creating database and applying schema...${NC}"
sqlite3 "$DB_PATH" < "$SCHEMA_FILE"
echo -e "${GREEN}✓ Schema applied successfully${NC}"

echo ""
echo -e "${BLUE}Step 2: Inserting sample data...${NC}"
sqlite3 "$DB_PATH" < "$SEED_FILE"
echo -e "${GREEN}✓ Sample data inserted successfully${NC}"

echo ""
echo -e "${BLUE}Step 3: Verifying database integrity...${NC}"
echo ""
sqlite3 "$DB_PATH" < "$VERIFY_FILE"

echo ""
echo -e "${BLUE}═════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Database initialization complete!${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Database Location: $DB_PATH"
echo "Size: $(ls -lh "$DB_PATH" | awk '{print $5}')"
echo ""
echo "Quick commands:"
echo "  sqlite3 $DB_PATH                    # Open database in CLI"
echo "  sqlite3 $DB_PATH '.tables'          # List all tables"
echo "  sqlite3 $DB_PATH '.schema users'    # Show users table schema"
echo ""
