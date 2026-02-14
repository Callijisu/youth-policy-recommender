import sys
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())
load_dotenv()

from database.mongo_handler import get_mongodb_handler

def update_with_real_policies():
    print("🌱 실제 2026년 청년 정책으로 데이터베이스 업데이트...")

    handler = get_mongodb_handler()
    if not handler or not handler.is_connected:
        print("❌ Database not connected")
        return False

    # 기존 정책들 삭제
    policies_collection = handler.database["policies"]
    policies_collection.delete_many({})
    print("🗑️ 기존 정책 데이터 삭제 완료")

    # 실제 2026년 청년 정책들
    real_policies = [
        {
            "policy_id": "YFS_2026_001",
            "title": "청년미래적금",
            "category": "금융",
            "target_age_min": 19,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["재직자", "구직자"],
            "target_income_max": 6000,  # 개인소득 6천만원 이하
            "benefit": "3년 동안 최대 2,200만원 목돈 마련, 우대형 최대 16.9% 연이율",
            "budget_max": 2200,
            "deadline": "2026-12-31",  # 연중 신청 가능
            "application_url": "https://www.youthcenter.go.kr",
            "agency": "기획재정부",
            "is_active": True,
            "requirements": ["중소기업 재직자 우대", "가구 중위소득 200% 이하"]
        },
        {
            "policy_id": "YJB_2026_001",
            "title": "청년일자리 도약장려금",
            "category": "일자리",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["비수도권"],  # 비수도권 중소기업
            "target_employment": ["구직자"],
            "target_income_max": 4000,
            "benefit": "중소기업 취업시 장려금 지급, 6개월~1년 지원",
            "budget_max": 600,
            "deadline": "상시",  # 상시 신청 가능
            "application_url": "https://www.work.go.kr",
            "agency": "고용노동부",
            "is_active": True,
            "requirements": ["비수도권 중소기업 취업"]
        },
        {
            "policy_id": "SPL_2026_001",
            "title": "서울청년정책네트워크",
            "category": "교육",
            "target_age_min": 19,
            "target_age_max": 39,
            "target_regions": ["서울"],
            "target_employment": ["재직자", "구직자", "학생", "자영업"],
            "target_income_max": None,  # 소득 제한 없음
            "benefit": "청년정책 참여 및 제안 기회, 활동비 지급",
            "budget_max": 100,
            "deadline": "2026-01-23",  # 실제 마감일
            "application_url": "https://youth.seoul.go.kr",
            "agency": "서울특별시",
            "is_active": True,
            "requirements": ["서울시 거주 또는 활동"]
        },
        {
            "policy_id": "YDR_2026_001",
            "title": "청년 부채 경감 정책",
            "category": "금융",
            "target_age_min": 19,
            "target_age_max": 39,
            "target_regions": ["서울"],
            "target_employment": ["재직자", "구직자", "학생"],
            "target_income_max": 5000,
            "benefit": "학자금 대출 이자 지원, 신용회복 지원, 긴급생활자금",
            "budget_max": 1000,
            "deadline": "2026-11-20",  # 실제 마감일
            "application_url": "https://youth.seoul.go.kr",
            "agency": "서울특별시",
            "is_active": True,
            "requirements": ["서울시 거주", "부채 보유자"]
        },
        {
            "policy_id": "TSA_2026_001",
            "title": "내일준비적금 확대",
            "category": "금융",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["재직자", "구직자", "군인"],  # 군 초급간부 포함
            "target_income_max": 4000,
            "benefit": "3년 적금 + 정부 기여금, 연 4-6% 수익률",
            "budget_max": 1800,
            "deadline": "상시",
            "application_url": "https://www.work.go.kr",
            "agency": "고용노동부",
            "is_active": True,
            "requirements": ["중소기업 재직자 우대"]
        },
        {
            "policy_id": "TRP_2026_001",
            "title": "K-패스 대중교통 정액패스",
            "category": "복지",
            "target_age_min": 19,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["재직자", "구직자", "학생"],
            "target_income_max": 3000,
            "benefit": "월 20만원 한도 대중교통 무제한, 20-53% 할인",
            "budget_max": 20,
            "deadline": "상시",
            "application_url": "https://www.ktcard.co.kr",
            "agency": "국토교통부",
            "is_active": True,
            "requirements": ["대중교통 이용자"]
        },
        {
            "policy_id": "TAX_2026_001",
            "title": "청년 근로소득 공제 확대",
            "category": "금융",
            "target_age_min": 19,
            "target_age_max": 34,  # 34세로 확대
            "target_regions": ["전국"],
            "target_employment": ["재직자"],
            "target_income_max": 7000,
            "benefit": "근로소득공제 60만원 + 30% 추가공제",
            "budget_max": 120,
            "deadline": "연말정산시",
            "application_url": "https://www.nts.go.kr",
            "agency": "국세청",
            "is_active": True,
            "requirements": ["근로자"]
        },
        {
            "policy_id": "EMP_2026_001",
            "title": "국민취업지원제도",
            "category": "일자리",
            "target_age_min": 18,
            "target_age_max": 64,  # 청년 외에도 전연령
            "target_regions": ["전국"],
            "target_employment": ["구직자"],
            "target_income_max": None,  # 소득 요건 별도
            "benefit": "취업지원서비스 + 구직급여 월 50만원(6개월)",
            "budget_max": 300,
            "deadline": "상시",
            "application_url": "https://www.work.go.kr",
            "agency": "고용노동부",
            "is_active": True,
            "requirements": ["구직 의사 및 구직활동"]
        },
        {
            "policy_id": "HOU_2026_001",
            "title": "청년 주거급여",
            "category": "주거",
            "target_age_min": 19,
            "target_age_max": 30,
            "target_regions": ["전국"],
            "target_employment": ["재직자", "구직자", "학생"],
            "target_income_max": None,  # 중위소득 기준 별도
            "benefit": "월세 지원, 지역별 기준임대료 범위 내",
            "budget_max": 384,  # 월 최대 32만원 x 12개월
            "deadline": "상시",
            "application_url": "https://www.bokjiro.go.kr",
            "agency": "국토교통부",
            "is_active": True,
            "requirements": ["중위소득 46% 이하", "부모와 별거"]
        },
        {
            "policy_id": "OVS_2026_001",
            "title": "K-Move 해외취업지원",
            "category": "일자리",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["구직자"],
            "target_income_max": None,
            "benefit": "해외취업 연수·교육비, 항공료, 정착금 지원",
            "budget_max": 500,
            "deadline": "2026-10-31",
            "application_url": "https://www.work.go.kr",
            "agency": "고용노동부",
            "is_active": True,
            "requirements": ["어학능력", "해외취업 의지"]
        },
        {
            "policy_id": "STU_2026_001",
            "title": "청년내일학습카드",
            "category": "교육",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["구직자", "재직자", "자영업"],
            "target_income_max": None,
            "benefit": "직업훈련비 최대 500만원 지원 (5년간)",
            "budget_max": 500,
            "deadline": "상시",
            "application_url": "https://www.hrd.go.kr",
            "agency": "고용노동부",
            "is_active": True,
            "requirements": ["직업훈련 수강 의지"]
        },
        {
            "policy_id": "START_2026_001",
            "title": "청년창업사관학교",
            "category": "창업",
            "target_age_min": 18,
            "target_age_max": 39,
            "target_regions": ["전국"],
            "target_employment": ["구직자", "재직자", "자영업", "학생"],
            "target_income_max": None,
            "benefit": "창업교육 + 최대 1억원 사업화 자금",
            "budget_max": 10000,
            "deadline": "2026-04-30",  # 일반적인 상반기 모집 마감
            "application_url": "https://start.kosmes.or.kr",
            "agency": "중소벤처기업부",
            "is_active": True,
            "requirements": ["창업 아이템 보유", "창업 의지"]
        }
    ]

    # 정책 삽입
    print(f"📝 {len(real_policies)}개의 실제 정책 삽입 중...")
    for policy in real_policies:
        # 기존 정책 확인 후 업데이트 또는 삽입
        existing_policy = policies_collection.find_one({"policy_id": policy["policy_id"]})

        if existing_policy:
            policies_collection.update_one(
                {"policy_id": policy["policy_id"]},
                {"$set": policy}
            )
            print(f"   Updated: {policy['title']}")
        else:
            # 새 정책 삽입
            policy["created_at"] = datetime.now()
            policy["updated_at"] = datetime.now()
            result = policies_collection.insert_one(policy)
            print(f"   Inserted: {policy['title']}")

    print(f"✅ {len(real_policies)}개의 실제 정책으로 업데이트 완료")
    return True

if __name__ == "__main__":
    success = update_with_real_policies()
    if success:
        print("\n✅ 실제 2026년 청년 정책 업데이트 성공!")
    else:
        print("\n❌ 정책 업데이트 실패")