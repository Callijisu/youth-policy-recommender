// src/components/domain/profile/StepResult.jsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // 👈 1. 라우터 이동 훅 임포트
import useProfileStore from '../../../hooks/useProfileStore';
import { useAgentVerify } from '../../../hooks/useAgentVerify';
import Button from '../../common/Button';

const StepResult = () => {
  const { userProfile } = useProfileStore();
  
  // React Query 훅 사용
  const { mutate, isPending, isError, isSuccess, data, error } = useAgentVerify();
  
  // 👈 2. 네비게이트 함수 생성
  const navigate = useNavigate();

  // 컴포넌트 마운트 시 검증 요청
  useEffect(() => {
    if (!isSuccess && !isError) {
      mutate(userProfile);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 1. 로딩 화면
  if (isPending) {
    return (
      <div className="flex flex-col items-center justify-center h-full animate-fadeIn py-10">
        <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-6"></div>
        <h2 className="text-xl font-bold text-gray-800 mb-2">맞춤 정책을 찾고 있습니다...</h2>
        <p className="text-gray-500 text-center">
          {userProfile.region} 거주, {userProfile.status} 관련<br/>
          혜택을 분석 중입니다. 🔍
        </p>
      </div>
    );
  }

  // 2. 에러 화면
  if (isError) {
    return (
      <div className="flex flex-col h-full animate-fadeIn items-center text-center pt-8">
        <div className="text-5xl mb-4">😵</div>
        <h2 className="text-xl font-bold text-red-500 mb-2">분석에 실패했어요</h2>
        <p className="text-gray-500 mb-8 text-sm">
          {error?.message || '잠시 후 다시 시도해주세요.'}
        </p>
        <Button onClick={() => mutate(userProfile)}>다시 시도</Button>
      </div>
    );
  }

  // 3. 성공 화면 (리스트 출력)
  if (isSuccess && data) {
    return (
      <div className="flex flex-col h-full animate-fadeIn">
        <div className="text-center mb-6">
          <div className="text-4xl mb-2">🎉</div>
          <h2 className="text-2xl font-bold text-gray-800">
            {userProfile.age}년생 {userProfile.region} 청년을 위한<br/>
            <span className="text-blue-600">맞춤 정책 {data.data.length}건</span>을 찾았어요!
          </h2>
        </div>

        {/* 정책 리스트 카드 영역 */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-3 px-1">
          {data.data.map((policy) => (
            <div 
              key={policy.id}
              // 👈 3. 카드 클릭 시 상세 페이지로 이동하는 이벤트 추가
              onClick={() => navigate(`/policy/${policy.id}`)}
              className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-blue-300 transition-all cursor-pointer"
            >
              <div className="flex justify-between items-start mb-2">
                <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded font-bold">
                  추천
                </span>
                <span className="text-gray-400 text-xs">D-Day 계산중</span>
              </div>
              <h3 className="text-lg font-bold text-gray-800 mb-1">{policy.title}</h3>
              <p className="text-blue-600 font-bold text-lg">{policy.amount}</p>
            </div>
          ))}
        </div>

        {/* 하단 버튼 (추가 기능 예시) */}
        <div className="mt-auto">
          <Button onClick={() => alert('나중에 "전체 리스트 저장하기" 기능을 붙여보세요!')}>
            결과 리스트 저장하기 📥
          </Button>
        </div>
      </div>
    );
  }

  return null;
};

export default StepResult;