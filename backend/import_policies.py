
import csv
import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional
import re

# Add backend directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.mongo_handler import get_mongodb_handler
from dotenv import load_dotenv

load_dotenv()

def parse_age(age_str: str) -> Optional[int]:
    """Parse age string to integer."""
    if not age_str:
        return None
    try:
        return int(age_str)
    except ValueError:
        return None

def extract_age_from_text(text: str) -> tuple:
    """Extract min and max age from policy text."""
    if not text:
        return None, None
    
    min_age, max_age = None, None
    
    # 패턴: "19세 ~ 39세", "만 19~34세", "19-39세"
    patterns = [
        r'(?:만\s*)?([0-9]+)\s*[~\-]\s*([0-9]+)\s*세',
        r'([0-9]+)세\s*(?:이상|부터).*?([0-9]+)세\s*(?:이하|까지)',
        r'([0-9]+)\s*세\s*[~\-]\s*([0-9]+)\s*세',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            min_age = int(match.group(1))
            max_age = int(match.group(2))
            return min_age, max_age
    
    # 패턴: "39세 이하"
    match = re.search(r'([0-9]+)\s*세\s*이하', text)
    if match:
        max_age = int(match.group(1))
        min_age = 15  # 청년 기본 최소 나이
        return min_age, max_age
    
    # 패턴: "19세 이상"
    match = re.search(r'([0-9]+)\s*세\s*이상', text)
    if match:
        min_age = int(match.group(1))
        max_age = 39  # 청년 기본 최대 나이
        return min_age, max_age
    
    return None, None

def normalize_region(region_name: str) -> str:
    """Normalize region name to standard format."""
    if not region_name:
        return "전국"
    
    region_map = {
        "서울": "서울", "서울특별시": "서울",
        "경기": "경기", "경기도": "경기",
        "인천": "인천", "인천광역시": "인천",
        "부산": "부산", "부산광역시": "부산",
        "대구": "대구", "대구광역시": "대구",
        "광주": "광주", "광주광역시": "광주",
        "대전": "대전", "대전광역시": "대전",
        "울산": "울산", "울산광역시": "울산",
        "세종": "세종", "세종특별자치시": "세종",
        "강원": "강원", "강원도": "강원", "강원특별자치도": "강원",
        "충북": "충북", "충청북도": "충북",
        "충남": "충남", "충청남도": "충남",
        "전북": "전북", "전라북도": "전북", "전북특별자치도": "전북",
        "전남": "전남", "전라남도": "전남",
        "경북": "경북", "경상북도": "경북",
        "경남": "경남", "경상남도": "경남",
        "제주": "제주", "제주도": "제주", "제주특별자치도": "제주"
    }
    
    # Check if any key is in the region name
    for key, value in region_map.items():
        if key in region_name:
            return value
            
    # If no match but not empty, return as is or map specific cities
    # For now, if unknown, keep original or "기타"
    return region_name

def determine_employment_status(text: str) -> List[str]:
    """Determine target employment status from text."""
    statuses = []
    text = text.lower() if text else ""
    
    if "대학생" in text or "재학" in text or "휴학" in text:
        statuses.append("학생")
    if "미취업" in text or "구직" in text or "취업준비" in text:
        statuses.append("구직자")
    if "재직" in text or "직장인" in text or "근로자" in text or "중소기업" in text:
        statuses.append("재직자")
    if "창업" in text or "예비창업" in text or "사업자" in text:
        statuses.append("자영업자") # Or '창업가' if schema supports
        
    if not statuses:
        statuses = ["구직자", "재직자", "학생", "자영업자", "기타"] # Default to all if not specified
        
    return list(set(statuses))

def clean_html(raw_html: str) -> str:
    """Remove HTML tags, decode HTML entities, and clean whitespace."""
    if not raw_html:
        return ""
    import html
    # HTML 태그 제거
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # HTML 엔티티 디코딩 (&middot; -> ·, &amp; -> & 등)
    cleantext = html.unescape(cleantext)
    # 추가 정리: \n을 공백으로, 여러 공백을 하나로
    cleantext = re.sub(r'\s+', ' ', cleantext)
    return cleantext.strip()

def extract_income_from_text(text: str) -> Optional[int]:
    """Extract income amount from text (return in Man-won)."""
    if not text:
        return None
    try:
        # 1. Check for specific patterns like "중위소득 100%", "연소득 5천만원"
        # Since calculating exact amount from "100%" is hard without base, we focus on absolute numbers first.
        # Agent 3's logic:
        patterns = [
            r'(\d+,?\d*)\s*만원',           # "3000만원", "1,000만원"
            r'(\d+,?\d*)\s*억',             # "1억"
            r'최대\s*(\d+,?\d*)\s*만원',     # "최대 3000만원"
            r'월\s*(\d+,?\d*)\s*만원',       # "월 50만원" => multiply by 12? No, usually income limit is annual. 
                                            # If monthly income limit (e.g. 200 manwon), keep as 200? Agent 3 compares against user annual income. 
                                            # If text says "Monthly 200", annual is 2400.
            r'(\d+,?\d*)\s*천만원',          # "5천만원"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Remove commas
                amount_str = matches[0].replace(',', '')
                amount = int(amount_str)

                # Unit conversion to Man-won
                if '억' in text:
                    amount = amount * 10000 
                elif '천만원' in text:
                    amount = amount * 1000
                elif '월' in text and amount < 1000: 
                    # Heuristic: if amount is small (e.g. 300), assume monthly and convert to annual
                    amount = amount * 12
                
                return amount
        return None
    except:
        return None

def import_policies_from_csv(csv_file_path: str):
    """Import policies from CSV to MongoDB."""
    mongo = get_mongodb_handler()
    if not mongo.is_connected:
        print("❌ MongoDB connection failed.")
        return

    print(f"📂 Reading policies from {csv_file_path}...")
    
    policies_to_insert = []
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Title
                title = row.get('plcyNm', '').strip()
                if not title:
                    continue
                    
                # Description & Benefit
                benefit = clean_html(row.get('plcySprtCn', ''))
                description = clean_html(row.get('plcyExplnCn', '')) 
                if not description: description = benefit
                
                # Category
                raw_category = row.get('lclsfNm', '기타')
                category = raw_category 
                
                # Age - CSV 필드 우선, 없으면 텍스트에서 추출
                min_age = parse_age(row.get('sprtTrgtMinAge'))
                max_age = parse_age(row.get('sprtTrgtMaxAge'))
                
                # 나이 정보가 없으면 텍스트에서 추출
                if min_age is None or max_age is None:
                    all_text = f"{description} {row.get('addAplyQlfcCndCn', '')} {row.get('ptcpPrpTrgtCn', '')}"
                    text_min, text_max = extract_age_from_text(all_text)
                    if min_age is None:
                        min_age = text_min
                    if max_age is None:
                        max_age = text_max
                
                # Region - 상위 기관명(광역시/도) 우선 사용
                # rgtrHghrkInstCdNm: 서울특별시, 경기도 등 (광역시/도 레벨)
                # rgtrInstCdNm: 진주시, 연제구 등 (시/군/구 레벨)
                high_inst = row.get('rgtrHghrkInstCdNm', '')
                rgtr_inst = row.get('rgtrInstCdNm', '')
                oper_inst = row.get('operInstCdNm', '')
                raw_region = high_inst or rgtr_inst or oper_inst or "전국"
                region = normalize_region(raw_region)
                
                # Employment
                target_employment = determine_employment_status(
                    description + " " + row.get('sprtTrgtCn', '') + " " + title + " " + row.get('jobCd', '')
                )
                
                # Income
                # Try to get from text fields if earnMaxAmt is empty
                income_text = row.get('earnEtcCn', '') + " " + row.get('earnCndSeCd', '') + " " + row.get('addAplyQlfcCndCn', '')
                income_max = extract_income_from_text(income_text)
                
                # Deadlines
                deadline_raw = row.get('aplyYmd', '상시')
                
                # URLs
                app_url = row.get('aplyUrlAddr', '') or row.get('refUrlAddr1', '')
                
                # Agency
                agency = rgtr_inst or oper_inst or "정부/지자체"
                
                policy_doc = {
                    "policy_id": row.get('plcyNo', f"CSV_{datetime.now().timestamp()}"),
                    "title": title,
                    "description": description,
                    "category": category,
                    "target_age_min": min_age,
                    "target_age_max": max_age,
                    "target_regions": [region],
                    "target_employment": target_employment,
                    "target_income_max": income_max, 
                    "benefit": benefit,
                    "budget_max": None, 
                    "deadline": deadline_raw,
                    "application_url": app_url,
                    "agency": agency,
                    "is_active": True,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                
                policies_to_insert.append(policy_doc)
                
    except FileNotFoundError:
        print(f"❌ File not found: {csv_file_path}")
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    if not policies_to_insert:
        print("⚠️ No policies found in CSV.")
        return

    print(f"📝 Found {len(policies_to_insert)} policies. Inserting/Updating in MongoDB...")
    
    # Upsert policies
    count = 0
    collection = mongo.get_collection("policies")
    
    for policy in policies_to_insert:
        try:
            # Use policy_id as unique key
            collection.update_one(
                {"policy_id": policy["policy_id"]},
                {"$set": policy},
                upsert=True
            )
            count += 1
            if count % 100 == 0:
                print(f"   Processed {count} policies...")
        except Exception as e:
            print(f"⚠️ Error inserting policy {policy.get('title')}: {e}")
            
    print(f"✅ Successfully processed {count} policies from CSV.")

if __name__ == "__main__":
    csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "policies_raw.csv")
    import_policies_from_csv(csv_file_path)
