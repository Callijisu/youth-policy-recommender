
import os
import sys
# Add backend directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mongo_handler import MongoDBHandler
from dotenv import load_dotenv

load_dotenv()

def inspect_policy():
    handler = MongoDBHandler()
    if not handler.is_connected:
        print("Failed to connect to MongoDB")
        return

    # Count policies
    count = handler.database["policies"].count_documents({})
    print(f"\nTotal Policies: {count}")

    # Check diversity
    regions = handler.database["policies"].distinct("target_regions")
    print(f"Unique Regions: {regions}")
    
    agencies = handler.database["policies"].distinct("agency")
    print(f"Unique Agencies (first 5): {agencies[:5]}")
    
    # Check if filtering fields exist
    sample = handler.database["policies"].find_one()
    print("\nSample Filter Fields:")
    print(f"Age: {sample.get('target_age_min')} - {sample.get('target_age_max')}")
    print(f"Employment: {sample.get('target_employment')}")
    print(f"Income: {sample.get('target_income_max')}")

if __name__ == "__main__":
    inspect_policy()
