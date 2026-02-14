import React, { useState } from 'react';

const TestSurvey = () => {
  const [profile, setProfile] = useState({
    age: '',
    region: '',
    income: '',
    employment: '',
    interest: ''
  });

  const [results, setResults] = useState(null);

  const handleSubmit = async () => {
    try {
      const currentYear = new Date().getFullYear();
      const birthYear = parseInt(profile.age, 10);
      const realAge = currentYear - birthYear;

      const requestBody = {
        age: realAge,
        region: profile.region,
        income: parseInt(profile.income) || 0,
        employment: profile.employment,
        interest: profile.interest,
        min_score: 30.0,
        max_results: 10
      };

      const response = await fetch('http://localhost:8000/api/orchestrator', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('API 호출 실패:', error);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">청년 정책 추천 테스트</h1>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">태어난 연도</label>
          <input
            type="number"
            placeholder="예: 1995"
            value={profile.age}
            onChange={(e) => setProfile({...profile, age: e.target.value})}
            className="w-full p-2 border rounded"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">거주지</label>
          <select
            value={profile.region}
            onChange={(e) => setProfile({...profile, region: e.target.value})}
            className="w-full p-2 border rounded"
          >
            <option value="">선택하세요</option>
            <option value="서울">서울</option>
            <option value="부산">부산</option>
            <option value="대구">대구</option>
            <option value="인천">인천</option>
            <option value="경기">경기</option>
            <option value="대전">대전</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">연 소득 (만원)</label>
          <input
            type="number"
            placeholder="예: 3000"
            value={profile.income}
            onChange={(e) => setProfile({...profile, income: e.target.value})}
            className="w-full p-2 border rounded"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">현재 상황</label>
          <select
            value={profile.employment}
            onChange={(e) => setProfile({...profile, employment: e.target.value})}
            className="w-full p-2 border rounded"
          >
            <option value="">선택하세요</option>
            <option value="구직자">구직자</option>
            <option value="재직자">재직자</option>
            <option value="학생">학생</option>
            <option value="자영업">자영업</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">관심분야</label>
          <select
            value={profile.interest}
            onChange={(e) => setProfile({...profile, interest: e.target.value})}
            className="w-full p-2 border rounded"
          >
            <option value="">선택하세요</option>
            <option value="일자리">일자리</option>
            <option value="주거">주거</option>
            <option value="금융">금융</option>
            <option value="창업">창업</option>
            <option value="교육">교육</option>
          </select>
        </div>

        <button
          onClick={handleSubmit}
          className="w-full bg-blue-600 text-white p-3 rounded hover:bg-blue-700"
        >
          정책 추천 받기
        </button>
      </div>

      {results && (
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-4">추천 결과</h2>
          {results.recommendation_result?.recommendations?.map((policy, index) => (
            <div key={index} className="border p-4 mb-4 rounded">
              <h3 className="font-bold">{policy.policy_name}</h3>
              <p className="text-gray-600">점수: {policy.score}점</p>
              <p className="text-sm">{policy.benefit}</p>
              <p className="text-xs text-gray-500">{policy.explanation}</p>
            </div>
          )) || <p>추천 결과가 없습니다.</p>}
        </div>
      )}
    </div>
  );
};

export default TestSurvey;