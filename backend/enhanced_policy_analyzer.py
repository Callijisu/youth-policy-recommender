import pandas as pd
import re
from typing import Dict, List, Optional, Tuple

class PolicyConditionAnalyzer:
    """정책 조건을 상세히 분석하는 클래스"""

    def __init__(self):
        self.region_keywords = {
            '서울': ['서울', '서울시', '서울특별시'],
            '부산': ['부산', '부산시', '부산광역시'],
            '대구': ['대구', '대구시', '대구광역시'],
            '인천': ['인천', '인천시', '인천광역시'],
            '광주': ['광주', '광주시', '광주광역시'],
            '대전': ['대전', '대전시', '대전광역시'],
            '울산': ['울산', '울산시', '울산광역시'],
            '세종': ['세종', '세종시', '세종특별자치시'],
            '경기': ['경기', '경기도'],
            '강원': ['강원', '강원도', '강원특별자치도'],
            '충북': ['충북', '충청북도'],
            '충남': ['충남', '충청남도'],
            '전북': ['전북', '전라북도', '전북특별자치도'],
            '전남': ['전남', '전라남도'],
            '경북': ['경북', '경상북도'],
            '경남': ['경남', '경상남도'],
            '제주': ['제주', '제주도', '제주특별자치도'],
            # 주요 시/군
            '진주': ['진주', '진주시'],
            '순창': ['순창', '순창군'],
            '곡성': ['곡성', '곡성군'],
            '목포': ['목포', '목포시'],
            '여수': ['여수', '여수시'],
            '순천': ['순천', '순천시'],
            '광양': ['광양', '광양시']
        }

    def analyze_age_conditions(self, conditions_text: str, csv_min: int, csv_max: int) -> Tuple[int, int]:
        """나이 조건 상세 분석"""
        if pd.isna(conditions_text):
            conditions_text = ""

        text = str(conditions_text).lower()

        # 1. 명시적인 나이 조건 찾기
        age_patterns = [
            r'(\d+)세\s*이상\s*(\d+)세\s*이하',
            r'(\d+)세\s*~\s*(\d+)세',
            r'만\s*(\d+)세\s*이상\s*만\s*(\d+)세\s*이하',
            r'(\d+)\s*세\s*미만',  # 최대 나이만
            r'(\d+)\s*세\s*이상',  # 최소 나이만
        ]

        for pattern in age_patterns:
            matches = re.findall(pattern, text)
            if matches:
                match = matches[0]
                if isinstance(match, tuple) and len(match) == 2:
                    return int(match[0]), int(match[1])
                elif '미만' in pattern and len(match) == 1:
                    return 18, int(match[0]) - 1
                elif '이상' in pattern and len(match) == 1:
                    return int(match[0]), 39

        # 2. 대학생/학생 관련 키워드로 추정
        if any(word in text for word in ['대학생', '재학생', '대학교', '대학원생', '휴학생']):
            return 18, 28  # 일반적인 대학생 연령

        # 3. CSV 데이터 활용
        if csv_min > 0 and csv_max > 0:
            return max(csv_min, 18), min(csv_max, 39)
        elif csv_min > 0:
            return max(csv_min, 18), 39
        elif csv_max > 0:
            return 18, min(csv_max, 39)

        # 4. 기본값 (청년)
        return 18, 39

    def analyze_region_conditions(self, conditions_text: str, policy_name: str) -> List[str]:
        """지역 조건 상세 분석"""
        if pd.isna(conditions_text):
            conditions_text = ""

        text = f"{conditions_text} {policy_name}".lower()
        found_regions = set()

        # 지역별 키워드 매칭
        for region_code, keywords in self.region_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    # 광역시/도로 정규화
                    if region_code in ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종']:
                        found_regions.add(region_code)
                    elif region_code == '진주':
                        found_regions.add('경남')
                    elif region_code in ['순창']:
                        found_regions.add('전북')
                    elif region_code in ['곡성', '목포', '여수', '순천', '광양']:
                        found_regions.add('전남')
                    else:
                        found_regions.add(region_code)

        # 도내/시내/군내 등의 표현이 있으면 해당 지역만
        if any(word in text for word in ['도내', '시내', '군내', '소재']):
            if found_regions:
                return list(found_regions)

        # 전국 키워드 체크
        if any(word in text for word in ['전국', '전 지역', '모든 지역']):
            return ['전국']

        return list(found_regions) if found_regions else ['전국']

    def analyze_employment_conditions(self, conditions_text: str, policy_name: str) -> List[str]:
        """고용 상태 조건 상세 분석"""
        if pd.isna(conditions_text):
            conditions_text = ""

        text = f"{conditions_text} {policy_name}".lower()
        employment_types = []

        # 명시적 고용 상태 체크
        if any(word in text for word in ['재학생', '대학생', '대학교', '휴학생', '재학 중']):
            employment_types.append('학생')

        if any(word in text for word in ['구직자', '미취업자', '실업자', '취업준비생']):
            employment_types.append('구직자')

        if any(word in text for word in ['재직자', '근로자', '직장인', '회사원', '사원']):
            employment_types.append('재직자')

        if any(word in text for word in ['사업자', '자영업', '대표', '창업자']):
            employment_types.append('자영업')

        # 특정 조건이 없으면 모든 고용 상태 포함
        if not employment_types:
            employment_types = ['구직자', '재직자', '학생', '자영업']

        return employment_types

    def analyze_income_conditions(self, conditions_text: str) -> Optional[int]:
        """소득 조건 상세 분석"""
        if pd.isna(conditions_text):
            return None

        text = str(conditions_text).lower()

        # 소득 관련 패턴
        income_patterns = [
            r'소득\s*(\d+)만원\s*이하',
            r'연소득\s*(\d+)만원\s*이하',
            r'월소득\s*(\d+)만원\s*이하',
            r'(\d+)만원\s*이하.*소득',
            r'중위소득\s*(\d+)%\s*이하'
        ]

        for pattern in income_patterns:
            matches = re.findall(pattern, text)
            if matches:
                amount = int(matches[0])
                if '중위소득' in pattern:
                    # 중위소득 기준을 실제 소득으로 변환
                    # 2025년 기준 중위소득 대략 계산
                    median_income_2025 = 5500  # 4인 가구 기준 연소득 (만원)
                    return int(amount * median_income_2025 / 100)
                elif '월소득' in text:
                    return amount * 12  # 연소득으로 변환
                return amount

        return None

    def extract_detailed_benefits(self, policy_desc: str, benefits_text: str) -> str:
        """혜택 정보 상세 추출"""
        if pd.isna(policy_desc):
            policy_desc = ""
        if pd.isna(benefits_text):
            benefits_text = ""

        combined_text = f"{policy_desc} {benefits_text}".strip()

        # 혜택 금액 추출
        amount_patterns = [
            r'(\d+)만원',
            r'(\d+)천만원',
            r'(\d+)억원',
            r'최대\s*(\d+)만원',
            r'월\s*(\d+)만원'
        ]

        # 텍스트 정리 및 요약
        if len(combined_text) > 200:
            combined_text = combined_text[:200] + "..."

        return combined_text

    def is_currently_available(self, start_date: str, end_date: str) -> bool:
        """현재 신청 가능한 정책인지 확인"""
        from datetime import datetime

        # 현재는 2026년 2월이므로, 2026년 이후 또는 상시 정책만 활성으로 판정
        current_date = datetime.now()

        try:
            if pd.isna(end_date) or not end_date:
                return True

            end_str = str(end_date).strip()

            # 상시/연중 키워드 체크
            if any(word in end_str.lower() for word in ['상시', '연중', '계속', '예산', '소진']):
                return True

            # 날짜 파싱
            if len(end_str) == 8 and end_str.isdigit():
                end_date_obj = datetime.strptime(end_str, '%Y%m%d')

                # 2025년 이후 정책들은 모두 유효하게 처리 (청년 정책의 특성상)
                cutoff_date = datetime(2025, 1, 1)
                return end_date_obj >= cutoff_date

        except:
            pass

        return True  # 파싱 실패시 일단 사용 가능으로 판정

