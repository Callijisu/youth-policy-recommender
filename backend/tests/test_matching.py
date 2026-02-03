"""Test orchestrator directly"""
import sys
sys.path.append('.')
from agents.agent3_matching import Agent3

def test_matching():
    agent3 = Agent3()
    
    # 테스트 사용자 프로필
    user_profile = {
        "age": 26,
        "region": "서울",
        "status": "재학생",
        "income": 0
    }
    
    print(f"테스트 프로필: {user_profile}")
    
    # 매칭 실행
    result = agent3.match_policies(user_profile)
    
    if result["success"]:
        print(f"\n✅ 매칭 성공!")
        print(f"매칭된 정책 수: {result.get('matched_count', 0)}")
        policies = result.get("policies", [])
        for i, p in enumerate(policies[:5]):
            print(f"  {i+1}. {p.get('title', 'N/A')[:40]} | 점수: {p.get('match_score', 0)}")
    else:
        print(f"\n❌ 매칭 실패: {result.get('error')}")

if __name__ == "__main__":
    test_matching()
