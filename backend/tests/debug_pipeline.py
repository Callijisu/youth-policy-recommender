"""Full debug of orchestrator pipeline"""
import sys
sys.path.append('.')
from orchestrator import AgentOrchestrator

def debug_full_pipeline():
    orchestrator = AgentOrchestrator()
    
    user_profile = {
        "age": 26,
        "region": "서울",
        "employment": "학생",
        "income": 0,
        "interest": None
    }
    
    print(f"사용자 프로필: {user_profile}")
    print("=" * 60)
    
    # Step 1: Agent1 프로필 검증
    print("\n[Step 1] Agent1 프로필 검증")
    profile_result = orchestrator.agent1.collect_profile(user_profile)
    print(f"  성공: {profile_result.get('success')}")
    if not profile_result.get('success'):
        print(f"  에러: {profile_result.get('error')}")
        return
        
    validated_profile = profile_result.get("profile_data", profile_result.get("profile", {}))
    print(f"  검증된 프로필: {validated_profile}")
    
    # Step 2: Agent2 정책 조회
    print("\n[Step 2] Agent2 정책 조회")
    policies_result = orchestrator.agent2.get_policies_from_db(None)
    print(f"  성공: {policies_result.get('success')}")
    print(f"  정책 수: {policies_result.get('count', 0)}")
    
    if policies_result.get('success') and policies_result.get('policies'):
        policies = policies_result['policies']
        
        # 서울 정책 샘플 확인
        seoul_policies = [p for p in policies if '서울' in str(p.get('target_regions', []))]
        print(f"  서울 정책 수: {len(seoul_policies)}")
        
        if seoul_policies:
            sample = seoul_policies[0]
            print(f"\n  서울 정책 샘플:")
            print(f"    title: {sample.get('title', 'N/A')[:40]}")
            print(f"    target_regions: {sample.get('target_regions')}")
            print(f"    target_age_min: {sample.get('target_age_min')}")
            print(f"    target_age_max: {sample.get('target_age_max')}")
        
        # Step 3: Agent3 형식으로 변환
        print("\n[Step 3] Agent3 형식 변환")
        policies_for_agent3 = orchestrator._convert_policies_for_agent3(policies)
        print(f"  변환된 정책 수: {len(policies_for_agent3)}")
        
        # 서울 정책 샘플 확인
        seoul_policies_3 = [p for p in policies_for_agent3 if '서울' in str(p.get('target_regions', []))]
        print(f"  변환 후 서울 정책 수: {len(seoul_policies_3)}")
        
        if seoul_policies_3:
            sample3 = seoul_policies_3[0]
            print(f"\n  변환된 서울 정책 샘플:")
            print(f"    target_regions: {sample3.get('target_regions')}")
        
        # Step 4: Agent3 매칭
        print("\n[Step 4] Agent3 매칭")
        matching_results = orchestrator.agent3.match_policies(
            validated_profile, policies_for_agent3, 40.0, 10
        )
        print(f"  매칭 결과: {len(matching_results) if matching_results else 0}개")
        
        if matching_results:
            for i, result in enumerate(matching_results[:3]):
                print(f"  {i+1}. {result.policy_name[:30]} - 점수: {result.score}")
    else:
        print(f"  에러: {policies_result.get('error')}")

if __name__ == "__main__":
    debug_full_pipeline()
