#!/usr/bin/env python3
"""
KodiBOT Database Seeding Script - Real User Data
Seeds database with comprehensive test data for all team members
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import create_tables, Citizens, Taxes, Parcels, Procedures, LinkedUsers, SessionLocal
from src.test_data import (
    ALL_CITIZENS, ALL_TAXES, ALL_PARCELS, TEST_PROCEDURES,
    PATRICK_DAUDI, get_patrick_phone, get_patrick_citizen_id
)

def clear_database():
    """Clear all existing data"""
    db = SessionLocal()
    try:
        print("🗑️  Clearing existing data...")
        db.query(LinkedUsers).delete()
        db.query(Taxes).delete()
        db.query(Parcels).delete()
        db.query(Procedures).delete()
        db.query(Citizens).delete()
        db.commit()
        print("✅ Database cleared")
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        db.rollback()
    finally:
        db.close()

def seed_citizens():
    """Seed all citizens"""
    db = SessionLocal()
    try:
        print("👥 Seeding citizens...")
        
        for citizen_data in ALL_CITIZENS:
            citizen = Citizens(
                phone_number=citizen_data["phone_number"],
                citizen_id=citizen_data["citizen_id"],
                first_name=citizen_data["first_name"],
                last_name=citizen_data["last_name"],
                email=citizen_data["email"],
                address=citizen_data["address"],
                date_of_birth=citizen_data["date_of_birth"],
                is_verified=citizen_data["is_verified"]
            )
            db.add(citizen)
            print(f"  ✅ Added: {citizen_data['first_name']} {citizen_data['last_name']} ({citizen_data['phone_number']})")
        
        db.commit()
        print(f"✅ Seeded {len(ALL_CITIZENS)} citizens")
        
    except Exception as e:
        print(f"❌ Error seeding citizens: {e}")
        db.rollback()
    finally:
        db.close()

def seed_taxes():
    """Seed all tax records"""
    db = SessionLocal()
    try:
        print("💰 Seeding tax records...")
        
        for tax_data in ALL_TAXES:
            tax = Taxes(
                citizen_id=tax_data["citizen_id"],
                tax_type=tax_data["tax_type"],
                amount_due=tax_data["amount_due"],
                amount_paid=tax_data["amount_paid"],
                due_date=tax_data["due_date"],
                status=tax_data["status"],
                tax_year=tax_data["tax_year"]
            )
            db.add(tax)
        
        db.commit()
        print(f"✅ Seeded {len(ALL_TAXES)} tax records")
        
    except Exception as e:
        print(f"❌ Error seeding taxes: {e}")
        db.rollback()
    finally:
        db.close()

def seed_parcels():
    """Seed all parcel records"""
    db = SessionLocal()
    try:
        print("🏠 Seeding parcel records...")
        
        for parcel_data in ALL_PARCELS:
            parcel = Parcels(
                citizen_id=parcel_data["citizen_id"],
                parcel_number=parcel_data["parcel_number"],
                property_type=parcel_data["property_type"],
                address=parcel_data["address"],
                area_sqm=parcel_data["area_sqm"],
                estimated_value=parcel_data["estimated_value"],
                status=parcel_data["status"]
            )
            db.add(parcel)
        
        db.commit()
        print(f"✅ Seeded {len(ALL_PARCELS)} parcel records")
        
    except Exception as e:
        print(f"❌ Error seeding parcels: {e}")
        db.rollback()
    finally:
        db.close()

def seed_procedures():
    """Seed procedure records"""
    db = SessionLocal()
    try:
        print("📋 Seeding procedures...")
        
        for proc_data in TEST_PROCEDURES:
            procedure = Procedures(
                name=proc_data["name"],
                description=proc_data["description"],
                steps=json.dumps(proc_data["steps"], ensure_ascii=False),
                required_documents=json.dumps(proc_data["required_documents"], ensure_ascii=False),
                estimated_duration=proc_data["estimated_duration"],
                cost=proc_data["cost"],
                department=proc_data["department"]
            )
            db.add(procedure)
        
        db.commit()
        print(f"✅ Seeded {len(TEST_PROCEDURES)} procedures")
        
    except Exception as e:
        print(f"❌ Error seeding procedures: {e}")
        db.rollback()
    finally:
        db.close()

def create_linked_users():
    """Create linked users for testing (all users are pre-linked)"""
    db = SessionLocal()
    try:
        print("🔗 Creating linked users...")
        
        for citizen_data in ALL_CITIZENS:
            linked_user = LinkedUsers(
                phone_number=citizen_data["phone_number"],
                citizen_id=citizen_data["citizen_id"],
                is_linked=True,
                linked_at=datetime.utcnow()
            )
            db.add(linked_user)
            print(f"  ✅ Linked: {citizen_data['first_name']} {citizen_data['last_name']}")
        
        db.commit()
        print(f"✅ Created {len(ALL_CITIZENS)} linked users")
        
    except Exception as e:
        print(f"❌ Error creating linked users: {e}")
        db.rollback()
    finally:
        db.close()

def print_summary():
    """Print seeding summary"""
    db = SessionLocal()
    try:
        print("\n📊 DATABASE SUMMARY")
        print("=" * 50)
        
        # Count records
        citizen_count = db.query(Citizens).count()
        tax_count = db.query(Taxes).count()
        parcel_count = db.query(Parcels).count()
        procedure_count = db.query(Procedures).count()
        linked_count = db.query(LinkedUsers).count()
        
        print(f"👥 Citizens: {citizen_count}")
        print(f"💰 Tax Records: {tax_count}")
        print(f"🏠 Parcels: {parcel_count}")
        print(f"📋 Procedures: {procedure_count}")
        print(f"🔗 Linked Users: {linked_count}")
        
        print("\n🎯 KEY TEST USERS:")
        print(f"👑 Founder: Patrick Daudi ({get_patrick_phone()})")
        
        # Show Patrick's rich data
        patrick_taxes = db.query(Taxes).filter(Taxes.citizen_id == get_patrick_citizen_id()).count()
        patrick_parcels = db.query(Parcels).filter(Parcels.citizen_id == get_patrick_citizen_id()).count()
        
        print(f"   - Tax records: {patrick_taxes}")
        print(f"   - Parcels: {patrick_parcels}")
        print(f"   - Total paid: {sum(tax.amount_paid for tax in db.query(Taxes).filter(Taxes.citizen_id == get_patrick_citizen_id()).all()):,.0f} FC")
        
        print("\n🚀 Ready for testing!")
        print("Use any of the phone numbers above for chat testing.")
        
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
    finally:
        db.close()

def main():
    """Main seeding function"""
    print("🌱 KodiBOT Database Seeding - Real User Data")
    print("=" * 60)
    
    # Create tables
    print("🏗️  Creating database tables...")
    create_tables()
    print("✅ Tables created")
    
    # Clear existing data
    clear_database()
    
    # Seed data in order (citizens first, then related records)
    seed_citizens()
    seed_taxes()
    seed_parcels()
    seed_procedures()
    create_linked_users()
    
    # Print summary
    print_summary()
    
    print("\n🎉 Database seeding completed successfully!")

if __name__ == "__main__":
    main()
