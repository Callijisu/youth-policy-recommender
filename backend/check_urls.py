# Check application URL status in database
import sys
sys.path.append('.')
from database.mongo_handler import get_mongodb_handler

handler = get_mongodb_handler()
db = handler.client['youth_policy']

# 전체 정책 수
total = db['policies'].count_documents({})

# application_url이 있는 정책
with_url = db['policies'].count_documents({"application_url": {"$exists": True, "$ne": "", "$ne": None}})

# application_url이 없는 정책
without_url = total - with_url

print(f"=== 정책 신청 URL 현황 ===")
print(f"전체 정책: {total}개")
print(f"신청 URL 있음: {with_url}개 ({with_url/total*100:.1f}%)")
print(f"신청 URL 없음: {without_url}개 ({without_url/total*100:.1f}%)")

# 샘플로 몇 개 확인
print("\n=== URL 있는 정책 샘플 ===")
for p in db['policies'].find({"application_url": {"$exists": True, "$ne": "", "$ne": None}}).limit(3):
    print(f"- {p.get('title', 'N/A')[:30]}")
    print(f"  URL: {p.get('application_url', 'N/A')[:60]}")

print("\n=== URL 없는 정책 샘플 ===")
for p in db['policies'].find({"$or": [{"application_url": {"$exists": False}}, {"application_url": ""}, {"application_url": None}]}).limit(3):
    print(f"- {p.get('title', 'N/A')[:30]}")
    print(f"  policy_id: {p.get('policy_id', 'N/A')}")