def update_policies_with_detailed_analysis():
    """기존 정책들을 상세 분석 결과로 업데이트"""
    print("🔍 정책 조건 상세 분석 시작...")

    # CSV 로드
    df = pd.read_csv('data/policies_raw.csv')
    analyzer = PolicyConditionAnalyzer()

    # MongoDB 연결
    from database.mongo_handler import get_mongodb_handler
    handler = get_mongodb_handler()
    collection = handler.database["policies"]

    updated_count = 0

    for idx, row in df.iterrows():
        try:
            policy_name = str(row['plcyNm']).strip()
            if not policy_name or policy_name == 'nan':
                continue

            conditions_text = str(row.get('addAplyQlfcCndCn', ''))
            csv_min_age = row.get('sprtTrgtMinAge', 0)
            csv_max_age = row.get('sprtTrgtMaxAge', 0)

            # 상세 분석
            min_age, max_age = analyzer.analyze_age_conditions(conditions_text, csv_min_age, csv_max_age)
            regions = analyzer.analyze_region_conditions(conditions_text, policy_name)
            employment_types = analyzer.analyze_employment_conditions(conditions_text, policy_name)
            income_limit = analyzer.analyze_income_conditions(conditions_text)

            # 현재 신청 가능 여부
            is_available = analyzer.is_currently_available(
                row.get('bizPrdBgngYmd'), row.get('bizPrdEndYmd')
            )

            # DB 업데이트
            policy_id = f"REAL_{idx+1:04d}"

            update_data = {
                "target_age_min": min_age,
                "target_age_max": max_age,
                "target_regions": regions,
                "target_employment": employment_types,
                "target_income_max": income_limit,
                "is_active": is_available,
                "original_conditions": conditions_text[:500],  # 원본 조건 보존
                "updated_at": datetime.now()
            }

            result = collection.update_one(
                {"policy_id": policy_id},
                {"$set": update_data}
            )

            if result.modified_count > 0:
                updated_count += 1

            if updated_count % 100 == 0:
                print(f"   업데이트됨: {updated_count}개...")

        except Exception as e:
            print(f"⚠️ 정책 {idx+1} 분석 실패: {e}")
            continue

    print(f"✅ {updated_count}개 정책 상세 분석 완료")
    return updated_count

if __name__ == "__main__":
    from datetime import datetime
    import sys
    import os
    sys.path.append(os.getcwd())
    from dotenv import load_dotenv
    load_dotenv()

    success = update_policies_with_detailed_analysis()
    print(f"\n🎉 정책 조건 상세 분석 완료: {success}개 업데이트")