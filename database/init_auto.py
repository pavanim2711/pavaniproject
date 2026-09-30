#!/usr/bin/env python3
"""
Quick Tym Database Auto-Initialization (No prompts)
"""

import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime

def main():
    script_dir = Path(__file__).parent
    db_path = script_dir / "quick_tym.db"
    schema_file = script_dir / "schema.sql"
    seed_file = script_dir / "seed.sql"
    
    print(f"Creating database at: {db_path}")
    
    # Remove existing database
    if db_path.exists():
        db_path.unlink()
        print("✓ Old database removed")
    
    # Create and apply schema
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    with open(schema_file, 'r') as f:
        cursor.executescript(f.read())
    conn.commit()
    print("✓ Schema applied")
    
    # Insert seed data
    with open(seed_file, 'r') as f:
        cursor.executescript(f.read())
    conn.commit()
    print("✓ Seed data inserted")
    
    # Count records
    tables = [
        'categories', 'users', 'products', 'inventory', 
        'rental_sessions', 'bookings', 'payments', 'deliveries',
        'delivery_tasks', 'pickup_requests', 'reviews', 'notifications',
        'ai_recommendations', 'demand_predictions'
    ]
    
    print("\nData summary:")
    for table in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        if count > 0:
            print(f"  • {table}: {count} records")
    
    # Verify constraints
    print("\nVerifying integrity...")
    checks = {
        "Invalid roles": "SELECT COUNT(*) FROM users WHERE role NOT IN ('Customer', 'Delivery_Partner', 'Admin')",
        "Invalid categories": "SELECT COUNT(*) FROM products WHERE category NOT IN ('Indoor', 'Outdoor')",
        "Price violations": "SELECT COUNT(*) FROM products WHERE price_per_hour < 50 OR price_per_hour > 500",
        "Negative inventory": "SELECT COUNT(*) FROM inventory WHERE quantity < 0",
    }
    
    for name, sql in checks.items():
        result = cursor.execute(sql).fetchone()[0]
        status = "✓" if result == 0 else "✗"
        print(f"  {status} {name}: {result}")
    
    conn.close()
    
    print(f"\n✓ Database ready at: {db_path}")
    print(f"  Size: {db_path.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
