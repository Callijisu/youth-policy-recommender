import sys
import os
import pandas as pd
import uuid
import re
from datetime import datetime
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())
load_dotenv()

from database.mongo_handler import get_mongodb_handler

def parse_date(date_str):
    """날짜 문자열을 파싱하여 표준 형식으로 변환"""
    if pd.isna(date_str) or not date_str:
        return None

    date_str = str(date_str).strip()

    # 다양한 날짜 형식 처리
    if '~' in date_str:
        # 범위가 있는 경우 종료일만 사용
        date_str = date_str.split('~')[-1].strip()

    # YYYYMMDD 형식 처리
    if len(date_str) == 8 and date_str.isdigit():
        try:
            return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        except:
            return None

    # 기타 형식은 상시로 처리
    return "상시"

def extract_age_from_conditions(conditions_text):
    """조건 텍스트에서 나이 정보 추출"""
    if pd.isna(conditions_text):
        return None, None

    text = str(conditions_text)

    # 나이 관련 패턴 찾기
    age_patterns = [
        r'(\d+)세?\s*~\s*(\d+)세',
        r'(\d+)세?\s*이상\s*(\d+)세?\s*이하',
        r'만\s*(\d+)세?\s*~\s*만?\s*(\d+)세',
    ]

    for pattern in age_patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1)), int(match.group(2))

    # 단일 나이 패턴
    single_age_patterns = [
        r'(\d+)세?\s*이하',
        r'(\d+)세?\s*미만'
    ]

    for pattern in single_age_patterns:
        match = re.search(pattern, text)
        if match:
            return 18, int(match.group(1))  # 기본 최소 나이 18세

    return None, None

def extract_region_from_name(policy_name, org_name):
    """정책명과 기관명에서 지역 추출"""
    # 광역시/도
    major_regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종',
                    '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']

    # 시/군/구 (더 많은 지역 추가)
    minor_regions = [
        # 경기도
        '수원', '성남', '용인', '안양', '안산', '고양', '과천', '구리', '남양주', '오산',
        '시흥', '군포', '의왕', '하남', '양주', '동두천', '의정부', '파주', '이천',
        '안성', '김포', '화성', '광주시', '여주', '연천', '가평', '양평',
        # 전라북도
        '전주', '군산', '익산', '정읍', '남원', '김제', '완주', '진안', '무주', '장수',
        '임실', '순창', '고창', '부안',
        # 전라남도
        '목포', '여수', '순천', '나주', '광양', '담양', '곡성', '구례', '고흥', '보성',
        '화순', '장흥', '강진', '해남', '영암', '무안', '함평', '영광', '장성', '완도', '진도',
        # 경상남도
        '창원', '진주', '통영', '사천', '김해', '밀양', '거제', '양산', '의령', '함안',
        '창녕', '고성', '남해', '하동', '산청', '함양', '거창', '합천',
        # 경상북도
        '포항', '경주', '김천', '안동', '구미', '영주', '영천', '상주', '문경', '경산',
        # 충청남도
        '천안', '공주', '보령', '아산', '서산', '논산', '계룡', '당진', '금산', '부여',
        '서천', '청양', '홍성', '예산', '태안',
        # 충청북도
        '청주', '충주', '제천', '보은', '옥천', '영동', '증평', '진천', '괴산', '음성', '단양',
        # 강원도
        '춘천', '원주', '강릉', '동해', '태백', '속초', '삼척', '홍천', '횡성', '영월',
        '평창', '정선', '철원', '화천', '양구', '인제', '고성', '양양',
        # 제주도
        '제주시', '서귀포'
    ]

    text = f"{policy_name} {org_name}".lower()

    # 시/군/구 먼저 확인 (더 구체적이므로)
    for region in minor_regions:
        if region.lower() in text:
            # 시/군/구를 광역시/도로 매핑
            region_map = {
                # 경기도
                '수원': '경기', '성남': '경기', '용인': '경기', '안양': '경기',
                '안산': '경기', '고양': '경기', '과천': '경기', '구리': '경기',
                '남양주': '경기', '오산': '경기', '시흥': '경기', '군포': '경기',
                '의왕': '경기', '하남': '경기', '양주': '경기', '동두천': '경기',
                '의정부': '경기', '파주': '경기', '이천': '경기', '안성': '경기',
                '김포': '경기', '화성': '경기', '여주': '경기', '연천': '경기',
                '가평': '경기', '양평': '경기',
                # 전라북도
                '전주': '전북', '군산': '전북', '익산': '전북', '정읍': '전북',
                '남원': '전북', '김제': '전북', '완주': '전북', '진안': '전북',
                '무주': '전북', '장수': '전북', '임실': '전북', '순창': '전북',
                '고창': '전북', '부안': '전북',
                # 전라남도
                '목포': '전남', '여수': '전남', '순천': '전남', '나주': '전남',
                '광양': '전남', '담양': '전남', '곡성': '전남', '구례': '전남',
                # 경상남도
                '창원': '경남', '진주': '경남', '통영': '경남', '사천': '경남',
                '김해': '경남', '밀양': '경남', '거제': '경남', '양산': '경남',
                # 기타 지역들...
            }
            mapped_region = region_map.get(region, region)
            return [mapped_region]

    # 광역시/도 확인
    for region in major_regions:
        if region.lower() in text:
            return [region]

    return ['전국']

