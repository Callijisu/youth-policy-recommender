
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.getcwd())
load_dotenv()

from agents.agent2_data import Agent2, PolicyFilter

def verify_agent2():
    print("🔍 Agent 2 Verification...")
    
    agent = Agent2(use_database=True)
    if not agent.db_handler or not agent.db_handler.is_connected:
         print("❌ Agent 2 failed to connect to DB")
         return False

    print(f"✅ Agent 2 initialized with DB: {agent.db_handler.database_name}")

    # 1. Get Policies from DB
    print("\n📝 Fetching policies from DB...")
    result = agent.get_policies_from_db()
    
    if result.get("success"):
        print(f"✅ Policies found: {result.get('count', 0)}")
        if result.get("policies"):
            print(f"   Sample: {result['policies'][0].get('title')}")
        else:
            print("   (No policies found in DB, which is expected if DB is empty, but strictness passed)")
    else:
        print(f"❌ Policy fetch failed: {result.get('error')}")
        return False

    # 2. Check API strictness (should fail/return empty, NOT dummy)
    print("\n📝 Checking API strictness...")
    try:
        api_result = agent.collect_from_api()
        if not api_result.get("success") and "추후 구현 예정" in api_result.get("error", ""):
             print("✅ API strictness passed (returned explicit not-implemented error)")
        else:
             print("❌ API strictness failed. Returned unexpected success or wrong error.")
             print(f"   Result: {api_result}")
             return False
    except Exception as e:
        print(f"❌ API check exception: {e}")
        return False

    return True

if __name__ == "__main__":
    if verify_agent2():
        print("\n✅ Verification SUCCESS")
        sys.exit(0)
    else:
        print("\n❌ Verification FAILED")
        sys.exit(1)
