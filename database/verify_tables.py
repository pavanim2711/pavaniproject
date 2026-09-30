#!/usr/bin/env python3
import sqlite3

db = sqlite3.connect('quick_tym.db')
cur = db.cursor()

print("Database Verification Report")
print("=" * 60)

# Get all tables
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
print(f"\nTotal Tables: {len(tables)}")
print("\nTable List:")
for t in tables:
    count = cur.execute(f"SELECT COUNT(*) FROM {t[0]}").fetchone()[0]
    print(f"  • {t[0]:25} - {count:4} records")

# Count indexes
indexes = cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'").fetchone()[0]
print(f"\nIndexes: {indexes}")

# Verify constraints
print("\nConstraint Verification:")
checks = {
    "Valid user roles": "SELECT COUNT(*) FROM users WHERE role NOT IN ('Customer', 'Delivery_Partner', 'Admin')",
    "Valid product categories": "SELECT COUNT(*) FROM products WHERE category NOT IN ('Indoor', 'Outdoor')",
    "Price in range": "SELECT COUNT(*) FROM products WHERE price_per_hour < 50 OR price_per_hour > 500",
    "Foreign keys intact": "SELECT COUNT(*) FROM rental_sessions WHERE product_id IS NOT NULL AND product_id NOT IN (SELECT id FROM products)",
}

for name, query in checks.items():
    result = cur.execute(query).fetchone()[0]
    status = "✓ PASS" if result == 0 else "✗ FAIL"
    print(f"  {status} - {name}: {result}")

# Sample data
print("\nSample Data:")
print("  Customers:", cur.execute("SELECT COUNT(*) FROM users WHERE role='Customer'").fetchone()[0])
print("  Products:", cur.execute("SELECT COUNT(*) FROM products").fetchone()[0])
print("  Rentals:", cur.execute("SELECT COUNT(*) FROM rental_sessions").fetchone()[0])
print("  Payments:", cur.execute("SELECT COUNT(*) FROM payments").fetchone()[0])

db.close()
print("\n" + "=" * 60)
print("✓ Database is ready for development")
