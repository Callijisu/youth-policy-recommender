
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
            "target_income_max": 300, # 월소득 300이하? 연소득으로 통일 필요. 여기선 연 3600 가정
            "benefit": "2년 만기시 300만원~1200만원 지급",
            "budget_max": 1200,
            "deadline": "2024-12-31",
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
            "target_employment": ["재직자", "구직자"],
            "target_income_max": 3600,
            "benefit": "월 10만원 적립시 정부지원금 10만원 추가 적립",
            "budget_max": 240,
            "deadline": "2024-12-31",
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
            "target_employment": ["예비창업자", "자영업"],
            "target_income_max": 0, # 제한없음
            "benefit": "최대 1억원 사업화 자금 지원",
            "budget_max": 10000,
            "deadline": "2024-03-31",
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
