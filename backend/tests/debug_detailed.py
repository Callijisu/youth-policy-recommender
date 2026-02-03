# -*- coding: utf-8 -*-
"""Detailed debug of orchestrator data flow - ASCII output only"""
import sys
sys.path.append('.')

# Set UTF-8 output
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from orchestrator import AgentOrchestrator

def debug():
    orchestrator = AgentOrchestrator()
    
    user_input = {
        "age": 26,
        "region": "서울",
        "employment": "학생",
        "income": 0,
        "interest": None
    }
    
    print("=== Step 1: Agent1 ===")
    profile_result = orchestrator.agent1.collect_profile(user_input)
    print(f"Success: {profile_result.get('success')}")
    
    if not profile_result.get('success'):
        print(f"Error: {profile_result.get('error')}")
        return
    
    validated_profile = profile_result.get("profile_data", profile_result.get("profile", {}))
    print(f"Profile keys: {list(validated_profile.keys()) if isinstance(validated_profile, dict) else type(validated_profile)}")
    print(f"Profile age: {validated_profile.get('age') if isinstance(validated_profile, dict) else 'N/A'}")
    print(f"Profile region: {validated_profile.get('region') if isinstance(validated_profile, dict) else 'N/A'}")
    
    print("\n=== Step 2: Agent2 ===")
    policies_result = orchestrator.agent2.get_policies_from_db(None)
    print(f"Success: {policies_result.get('success')}")
    print(f"Count: {policies_result.get('count', 0)}")
    
    if not policies_result.get('success'):
        print(f"Error: {policies_result.get('error')}")
        return
    
    policies = policies_result.get('policies', [])
    
    # Find Seoul policies
    seoul_count = 0
    sample_seoul = None
    for p in policies:
        regions = p.get('target_regions', [])
        if regions and '서울' in str(regions):
            seoul_count += 1
            if sample_seoul is None:
                sample_seoul = p
    
    print(f"Seoul policies in Agent2 result: {seoul_count}")
    
    if sample_seoul:
        print(f"Sample Seoul policy regions: {sample_seoul.get('target_regions')}")
        print(f"Sample Seoul policy age: {sample_seoul.get('target_age_min')}-{sample_seoul.get('target_age_max')}")
    
    print("\n=== Step 3: Convert for Agent3 ===")
    policies_for_agent3 = orchestrator._convert_policies_for_agent3(policies)
    print(f"Converted count: {len(policies_for_agent3)}")
    
    # Find Seoul in converted
    seoul_count_3 = 0
    sample_seoul_3 = None
    for p in policies_for_agent3:
        regions = p.get('target_regions', [])
        if regions and '서울' in str(regions):
            seoul_count_3 += 1
            if sample_seoul_3 is None:
                sample_seoul_3 = p
    
    print(f"Seoul policies after conversion: {seoul_count_3}")
    
    if sample_seoul_3:
        print(f"Converted Seoul policy regions: {sample_seoul_3.get('target_regions')}")
    
    print("\n=== Step 4: Agent3 Matching ===")
    # Test single policy directly
    if sample_seoul_3:
        score, reasons = orchestrator.agent3.calculate_score(validated_profile, sample_seoul_3)
        print(f"Direct score test: {score}")
        print(f"Reasons: {reasons}")
    
    # Full matching
    matching_results = orchestrator.agent3.match_policies(
        validated_profile, policies_for_agent3, 40.0, 10
    )
    print(f"Match results: {len(matching_results) if matching_results else 0}")

if __name__ == "__main__":
    debug()
