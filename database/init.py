#!/usr/bin/env python3
"""
Quick Tym Database Initialization Script
Creates SQLite database, applies schema, inserts seed data, and verifies integrity
Version: 1.0
"""

import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime

# Colors for output (works on Windows 10+ and Unix)
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
    @staticmethod
    def enable_windows_colors():
        """Enable ANSI color codes on Windows 10+"""
        if sys.platform == 'win32':
            os.system('color')

def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*70}{Colors.RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def main():
    Colors.enable_windows_colors()
    
    print_header("Quick Tym SQLite Database Initialization")
    
    # Configuration
    script_dir = Path(__file__).parent
    db_path = script_dir / "quick_tym.db"
    schema_file = script_dir / "schema.sql"
    seed_file = script_dir / "seed.sql"
    verify_file = script_dir / "verify.sql"
    
    # Verify required files exist
    print("Checking required files...")
    
    required_files = {
        "Schema": schema_file,
        "Seed Data": seed_file,
        "Verification": verify_file
    }
    
    for name, filepath in required_files.items():
        if filepath.exists():
            print_success(f"{name} file found: {filepath.name}")
        else:
            print_error(f"{name} file not found: {filepath}")
            return False
    
    # Handle existing database
    print("\nChecking existing database...")
    if db_path.exists():
        print_warning(f"Database file already exists: {db_path}")
        response = input("Do you want to recreate it? (y/n): ").lower().strip()
        if response != 'y':
            print("Database initialization cancelled.")
            return False
        db_path.unlink()
        print_success("Old database removed")
    
    # Create database and apply schema
    print_header("Step 1: Creating Database and Applying Schema")
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Read and execute schema
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        cursor.executescript(schema_sql)
        conn.commit()
        print_success("Schema applied successfully")
        
    except Exception as e:
        print_error(f"Failed to apply schema: {e}")
        return False
    finally:
        if conn:
            conn.close()
    
    # Insert seed data
    print_header("Step 2: Inserting Sample Data")
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        with open(seed_file, 'r') as f:
            seed_sql = f.read()
        
        cursor.executescript(seed_sql)
        conn.commit()
        print_success("Sample data inserted successfully")
        
        # Count inserted records
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
        
    except Exception as e:
        print_error(f"Failed to insert seed data: {e}")
        return False
    finally:
        if conn:
            conn.close()
    
    # Verify database integrity
    print_header("Step 3: Verifying Database Integrity")
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Perform integrity checks
        checks = {
            "Invalid user roles": "SELECT COUNT(*) FROM users WHERE role NOT IN ('Customer', 'Delivery_Partner', 'Admin')",
            "Invalid product categories": "SELECT COUNT(*) FROM products WHERE category NOT IN ('Indoor', 'Outdoor')",
            "Prices outside range (₹50-₹500)": "SELECT COUNT(*) FROM products WHERE price_per_hour < 50 OR price_per_hour > 500",
            "Negative inventory": "SELECT COUNT(*) FROM inventory WHERE quantity < 0 OR available_quantity < 0",
            "Invalid rental session times": "SELECT COUNT(*) FROM rental_sessions WHERE end_time IS NOT NULL AND end_time < start_time",
            "Orphaned products": "SELECT COUNT(*) FROM inventory WHERE product_id NOT IN (SELECT id FROM products)",
            "Orphaned rental sessions": "SELECT COUNT(*) FROM rental_sessions WHERE user_id NOT IN (SELECT id FROM users)",
            "Orphaned payments": "SELECT COUNT(*) FROM payments WHERE rental_session_id NOT IN (SELECT id FROM rental_sessions)",
        }
        
        all_passed = True
        for check_name, check_sql in checks.items():
            result = cursor.execute(check_sql).fetchone()[0]
            if result == 0:
                print_success(f"{check_name}: 0 issues")
            else:
                print_error(f"{check_name}: {result} issues found")
                all_passed = False
        
        if not all_passed:
            print_error("Database verification found issues!")
            return False
        
        # Verify indexes exist
        index_count = cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'"
        ).fetchone()[0]
        print_success(f"Database indexes: {index_count} indexes created")
        
        # Verify foreign keys
        cursor.execute("PRAGMA foreign_keys")
        fk_status = cursor.fetchone()[0]
        if fk_status:
            print_success("Foreign key constraints: ENABLED")
        else:
            print_warning("Foreign key constraints: DISABLED (should be enabled)")
        
    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False
    finally:
        if conn:
            conn.close()
    
    # Final summary
    print_header("Database Initialization Complete!")
    
    db_size = db_path.stat().st_size
    db_size_mb = db_size / (1024 * 1024)
    
    print(f"Database Location: {db_path}")
    print(f"Database Size: {db_size_mb:.2f} MB ({db_size:,} bytes)")
    print(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + Colors.GREEN + "✓ All checks passed! Database is ready for use." + Colors.RESET)
    
    print("\nUseful SQLite commands:")
    print(f"  sqlite3 \"{db_path}\"                    # Open database")
    print(f"  sqlite3 \"{db_path}\" '.tables'          # List all tables")
    print(f"  sqlite3 \"{db_path}\" '.schema users'    # Show users table schema")
    print(f"  sqlite3 \"{db_path}\" 'SELECT * FROM products;'  # Query products")
    
    print("\n" + "="*70 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDatabase initialization cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
