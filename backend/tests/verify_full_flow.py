
import sys
import os
import json
from dotenv import load_dotenv

sys.path.append(os.getcwd())
load_dotenv()

from orchestrator import AgentOrchestrator

def verify_full_flow():
    print("🔄 Full Agent Flow Verification...")
    
    # 1. Initialize Orchestrator
    try:
        orchestrator = AgentOrchestrator(use_database=True)
        print("✅ Orchestrator Initialized")
    except Exception as e:
        print(f"❌ Orchestrator Initialization Failed: {e}")
        return False

    # 2. Define User Input (Targeting seeded policies)
    # Seeded: JOB_001 (15-34, Nationwide, Job Seeker)
    user_input = {
        "age": 25,
        "region": "서울",
        "income": 0,
        "employment": "구직자",
        "interest": "일자리"
    }
    
    print(f"\n👤 Processing for User: {user_input}")
    
    # 3. Process Recommendation
    try:
        result = orchestrator.process_recommendation(user_input)
    except Exception as e:
        print(f"❌ process_recommendation failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    # 4. Analyze Result
    if result.get("success"):
        print("\n✅ Recommendation Successful!")
        print(f"   Session ID: {result.get('session_id')}")
        
        # Check Steps
        steps = result.get("steps_summary", [])
        print("\n📊 Agent Steps Status:")
        for step in steps:
            status_icon = "✅" if step.get("success") else "❌"
            print(f"   {status_icon} {step.get('agent_name')}: {step.get('duration', 0):.2f}s")
            if not step.get("success"):
                print(f"      Error: {step.get('error_message')}")
        
        # Check Recommendations
        rec_result = result.get("recommendation_result", {})
        recs = rec_result.get("recommendations", [])
        print(f"\n🎁 Recommendations Found: {len(recs)}")
        
        if len(recs) == 0:
            print("⚠️ Warning: 0 recommendations found. Check matching logic or seed data coverage.")
            # We expect at least JOB_001 to match
            return False
            
        for i, rec in enumerate(recs, 1):
             print(f"   {i}. [{rec.get('score_grade')}] {rec.get('policy_name')} (Score: {rec.get('score')})")
             print(f"      Agency: {rec.get('agency')}")
             # Check if explanation exists (Agent 4)
             if rec.get("explanation"):
                 print(f"      Explanation: {rec.get('explanation')[:50]}...")
             else:
                 print("      Explanation: (Missing)")
        
        return True

    else:
        print(f"\n❌ Recommendation Failed: {result.get('error_detail')}")
        return False

if __name__ == "__main__":
    if verify_full_flow():
        print("\n✅ Full Flow Verification SUCCESS")
        sys.exit(0)
    else:
        print("\n❌ Full Flow Verification FAILED")
        sys.exit(1)
