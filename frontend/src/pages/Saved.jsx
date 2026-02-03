import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/common/Button';

const Saved = () => {
    const navigate = useNavigate();
    const [savedPolicies, setSavedPolicies] = useState([]);

    useEffect(() => {
        // LocalStorage에서 저장된 정책 로드
        const loadSavedPolicies = () => {
            try {
                const saved = JSON.parse(localStorage.getItem('savedPolicies')) || [];
                setSavedPolicies(saved);
            } catch (e) {
                console.error("저장된 정책 로드 실패:", e);
                setSavedPolicies([]);
            }
        };
        loadSavedPolicies();
    }, []);

    const handleDelete = (id, e) => {
        e.stopPropagation(); // 카드 클릭 이벤트 전파 방지
        const updated = savedPolicies.filter(p => p.id !== id);
        setSavedPolicies(updated);
        localStorage.setItem('savedPolicies', JSON.stringify(updated));
    };

    return (
        <div className="flex flex-col h-full animate-fadeIn">
            {/* 헤더 with 뒤로가기 */}
            <div className="flex items-center mb-6 pt-4 px-1">
                <button
                    onClick={() => navigate(-1)}
                    className="text-2xl mr-3 hover:text-blue-600 transition"
                >
                    ←
                </button>
                <div className="flex-1 text-center">
                    <h2 className="text-2xl font-bold text-gray-800">
                        내 보관함 📂
                    </h2>
                    <p className="text-gray-500 text-sm mt-1">
                        저장한 정책 {savedPolicies.length}건이 있습니다.
                    </p>
                </div>
                <div className="w-8"></div> {/* 균형을 위한 빈 공간 */}
            </div>

            {savedPolicies.length === 0 ? (
                <div className="flex-1 flex flex-col items-center justify-center text-gray-400">
                    <div className="text-4xl mb-4">📭</div>
                    <p>저장된 정책이 없습니다.</p>
                    <button
                        onClick={() => navigate('/')}
                        className="mt-4 text-blue-500 font-bold hover:underline"
                    >
                        정책 찾으러 가기
                    </button>
                </div>
            ) : (
                <div className="flex-1 overflow-y-auto mb-4 space-y-3 px-1">
                    {savedPolicies.map((policy) => (
                        <div
                            key={policy.id}
                            onClick={() => navigate(`/policy/${policy.id}`, { state: { policy } })}
                            className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-blue-300 transition-all cursor-pointer relative"
                        >
                            <div className="flex justify-between items-start mb-2">
                                <div className="flex gap-1 flex-wrap">
                                    {policy.tags && policy.tags.map((tag, idx) => (
                                        <span key={idx} className="bg-blue-50 text-blue-600 text-xs px-2 py-1 rounded font-medium">
                                            #{tag}
                                        </span>
                                    ))}
                                </div>
                                <button
                                    onClick={(e) => handleDelete(policy.id, e)}
                                    className="text-gray-400 hover:text-red-500 text-sm font-bold px-2"
                                >
                                    삭제
                                </button>
                            </div>

                            <h3 className="text-lg font-bold text-gray-800 mb-1">{policy.title}</h3>
                            <p className="text-blue-600 font-bold text-sm mb-2">{policy.amount}</p>
                            <span className={`text-xs font-bold px-2 py-1 rounded ${policy.deadline === '상시 모집' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                                {policy.deadline || '일정 미정'}
                            </span>
                        </div>
                    ))}
                </div>
            )}

            <div className="mt-auto pt-4 border-t border-gray-100">
                <Button onClick={() => navigate('/')}>
                    새로운 정책 찾기 🔍
                </Button>
            </div>
        </div>
    );
};

export default Saved;
