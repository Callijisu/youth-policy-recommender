# Full pipeline test with detailed output
import sys
sys.path.append('.')

from orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

user_input = {
    "age": 26,
    "region": "서울",
    "employment": "학생",
    "income": 0,
    "interest": None
}

print("=== Testing Full Pipeline ===")
print(f"Input: {user_input}")

# Step 1: Agent1
print("\n--- Agent1 ---")
profile_result = orchestrator.agent1.collect_profile(user_input)
print(f"Success: {profile_result.get('success')}")
validated_profile = profile_result.get("profile_data", {})
print(f"Profile region: {validated_profile.get('region')}")

# Step 2: Agent2
print("\n--- Agent2 ---")
policies_result = orchestrator.agent2.get_policies_from_db(None)
print(f"Success: {policies_result.get('success')}")
print(f"Policy count: {policies_result.get('count', 0)}")

policies = policies_result.get('policies', [])

# Count Seoul policies
seoul_count = sum(1 for p in policies if '서울' in str(p.get('target_regions', [])))
print(f"Seoul policies: {seoul_count}")

# Step 3: Convert for Agent3
print("\n--- Convert for Agent3 ---")
policies_for_agent3 = orchestrator._convert_policies_for_agent3(policies)
print(f"Converted: {len(policies_for_agent3)}")

seoul_in_converted = sum(1 for p in policies_for_agent3 if '서울' in str(p.get('target_regions', [])))
print(f"Seoul after convert: {seoul_in_converted}")

# Step 4: Direct score calculation for one Seoul policy
print("\n--- Direct Score Test ---")
for p in policies_for_agent3:
    if '서울' in str(p.get('target_regions', [])):
        score, reasons = orchestrator.agent3.calculate_score(validated_profile, p)
        print(f"Policy: {p.get('title', 'N/A')[:30]}")
        print(f"Score: {score}")
        print(f"Reasons: {reasons[:2] if reasons else 'None'}")
        break

# Step 5: Full matching
print("\n--- Full Matching ---")
results = orchestrator.agent3.match_policies(validated_profile, policies_for_agent3, 40.0, 10)
print(f"Match results: {len(results) if results else 0}")

if results:
    for r in results[:3]:
        print(f"  - {r.title[:30]}: {r.score}")
