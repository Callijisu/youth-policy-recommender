"""Debug script to check policy data and matching"""
import sys
sys.path.append('.')
from database.mongo_handler import get_mongodb_handler

def debug_policies():
    handler = get_mongodb_handler()
    db = handler.client['youth_policy']
    policies = db['policies']
    
    # 1. 전체 정책 수
    total = policies.count_documents({})
    print(f"총 정책 수: {total}")
    
    # 2. 지역별 정책 수 (샘플)
    print("\n=== 지역별 정책 수 ===")
    regions_sample = policies.aggregate([
        {"$unwind": "$target_regions"},
        {"$group": {"_id": "$target_regions", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 15}
    ])
    for r in regions_sample:
        print(f"  {r['_id']}: {r['count']}개")
    
    # 3. 서울 관련 정책
    print("\n=== 서울 관련 정책 ===")
    seoul_policies = list(policies.find({
        "target_regions": {"$regex": "서울"}
    }).limit(5))
    print(f"서울 정책 수: {policies.count_documents({'target_regions': {'$regex': '서울'}})}")
    for p in seoul_policies:
        print(f"  - {p.get('title')[:30]}... | 지역: {p.get('target_regions')} | 나이: {p.get('target_age_min')}-{p.get('target_age_max')}")
    
    # 4. 전국 정책
    print("\n=== 전국 정책 ===")
    national_count = policies.count_documents({"target_regions": {"$regex": "전국"}})
    print(f"전국 정책 수: {national_count}")
    
    # 5. 26세에 해당하는 정책 (2000년생)
    print("\n=== 26세 해당 정책 (나이 조건) ===")
    age_match = policies.count_documents({
        "$or": [
            {"target_age_min": None, "target_age_max": None},
            {"target_age_min": {"$lte": 26}, "target_age_max": {"$gte": 26}},
            {"target_age_min": {"$lte": 26}, "target_age_max": None},
            {"target_age_min": None, "target_age_max": {"$gte": 26}},
        ]
    })
    print(f"26세 해당 정책 수: {age_match}")

if __name__ == "__main__":
    debug_policies()
