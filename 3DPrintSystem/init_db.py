#!/usr/bin/env python3
"""
Database Initialization Script for 3D Print System
Creates all database tables from SQLAlchemy models
"""
import os
import sys
from app import create_app
from app.extensions import db

def init_database():
    """Initialize the database with all tables"""
    
    # Create the Flask app
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Creating database tables...")
            
            # Create all tables
            db.create_all()
            
            print("✅ Database tables created successfully!")
            print("\nTables created:")
            
            # List all tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            for table in tables:
                columns = inspector.get_columns(table)
                print(f"  📋 {table} ({len(columns)} columns)")
                for col in columns:
                    print(f"    - {col['name']} ({col['type']})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            return False

if __name__ == "__main__":
    if init_database():
        print("\n🎉 Database initialization completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Database initialization failed!")
        sys.exit(1) 