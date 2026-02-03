
import sys
import os
import time
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())

# Load environment variables
load_dotenv()

from agents.agent1_profile import Agent1
from database.mongo_handler import get_mongodb_handler

def verify_agent1_db():
    print("🔍 Agent 1 DB Integration Verification...")
    
    # 1. Initialize Agent with DB
    agent = Agent1(use_database=True)
    if not agent.db_handler or not agent.db_handler.is_connected:
        print("❌ Agent 1 failed to connect to DB")
        return False
        
    print(f"✅ Agent 1 initialized with DB: {agent.db_handler.database_name}")

    # 2. Collect Profile
    test_data = {
        "age": 28,
        "region": "서울",
        "income": 3500,
        "employment": "재직자",
        "interest": "창업"
    }
    
    print("\n📝 Collecting Profile...")
    result = agent.collect_profile(test_data)
    
    if not result.get("success"):
        print(f"❌ collect_profile failed: {result.get('error')}")
        return False
        
    profile_id = result.get("profile_id")
    print(f"✅ collect_profile success: {profile_id}")
    
    # 3. Verify Database Saved Flag
    if not result.get("database_saved"):
        print("❌ 'database_saved' flag is missing or False")
        if result.get("database_error"):
            print(f"   Error: {result.get('database_error')}")
        return False
    print("✅ 'database_saved' flag is True")

    # 4. Verify Actual DB Content
    print("\n💾 Verifying content in MongoDB...")
    handler = get_mongodb_handler()
    profile_in_db = handler.get_user_profile(profile_id)
    
    if not profile_in_db.get("success"):
         print(f"❌ Failed to fetch profile from DB: {profile_in_db.get('error')}")
         return False
         
    fetched_data = profile_in_db.get("profile", {})
    if fetched_data.get("region") == "서울" and fetched_data.get("interest") == "창업":
        print("✅ Profile data matches in DB")
    else:
        print("❌ Profile data mismatch in DB")
        print(f"   Expected: {test_data}")
        print(f"   Got: {fetched_data}")
        return False

    return True

if __name__ == "__main__":
    if verify_agent1_db():
        print("\n✅ Verification SUCCESS")
        sys.exit(0)
    else:
        print("\n❌ Verification FAILED")
        sys.exit(1)
