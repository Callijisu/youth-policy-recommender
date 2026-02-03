# Quick test to check profile_data format
import sys
sys.path.append('.')

from agents.agent1_profile import Agent1

agent1 = Agent1(use_database=False)  # Skip DB for quick test

user_input = {
    "age": 26,
    "region": "서울",  
    "employment": "학생",
    "income": 0,
    "interest": None
}

result = agent1.collect_profile(user_input)

print("Success:", result.get("success"))
if result.get("success"):
    profile_data = result.get("profile_data", {})
    print("Profile data keys:", list(profile_data.keys()))
    print("age:", profile_data.get("age"), type(profile_data.get("age")))
    print("region:", profile_data.get("region"), type(profile_data.get("region")))
    print("employment:", profile_data.get("employment"), type(profile_data.get("employment")))
    print("income:", profile_data.get("income"), type(profile_data.get("income")))
else:
    print("Error:", result.get("error"))
