
from database.mongo_handler import get_mongodb_handler
from dotenv import load_dotenv

load_dotenv()

def debug_db():
    mongo = get_mongodb_handler()
    if not mongo.is_connected:
        print("❌ MongoDB Not Connected")
        return

    db = mongo.database
    collection = db["policies"]
    
    # Check total count
    count = collection.count_documents({})
    print(f"📊 Total Policies: {count}")
    
    # Check for HOU_001
    hou_001 = collection.find_one({"policy_id": "HOU_001"})
    if hou_001:
        print("✅ Found HOU_001:")
        print(f"   Title: {hou_001.get('title')}")
    else:
        print("❌ HOU_001 NOT FOUND in DB")
        
    # List some actual IDs
    print("\n🔍 Sample IDs in DB:")
    cursor = collection.find({}, {"policy_id": 1, "title": 1}).limit(5)
    for doc in cursor:
        print(f"   [{doc.get('policy_id')}] {doc.get('title')}")

if __name__ == "__main__":
    debug_db()
