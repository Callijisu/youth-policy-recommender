import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useProfileStore from '../../../hooks/useProfileStore';
import { useAgentVerify } from '../../../hooks/useAgentVerify';
import Button from '../../common/Button';

const StepResult = () => {
  const { userProfile } = useProfileStore();
  const [searchTerm, setSearchTerm] = useState("");

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
          {userProfile.region} 거주, {userProfile.status} 관련<br />
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
    const filteredPolicies = data.data.filter(policy =>
      policy.title.includes(searchTerm) ||
      policy.tags?.some(tag => tag.includes(searchTerm))
    );

    return (
      <div className="flex flex-col h-full animate-fadeIn">
        <div className="text-center mb-4">
          <div className="text-4xl mb-2">🎉</div>
          <h2 className="text-2xl font-bold text-gray-800">
            {userProfile.age}년생 {userProfile.region} 청년을 위한<br />
            <span className="text-blue-600">맞춤 정책 {data.data.length}건</span>을 찾았어요!
          </h2>
        </div>

        {/* 검색창 */}
        <div className="mb-4 px-1">
          <input
            type="text"
            placeholder="정책 이름 검색..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all"
          />
        </div>

        {/* 정책 리스트 카드 영역 */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-2 px-1">
          {filteredPolicies.length > 0 ? (
            filteredPolicies.map((policy) => (
              <div
                key={policy.id}
                onClick={() => navigate(`/policy/${policy.id}`, { state: { policy } })}
                className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm hover:shadow-md hover:border-blue-300 transition-all cursor-pointer"
              >
                <div className="flex justify-between items-center">
                  <div className="flex-1 min-w-0">
                    <div className="flex gap-1 flex-wrap mb-1">
                      {policy.tags && policy.tags.slice(0, 2).map((tag, idx) => (
                        <span key={idx} className="bg-blue-50 text-blue-600 text-xs px-2 py-0.5 rounded font-medium">
                          #{tag}
                        </span>
                      ))}
                    </div>
                    <h3 className="text-sm font-bold text-gray-800 truncate">{policy.title}</h3>
                  </div>
                  <span className={`text-xs font-bold px-2 py-1 rounded ml-2 whitespace-nowrap flex-shrink-0 ${policy.deadline === '상시 모집' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                    {policy.deadline?.slice(0, 10) || '상시'}
                  </span>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-10 text-gray-400">
              검색 결과가 없습니다.
            </div>
          )}
        </div>

        {/* 하단 버튼 */}
        <div className="mt-auto flex flex-col gap-2">
          <Button onClick={() => {
            const existing = JSON.parse(localStorage.getItem('savedPolicies')) || [];
            const newPolicies = data.data.filter(p => !existing.some(e => e.id === p.id));
            const updated = [...newPolicies, ...existing];
            localStorage.setItem('savedPolicies', JSON.stringify(updated));

            alert(`${newPolicies.length}건이 보관함에 저장되었습니다!`);
            navigate('/saved');
          }}>
            이 결과 저장하기 📥
          </Button>

          <div className="flex gap-2">
            <button
              onClick={() => {
                useProfileStore.getState().resetStep();
                navigate('/');
              }}
              className="flex-1 py-3 text-gray-500 bg-gray-100 rounded-xl hover:bg-gray-200 font-bold transition-colors"
            >
              처음으로 🔄
            </button>
            <button
              onClick={() => navigate('/saved')}
              className="flex-1 py-3 text-blue-600 bg-blue-50 rounded-xl hover:bg-blue-100 font-bold transition-colors"
            >
              보관함 가기 📂
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default StepResult;