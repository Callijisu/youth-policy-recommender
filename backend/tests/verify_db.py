
import sys
import os
import time
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())

# Load environment variables
load_dotenv()

from database.mongo_handler import get_mongodb_handler

def verify_db():
    print("🔍 Database Verification Starting...")
    
    try:
        handler = get_mongodb_handler()
        connection_status = handler.test_connection()
        
        if not connection_status.get("connected"):
            print("❌ MongoDB Not Connected")
            print(f"Error: {connection_status.get('error')}")
            return False
            
        print(f"✅ MongoDB Connected: {connection_status.get('database_name')}")
        
        # Check Policies
        policies = handler.get_all_policies()
        if policies.get("success"):
            count = policies.get("count", 0)
            print(f"✅ Policies Found: {count}")
            if count == 0:
                print("⚠️ Warning: 0 policies found in DB. The application will return empty lists.")
            else:
                print("  Sample Policy Titles:")
                for p in policies.get("policies", [])[:3]:
                    print(f"  - {p.get('title')}")
        else:
            print(f"❌ Policy Retrieval Failed: {policies.get('error')}")
            return False
            
        return True

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    if verify_db():
        print("\n✅ Verification SUCCESS")
        sys.exit(0)
    else:
        print("\n❌ Verification FAILED")
        sys.exit(1)
