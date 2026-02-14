import React, { useState } from 'react';
import { FaArrowLeft, FaCheck, FaUsers, FaClipboardList, FaChartBar } from 'react-icons/fa';

const QualitativeEvaluation = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [basicInfo, setBasicInfo] = useState({
    age: '',
    gender: '',
    policyInterest: ''
  });

  const [policyData] = useState({
    basic: {
      title: "서울시 청년수당",
      amount: "월 50만원",
      period: "6개월"
    },
    enhanced: {
      title: "서울시 청년수당",
      amount: "월 50만원",
      period: "6개월",
      personalizedExplanation: "취업 준비생인 당신에게 딱 맞는 정책입니다. 구직 활동을 하면서 생활비 부담을 덜어주는 월 50만원의 지원금을 받을 수 있습니다. 서울 거주 조건을 만족하며, 소득 수준도 해당되므로 신청 자격이 충분합니다.",
      benefits: [
        "월 50만원 × 6개월 = 총 300만원 지원",
        "구직활동 증명만으로 신청 가능",
        "별도 상환 의무 없음"
      ]
    }
  });

  const [evaluationScores, setEvaluationScores] = useState({
    understanding_basic: '',
    relevance_basic: '',
    conditions_basic: '',
    benefits_basic: '',
    application_basic: '',
    understanding_enhanced: '',
    relevance_enhanced: '',
    conditions_enhanced: '',
    benefits_enhanced: '',
    application_enhanced: '',
    personalization: '',
    interest_increase: '',
    application_intent: '',
    recommendation: '',
    preference: ''
  });

  const [feedback, setFeedback] = useState({
    helpful_aspects: '',
    improvement_needed: ''
  });

  const handleBasicInfoChange = (field, value) => {
    setBasicInfo(prev => ({ ...prev, [field]: value }));
  };

  const handleScoreChange = (field, value) => {
    setEvaluationScores(prev => ({ ...prev, [field]: value }));
  };

  const handleFeedbackChange = (field, value) => {
    setFeedback(prev => ({ ...prev, [field]: value }));
  };

  const submitEvaluation = async () => {
    const evaluationData = {
      basicInfo,
      evaluationScores,
      feedback,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent
    };

    try {
      const response = await fetch('http://localhost:8000/api/evaluation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(evaluationData),
      });

      if (response.ok) {
        alert('평가가 성공적으로 제출되었습니다. 참여해주셔서 감사합니다!');
        setCurrentStep(4);
      } else {
        alert('제출 중 오류가 발생했습니다. 다시 시도해주세요.');
      }
    } catch (error) {
      console.error('제출 오류:', error);
      alert('제출 중 오류가 발생했습니다. 다시 시도해주세요.');
    }
  };

  const ScaleInput = ({ field, label, category = '' }) => {
    const fullField = category ? `${field}_${category}` : field;
    return (
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">{label}</label>
        <div className="flex justify-between items-center">
          <span className="text-xs text-gray-500">전혀 아니다</span>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map(score => (
              <label key={score} className="flex items-center">
                <input
                  type="radio"
                  name={fullField}
                  value={score}
                  checked={evaluationScores[fullField] === score.toString()}
                  onChange={(e) => handleScoreChange(fullField, e.target.value)}
                  className="mr-1"
                />
                <span className="text-sm">{score}</span>
              </label>
            ))}
          </div>
          <span className="text-xs text-gray-500">매우 그렇다</span>
        </div>
      </div>
    );
  };

  const PolicyDisplay = ({ type, title }) => (
    <div className="bg-white rounded-lg border p-4 mb-6">
      <h3 className="text-lg font-bold mb-4 text-blue-600">{title}</h3>

      {type === 'basic' ? (
        <div className="space-y-2">
          <div className="font-medium">{policyData.basic.title}</div>
          <div className="text-gray-600">지원금액: {policyData.basic.amount}</div>
          <div className="text-gray-600">지원기간: {policyData.basic.period}</div>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="font-medium">{policyData.enhanced.title}</div>
          <div className="text-gray-600">지원금액: {policyData.enhanced.amount}</div>
          <div className="text-gray-600">지원기간: {policyData.enhanced.period}</div>

          <div className="bg-blue-50 p-3 rounded-lg">
            <h4 className="font-medium text-blue-800 mb-2">💡 맞춤형 설명</h4>
            <p className="text-sm text-blue-700">{policyData.enhanced.personalizedExplanation}</p>
          </div>

          <div className="bg-green-50 p-3 rounded-lg">
            <h4 className="font-medium text-green-800 mb-2">✅ 주요 혜택</h4>
            <ul className="text-sm text-green-700 space-y-1">
              {policyData.enhanced.benefits.map((benefit, index) => (
                <li key={index}>• {benefit}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );

  const renderStep = () => {
    switch (currentStep) {
      case 0:
        return (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <FaUsers className="text-4xl text-blue-600 mx-auto mb-4" />
              <h1 className="text-3xl font-bold text-gray-900 mb-4">정성적 평가 연구</h1>
              <p className="text-gray-600">GPT 기반 맞춤형 정책 설명의 품질을 평가해주세요</p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-sm border">
              <h2 className="text-xl font-bold mb-4">기본 정보</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">나이</label>
                  <input
                    type="number"
                    value={basicInfo.age}
                    onChange={(e) => handleBasicInfoChange('age', e.target.value)}
                    className="w-full p-3 border rounded-lg"
                    placeholder="예: 25"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">성별</label>
                  <select
                    value={basicInfo.gender}
                    onChange={(e) => handleBasicInfoChange('gender', e.target.value)}
                    className="w-full p-3 border rounded-lg"
                  >
                    <option value="">선택하세요</option>
                    <option value="male">남성</option>
                    <option value="female">여성</option>
                    <option value="other">기타</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    평소 청년 정책에 대한 관심도 (1-5점)
                  </label>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-500">전혀 관심없음</span>
                    <div className="flex gap-2">
                      {[1, 2, 3, 4, 5].map(score => (
                        <label key={score} className="flex items-center">
                          <input
                            type="radio"
                            name="policyInterest"
                            value={score}
                            checked={basicInfo.policyInterest === score.toString()}
                            onChange={(e) => handleBasicInfoChange('policyInterest', e.target.value)}
                            className="mr-1"
                          />
                          <span className="text-sm">{score}</span>
                        </label>
                      ))}
                    </div>
                    <span className="text-xs text-gray-500">매우 관심많음</span>
                  </div>
                </div>
              </div>

              <button
                onClick={() => setCurrentStep(1)}
                disabled={!basicInfo.age || !basicInfo.gender || !basicInfo.policyInterest}
                className="w-full mt-6 bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition"
              >
                다음 단계
              </button>
            </div>
          </div>
        );

      case 1:
        return (
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <FaClipboardList className="text-4xl text-blue-600 mx-auto mb-4" />
              <h2 className="text-2xl font-bold">A형 정책 설명 평가</h2>
              <p className="text-gray-600">기존 방식의 정책 설명을 확인하고 평가해주세요</p>
            </div>

            <PolicyDisplay type="basic" title="A형: 기본 정책 설명" />

            <div className="bg-white rounded-lg p-6 shadow-sm border">
              <h3 className="text-lg font-bold mb-4">A형에 대한 평가</h3>
              <div className="space-y-4">
                <ScaleInput field="understanding" category="basic" label="정책의 내용을 이해하기 쉬운가?" />
                <ScaleInput field="relevance" category="basic" label="나에게 왜 필요한지 납득이 가는가?" />
                <ScaleInput field="conditions" category="basic" label="정책 신청 조건이 명확하게 이해되는가?" />
                <ScaleInput field="benefits" category="basic" label="정책 혜택이 구체적으로 설명되어 있는가?" />
                <ScaleInput field="application" category="basic" label="정책 신청 방법이 명확한가?" />
              </div>

              <button
                onClick={() => setCurrentStep(2)}
                className="w-full mt-6 bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition"
              >
                다음: B형 평가하기
              </button>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <FaChartBar className="text-4xl text-green-600 mx-auto mb-4" />
              <h2 className="text-2xl font-bold">B형 정책 설명 평가</h2>
              <p className="text-gray-600">GPT 기반 맞춤형 설명을 확인하고 평가해주세요</p>
            </div>

            <PolicyDisplay type="enhanced" title="B형: GPT 기반 맞춤형 설명" />

            <div className="bg-white rounded-lg p-6 shadow-sm border">
              <h3 className="text-lg font-bold mb-4">B형에 대한 평가</h3>
              <div className="space-y-4">
                <ScaleInput field="understanding" category="enhanced" label="정책의 내용을 이해하기 쉬운가?" />
                <ScaleInput field="relevance" category="enhanced" label="나에게 왜 필요한지 납득이 가는가?" />
                <ScaleInput field="conditions" category="enhanced" label="정책 신청 조건이 명확하게 이해되는가?" />
                <ScaleInput field="benefits" category="enhanced" label="정책 혜택이 구체적으로 설명되어 있는가?" />
                <ScaleInput field="application" category="enhanced" label="정책 신청 방법이 명확한가?" />

                <div className="border-t pt-4 mt-6">
                  <h4 className="text-md font-bold mb-4">추가 평가 항목</h4>
                  <ScaleInput field="personalization" label="설명이 개인 상황에 맞춤화되어 있다고 느끼는가?" />
                  <ScaleInput field="interest_increase" label="정책에 대한 관심도가 높아졌는가?" />
                  <ScaleInput field="application_intent" label="실제로 신청해보고 싶다는 생각이 드는가?" />
                  <ScaleInput field="recommendation" label="다른 사람에게 추천하고 싶은가?" />
                </div>

                <div className="border-t pt-4 mt-6">
                  <label className="block text-sm font-medium mb-2">
                    어떤 방식의 설명을 선호하시나요?
                  </label>
                  <div className="space-y-2">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name="preference"
                        value="basic"
                        checked={evaluationScores.preference === 'basic'}
                        onChange={(e) => handleScoreChange('preference', e.target.value)}
                        className="mr-2"
                      />
                      <span>A형 (기본 정책 설명)</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name="preference"
                        value="enhanced"
                        checked={evaluationScores.preference === 'enhanced'}
                        onChange={(e) => handleScoreChange('preference', e.target.value)}
                        className="mr-2"
                      />
                      <span>B형 (GPT 기반 맞춤형 설명)</span>
                    </label>
                  </div>
                </div>
              </div>

              <button
                onClick={() => setCurrentStep(3)}
                className="w-full mt-6 bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition"
              >
                다음: 의견 작성하기
              </button>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold">자유 의견</h2>
              <p className="text-gray-600">사용 경험에 대한 솔직한 의견을 들려주세요</p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-sm border space-y-6">
              <div>
                <label className="block text-sm font-medium mb-2">
                  가장 도움이 되었던 부분은 무엇인가요?
                </label>
                <textarea
                  value={feedback.helpful_aspects}
                  onChange={(e) => handleFeedbackChange('helpful_aspects', e.target.value)}
                  className="w-full p-3 border rounded-lg h-24"
                  placeholder="예: 개인 상황에 맞는 설명이 이해하기 쉬웠습니다..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  개선이 필요한 부분은 무엇인가요?
                </label>
                <textarea
                  value={feedback.improvement_needed}
                  onChange={(e) => handleFeedbackChange('improvement_needed', e.target.value)}
                  className="w-full p-3 border rounded-lg h-24"
                  placeholder="예: 신청 방법을 더 자세히 설명해주면 좋겠습니다..."
                />
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setCurrentStep(2)}
                  className="flex-1 bg-gray-200 text-gray-700 p-3 rounded-lg hover:bg-gray-300 transition"
                >
                  이전
                </button>
                <button
                  onClick={submitEvaluation}
                  className="flex-1 bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition"
                >
                  평가 제출하기
                </button>
              </div>
            </div>
          </div>
        );

      case 4:
        return (
          <div className="max-w-2xl mx-auto text-center">
            <div className="bg-white rounded-lg p-8 shadow-sm border">
              <FaCheck className="text-4xl text-green-600 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-green-700 mb-4">평가 완료!</h2>
              <p className="text-gray-600 mb-6">
                소중한 의견을 주셔서 감사합니다.<br />
                연구에 큰 도움이 될 것입니다.
              </p>
              <button
                onClick={() => window.location.href = '/'}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
              >
                메인으로 돌아가기
              </button>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      {currentStep > 0 && currentStep < 4 && (
        <div className="max-w-4xl mx-auto mb-8">
          <div className="flex justify-between items-center mb-4">
            <button
              onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
              className="flex items-center text-gray-600 hover:text-blue-600 transition"
            >
              <FaArrowLeft className="mr-2" /> 이전
            </button>
            <span className="text-sm text-gray-500">
              단계 {currentStep + 1} / 4
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentStep + 1) / 4) * 100}%` }}
            ></div>
          </div>
        </div>
      )}

      {renderStep()}
    </div>
  );
};

export default QualitativeEvaluation;