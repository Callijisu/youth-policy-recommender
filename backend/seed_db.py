
import sys
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())
load_dotenv()

from database.mongo_handler import get_mongodb_handler

def seed_database():
    print("🌱 Database Seeding Starting...")
    
    handler = get_mongodb_handler()
    if not handler or not handler.is_connected:
        print("❌ Database not connected")
        return False

    # Sample Policies
    policies = [
        {
            "policy_id": "JOB_001",
            "title": "청년내일채움공제",
            "category": "일자리",
            "target_age_min": 15,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["구직자", "재직자"],
            "target_income_max": 4000, # 연소득 4000만원 이하로 상향
            "benefit": "2년 만기시 300만원~1200만원 지급",
            "budget_max": 1200,
            "deadline": "2026-12-31",
            "application_url": "https://www.work.go.kr",
            "agency": "고용노동부",
            "is_active": True
        },
        {
            "policy_id": "FIN_001",
            "title": "청년희망적금",
            "category": "금융",
            "target_age_min": 19,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["재직자", "구직자", "자영업"],
            "target_income_max": 5000,
            "benefit": "월 10만원 적립시 정부지원금 10만원 추가 적립",
            "budget_max": 240,
            "deadline": "2026-12-31",
            "application_url": "https://www.finlife.or.kr",
            "agency": "금융위원회",
            "is_active": True
        },
        {
            "policy_id": "HOU_001",
            "title": "청년 전세자금대출",
            "category": "주거",
            "target_age_min": 19,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["재직자", "구직자"],
            "target_income_max": 6000,
            "benefit": "전세자금 최대 2억원 대출",
            "budget_max": 20000,
            "deadline": "연중 상시",
            "application_url": "https://www.hf.go.kr",
            "agency": "국토교통부",
            "is_active": True
        },
        {
            "policy_id": "STARTUP_001",
            "title": "청년창업사관학교",
            "category": "창업",
            "target_age_min": 18,
            "target_age_max": 39,
            "target_regions": ["전국"],
            "target_employment": ["구직자", "재직자", "자영업", "학생"],
            "target_income_max": 0, # 제한없음
            "benefit": "최대 1억원 사업화 자금 지원",
            "budget_max": 10000,
            "deadline": "2026-12-31",
            "application_url": "https://start.kosmes.or.kr",
            "agency": "중소벤처기업부",
            "is_active": True
        },
         {
            "policy_id": "WEL_001",
            "title": "청년마음건강지원사업",
            "category": "복지",
            "target_age_min": 19,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["재직자", "구직자", "자영업", "학생", "무직"],
            "target_income_max": 0,
            "benefit": "전문 심리상담 10회 지원",
            "budget_max": 100,
            "deadline": "연중 상시",
            "application_url": "https://www.bokjiro.go.kr",
             "agency": "보건복지부",
             "is_active": True
        },
        {
            "policy_id": "EDU_001",
            "title": "청년도약계좌",
            "category": "금융",
            "target_age_min": 19,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["재직자", "구직자"],
            "target_income_max": 6000,
            "benefit": "5년 만기시 최대 5000만원 적립 지원",
            "budget_max": 5000,
            "deadline": "2027-12-31",
            "application_url": "https://www.nhbank.com",
            "agency": "기획재정부",
            "is_active": True
        },
        {
            "policy_id": "JOB_002",
            "title": "국민취업지원제도",
            "category": "일자리",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["구직자"],  # 구직자만 대상
            "target_income_max": 4000,  # 소득 제한 추가
            "benefit": "구직급여 월 50만원 + 취업지원서비스",
            "budget_max": 300,
            "deadline": "2026-12-31",  # 마감일 변경
            "application_url": "https://www.work.go.kr",
            "agency": "고용노동부",
            "is_active": True
        },
        {
            "policy_id": "EDU_002",
            "title": "청년내일학습카드",
            "category": "교육",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["구직자", "재직자", "자영업"],
            "target_income_max": 0,
            "benefit": "직업훈련비 최대 500만원 지원",
            "budget_max": 500,
            "deadline": "연중 상시",
            "application_url": "https://www.hrd.go.kr",
            "agency": "고용노동부",
            "is_active": True
        },
        {
            "policy_id": "STARTUP_002",
            "title": "청년창업펀드",
            "category": "창업",
            "target_age_min": 18,
            "target_age_max": 39,
            "target_regions": ["전국"],
            "target_employment": ["구직자", "재직자", "자영업", "학생"],
            "target_income_max": 0,
            "benefit": "창업자금 최대 3억원 투자",
            "budget_max": 30000,
            "deadline": "2026-12-31",
            "application_url": "https://www.kosmes.or.kr",
            "agency": "중소벤처기업부",
            "is_active": True
        },
        {
            "policy_id": "HOU_002",
            "title": "청년 주거급여",
            "category": "주거",
            "target_age_min": 19,
            "target_age_max": 30,  # 30세까지만
            "target_regions": ["전국"],
            "target_employment": ["재직자", "구직자"],  # 학생/자영업 제외
            "target_income_max": 2400,  # 낮은 소득 제한
            "benefit": "월 최대 32만원 주거비 지원",
            "budget_max": 384,
            "deadline": "2026-12-31",  # 업데이트된 마감일
            "application_url": "https://www.bokjiro.go.kr",
            "agency": "국토교통부",
            "is_active": True
        },
        {
            "policy_id": "CUL_001",
            "title": "청년문화패스",
            "category": "문화",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["재직자", "구직자", "학생", "자영업"],
            "target_income_max": 0,
            "benefit": "문화활동비 연 10만원 지원",
            "budget_max": 10,
            "deadline": "2027-12-31",
            "application_url": "https://www.mcst.go.kr",
            "agency": "문화체육관광부",
            "is_active": True
        },
        {
            "policy_id": "JOB_003",
            "title": "청년디지털일자리",
            "category": "일자리",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["구직자"],
            "target_income_max": 0,
            "benefit": "디지털 분야 취업연계 + 교육지원",
            "budget_max": 200,
            "deadline": "2026-12-31",
            "application_url": "https://www.work.go.kr",
            "agency": "고용노동부",
            "is_active": True
        },
        {
            "policy_id": "MIL_001",
            "title": "병역이행자 취업지원",
            "category": "일자리",
            "target_age_min": 20,
            "target_age_max": 35,
            "target_regions": ["전국"],
            "target_employment": ["구직자"],
            "target_income_max": 0,
            "benefit": "취업알선 + 면접비 지원",
            "budget_max": 50,
            "deadline": "연중 상시",
            "application_url": "https://www.mma.go.kr",
            "agency": "국방부",
            "is_active": True
        },
        {
            "policy_id": "RURAL_001",
            "title": "청년농업인정착지원",
            "category": "농업",
            "target_age_min": 18,
            "target_age_max": 40,
            "target_regions": ["전국"],
            "target_employment": ["구직자", "자영업"],
            "target_income_max": 0,
            "benefit": "영농정착지원금 연 1200만원 (3년간)",
            "budget_max": 3600,
            "deadline": "2026-12-31",
            "application_url": "https://www.mafra.go.kr",
            "agency": "농림축산식품부",
            "is_active": True
        },
        {
            "policy_id": "SEOUL_001",
            "title": "서울 청년월세지원",
            "category": "주거",
            "target_age_min": 19,
            "target_age_max": 39,
            "target_regions": ["서울"],
            "target_employment": ["재직자", "구직자", "학생", "자영업"],
            "target_income_max": 4800,
            "benefit": "월세 최대 20만원 지원 (10개월)",
            "budget_max": 200,
            "deadline": "2027-12-31",
            "application_url": "https://www.seoul.go.kr",
            "agency": "서울특별시",
            "is_active": True
        },
        {
            "policy_id": "K_MOVE_001",
            "title": "K-Move 해외취업지원",
            "category": "일자리",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["구직자"],
            "target_income_max": 0,
            "benefit": "해외취업 항공료 + 정착금 지원",
            "budget_max": 300,
            "deadline": "2026-12-31",
            "application_url": "https://www.work.go.kr",
            "agency": "고용노동부",
            "is_active": True
        },
        {
            "policy_id": "TECH_001",
            "title": "청년AI아카데미",
            "category": "교육",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["구직자", "재직자"],
            "target_income_max": 0,
            "benefit": "AI 전문교육 + 취업연계",
            "budget_max": 0,
            "deadline": "2026-12-31",
            "application_url": "https://www.msit.go.kr",
            "agency": "과학기술정보통신부",
            "is_active": True
        },
        {
            "policy_id": "SOCIAL_001",
            "title": "청년사회혁신가육성",
            "category": "창업",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["구직자", "재직자", "학생"],
            "target_income_max": 0,
            "benefit": "사회문제해결 프로젝트 지원금 500만원",
            "budget_max": 500,
            "deadline": "2026-12-31",
            "application_url": "https://www.korea.kr",
            "agency": "행정안전부",
            "is_active": True
        },
        {
            "policy_id": "BUSAN_001",
            "title": "부산 청년구직활동지원금",
            "category": "일자리",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["부산"],
            "target_employment": ["구직자"],
            "target_income_max": 3600,
            "benefit": "구직활동비 월 30만원 (6개월)",
            "budget_max": 180,
            "deadline": "2027-12-31",
            "application_url": "https://www.busan.go.kr",
            "agency": "부산광역시",
            "is_active": True
        },
        {
            "policy_id": "GREEN_001",
            "title": "그린뉴딜청년인턴십",
            "category": "일자리",
            "target_age_min": 18,
            "target_age_max": 34,
            "target_regions": ["전국"],
            "target_employment": ["구직자"],
            "target_income_max": 0,
            "benefit": "친환경 분야 인턴십 + 월 200만원",
            "budget_max": 1200,
            "deadline": "2026-12-31",
            "application_url": "https://www.motie.go.kr",
            "agency": "산업통상자원부",
            "is_active": True
        }
    ]

    print(f"📝 Inserting/Updating {len(policies)} policies...")
    
    count = 0
    for policy in policies:
        # Check if exists
        # There is no direct single update method in handler exposed nicely for "upsert by policy_id"
        # but save_policy might behave as insert.
        # Let's inspect handler.save_policy?
        # Assuming save_policy inserts. If we want idempotency, we should delete first or use upsert logic.
        # Handler 'save_policy' logic (from memory/view) uses insert_one usually.
        # Let's try to delete defaults first to be clean.
        
        # We can directly access collection via handler.db['policies']
        try:
            handler.database['policies'].delete_many({"policy_id": policy["policy_id"]})
            handler.database['policies'].insert_one(policy)
            print(f"   Saved: {policy['title']}")
            count += 1
        except Exception as e:
            print(f"   Failed to save {policy['title']}: {e}")

    print(f"✅ Seeded {count} policies.")
    return True

if __name__ == "__main__":
    if seed_database():
        print("\n✅ Seeding SUCCESS")
    else:
        print("\n❌ Seeding FAILED")
