"""Clear all policies and re-import fresh"""
import sys
sys.path.append('.')
from database.mongo_handler import get_mongodb_handler

def clear_policies():
    handler = get_mongodb_handler()
    db = handler.client['youth_policy']
    policies = db['policies']
    
    # 전체 삭제
    result = policies.delete_many({})
    print(f"✅ 삭제된 정책 수: {result.deleted_count}")
    
    # 확인
    remaining = policies.count_documents({})
    print(f"남은 정책 수: {remaining}")

if __name__ == "__main__":
    clear_policies()