def categorize_policy(major_cat, minor_cat, policy_name):
    """정책을 우리 시스템 카테고리로 분류"""
    text = f"{major_cat} {minor_cat} {policy_name}".lower()

    # 카테고리 매핑
    if any(word in text for word in ['일자리', '취업', '고용', '구직', '채용', '직업', '인턴', '직장']):
        return '일자리'
    elif any(word in text for word in ['주거', '주택', '전세', '월세', '임대', '거주']):
        return '주거'
    elif any(word in text for word in ['창업', '사업', '기업', '스타트업', '벤처']):
        return '창업'
    elif any(word in text for word in ['금융', '대출', '적금', '보험', '투자', '자금']):
        return '금융'
    elif any(word in text for word in ['교육', '학습', '연수', '강의', '훈련', '학교']):
        return '교육'
    elif any(word in text for word in ['복지', '지원', '보조', '건강', '의료', '상담']):
        return '복지'
    elif any(word in text for word in ['문화', '예술', '체험', '여행', '관광']):
        return '문화'
    else:
        return '복지'  # 기본 카테고리

def extract_employment_target(conditions_text, policy_name):
    """고용 대상 추출"""
    if pd.isna(conditions_text):
        conditions_text = ""

    text = f"{conditions_text} {policy_name}".lower()

    targets = []
    if any(word in text for word in ['구직', '미취업', '무직', '실업']):
        targets.append('구직자')
    if any(word in text for word in ['재직', '근로', '직장', '회사원']):
        targets.append('재직자')
    if any(word in text for word in ['학생', '대학생', '재학']):
        targets.append('학생')
    if any(word in text for word in ['자영업', '사업자', '프리랜서']):
        targets.append('자영업')

    # 아무것도 없으면 모든 대상
    if not targets:
        targets = ['구직자', '재직자', '학생', '자영업']

    return targets

def extract_income_limit(conditions_text, benefit_text):
    """소득 제한 추출 (만원 단위)"""
    if pd.isna(conditions_text):
        conditions_text = ""
    if pd.isna(benefit_text):
        benefit_text = ""

    text = f"{conditions_text} {benefit_text}".lower()

    # 소득 제한 패턴 찾기
    income_patterns = [
        r'소득\s*(\d+)만원\s*이하',
        r'연소득\s*(\d+)만원\s*이하',
        r'중위소득\s*(\d+)%\s*이하',
        r'(\d+)만원\s*이하'
    ]

    for pattern in income_patterns:
        match = re.search(pattern, text)
        if match:
            amount = int(match.group(1))
            if '중위소득' in match.group(0):
                # 중위소득 기준을 대략적인 금액으로 변환
                return amount * 50  # 중위소득 100% = 약 5000만원 기준
            return amount

    return None  # 소득 제한 없음

