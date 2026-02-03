
import { useMutation } from '@tanstack/react-query';
import api from '../services/api';

// API 호출 함수
const verifyProfileApi = async (profileData) => {
  // 1. 데이터 변환 (Frontend -> Backend)
  const currentYear = new Date().getFullYear();
  const birthYear = parseInt(profileData.age, 10);
  const realAge = currentYear - birthYear;

  // 소득 정보가 없으면 0으로 처리 (혹은 UI에 추가 필요)
  const incomeVal = profileData.income ? parseInt(profileData.income, 10) : 0;

  // Frontend Status -> Backend Enum Mapping
  const employmentMap = {
    '재학': '학생',
    '미취업': '구직자',
    '재직': '재직자',
    '창업': '자영업',
    '단기근로': '구직자' // 단기근로자는 보통 구직 지원 대상에 포함됨
  };

  const requestBody = {
    age: realAge,
    region: profileData.region,
    income: incomeVal,
    employment: employmentMap[profileData.status] || "구직자", // 매핑되지 않은 값은 기본값 '구직자'
    interest: null, // 관심사는 선택사항 (Backend accepts null)
    min_score: 40.0,
    max_results: 20
  };

  console.log("🚀 [API 요청] 매칭 시작:", requestBody);

  try {
    // 2. 실제 API 호출 (Orchestrator: AI 기반 통합 추천)
    const response = await api.post('/api/orchestrator', requestBody);
    console.log("✅ [API 응답] 성공:", response.data);

    // 3. 응답 데이터 변환 (Backend -> Frontend)
    // OrchestratorResponse -> recommendation_result -> recommendations (PolicyCard list)
    const rawRecommendations = response.data.recommendation_result?.recommendations || [];

    const recommendations = rawRecommendations.map(item => ({
      id: item.policy_id,
      title: item.policy_name,
      amount: item.benefit,
      score: item.score,
      explanation: item.explanation,
      match_reasons: item.match_reasons || [], // 매칭 이유 (나이조건 부합, 지역 적합 등)
      tags: item.tags || [],
      deadline: item.deadline_status === 'ongoing' ? '상시 모집' : item.deadline
    }));

    return {
      status: "success",
      message: response.data.message,
      data: recommendations
    };

  } catch (error) {
    console.error("❌ [API 오류] 매칭 실패:", error);
    throw error;
  }
};

export const useAgentVerify = () => {
  return useMutation({
    mutationFn: verifyProfileApi,
    onSuccess: (data) => {
      console.log('검증 성공:', data);
    },
    onError: (error) => {
      console.error('검증 실패:', error);
    },
  });
};