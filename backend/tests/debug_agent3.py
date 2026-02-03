"""Debug Agent3 matching directly"""
import sys
sys.path.append('.')
from database.mongo_handler import get_mongodb_handler
from agents.agent3_matching import Agent3

def debug_matching():
    # DB에서 서울 정책 몇 개 가져오기
    handler = get_mongodb_handler()
    db = handler.client['youth_policy']
    
    # 서울 정책 5개 샘플
    policies = list(db['policies'].find({"target_regions": {"$regex": "서울"}}).limit(5))
    print(f"서울 정책 {len(policies)}개 샘플:")
    for p in policies:
        print(f"  - {p.get('title', 'N/A')[:30]}")
        print(f"    지역: {p.get('target_regions')}")
        print(f"    나이: {p.get('target_age_min')}-{p.get('target_age_max')}")
    
    # Agent3로 직접 테스트
    agent3 = Agent3()
    user_profile = {
        "age": 26,
        "region": "서울",
        "employment": "학생",
        "income": 0
    }
    
    print(f"\n사용자 프로필: {user_profile}")
    
    # 단일 정책 점수 계산 테스트
    if policies:
        test_policy = policies[0]
        print(f"\n테스트 정책: {test_policy.get('title', 'N/A')[:40]}")
        score, reasons = agent3.calculate_score(user_profile, test_policy)
        print(f"  점수: {score}")
        print(f"  사유: {reasons}")
        
        # 지역 매칭 직접 테스트
        region_match, region_score = agent3.check_region_match(
            user_profile.get("region"),
            test_policy.get("target_regions")
        )
        print(f"  지역 매칭: {region_match}, 점수: {region_score}")

if __name__ == "__main__":
    debug_matching()
