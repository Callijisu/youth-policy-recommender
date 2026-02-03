"""Test full orchestrator flow"""
import sys
sys.path.append('.')
from orchestrator import AgentOrchestrator

def test_orchestrator():
    orchestrator = AgentOrchestrator()
    
    # 테스트 사용자 프로필
    user_profile = {
        "age": 26,
        "region": "서울",
        "employment": "학생",  # 학생, 재직자, 구직자, 자영업, 무직 중 하나
        "income": 0,
        "interest": None
    }
    
    print(f"테스트 프로필: {user_profile}")
    print("=" * 50)
    
    # Orchestrator 실행
    result = orchestrator.process_recommendation(user_profile)
    
    print(f"\n결과:")
    print(f"  success: {result.get('success')}")
    print(f"  message: {result.get('message', 'N/A')}")
    
    policies = result.get("policies", [])
    print(f"  policies count: {len(policies)}")
    
    if policies:
        print("\n상위 5개 정책:")
        for i, p in enumerate(policies[:5]):
            print(f"  {i+1}. {p.get('title', 'N/A')[:40]}")
            print(f"      점수: {p.get('match_score', 0)}, 지역: {p.get('target_regions')}")
    else:
        print("\n❌ 정책이 없습니다!")
        # 더 자세한 디버깅
        if "error" in result:
            print(f"  에러: {result['error']}")

if __name__ == "__main__":
    test_orchestrator()