def load_real_policies():
    """실제 정책 데이터를 CSV에서 로드하여 데이터베이스에 저장"""
    print("🌱 실제 정책 데이터(CSV)를 데이터베이스에 로드 시작...")

    # MongoDB 연결
    handler = get_mongodb_handler()
    if not handler or not handler.is_connected:
        print("❌ Database not connected")
        return False

    # CSV 로드
    try:
        df = pd.read_csv('data/policies_raw.csv')
        print(f"📄 CSV에서 {len(df)}개 정책 데이터 로드")
    except Exception as e:
        print(f"❌ CSV 로드 실패: {e}")
        return False

    # 기존 정책 삭제
    policies_collection = handler.database["policies"]
    policies_collection.delete_many({})
    print("🗑️ 기존 정책 데이터 삭제 완료")

    # 정책 변환 및 저장
    converted_policies = []
    success_count = 0

    for idx, row in df.iterrows():
        try:
            # 기본 정보
            policy_name = str(row['plcyNm']).strip()
            if not policy_name or policy_name == 'nan':
                continue

            policy_desc = str(row.get('plcyExplnCn', '')).strip()
            major_cat = str(row.get('mclsfNm', '')).strip()
            minor_cat = str(row.get('lclsfNm', '')).strip()
            conditions = str(row.get('addAplyQlfcCndCn', '')).strip()
            org_name = str(row.get('operInstCdNm', '')).strip()

            # 나이 조건 추출
            csv_min_age = row.get('sprtTrgtMinAge', 0)
            csv_max_age = row.get('sprtTrgtMaxAge', 0)

            # CSV의 나이가 0이면 조건 텍스트에서 추출 시도
            if csv_min_age == 0 or csv_max_age == 0:
                extracted_min, extracted_max = extract_age_from_conditions(conditions)
                target_age_min = extracted_min if extracted_min else (csv_min_age if csv_min_age > 0 else 18)
                target_age_max = extracted_max if extracted_max else (csv_max_age if csv_max_age > 0 else 39)
            else:
                target_age_min = int(csv_min_age)
                target_age_max = int(csv_max_age)

            # 39세 초과는 39세로 제한 (청년 정책)
            if target_age_max > 39:
                target_age_max = 39
            if target_age_min < 18:
                target_age_min = 18

            # 마감일 처리
            end_date = parse_date(row.get('bizPrdEndYmd'))
            if not end_date:
                end_date = "상시"

            # 정책 데이터 생성
            policy_data = {
                "policy_id": f"REAL_{idx+1:04d}",
                "title": policy_name,
                "category": categorize_policy(major_cat, minor_cat, policy_name),
                "target_age_min": target_age_min,
                "target_age_max": target_age_max,
                "target_regions": extract_region_from_name(policy_name, org_name),
                "target_employment": extract_employment_target(conditions, policy_name),
                "target_income_max": extract_income_limit(conditions, policy_desc),
                "benefit": policy_desc[:200] + "..." if len(policy_desc) > 200 else policy_desc,
                "budget_max": None,  # CSV에서 추출하기 어려움
                "deadline": end_date,
                "application_url": str(row.get('aplyUrlAddr', '')).strip() or None,
                "agency": org_name or "미상",
                "is_active": True,
                "requirements": [conditions[:100]] if conditions and conditions != 'nan' else [],
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }

            converted_policies.append(policy_data)
            success_count += 1

            # 진행 상황 출력 (100개마다)
            if success_count % 100 == 0:
                print(f"   처리됨: {success_count}개...")

        except Exception as e:
            print(f"⚠️ 정책 {idx+1} 처리 실패: {e}")
            continue

    # 데이터베이스에 일괄 저장
    if converted_policies:
        try:
            result = policies_collection.insert_many(converted_policies)
            print(f"✅ {len(result.inserted_ids)}개 정책 데이터베이스 저장 완료")

            # 카테고리별 통계
            categories = {}
            for policy in converted_policies:
                cat = policy['category']
                categories[cat] = categories.get(cat, 0) + 1

            print("📊 카테고리별 정책 수:")
            for cat, count in sorted(categories.items()):
                print(f"   - {cat}: {count}개")

            return True

        except Exception as e:
            print(f"❌ 데이터베이스 저장 실패: {e}")
            return False
    else:
        print("❌ 변환된 정책이 없습니다")
        return False

if __name__ == "__main__":
    success = load_real_policies()
    if success:
        print("\n🎉 실제 정책 데이터 로드 성공!")
    else:
        print("\n❌ 정책 데이터 로드 실패")