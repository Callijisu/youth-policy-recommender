// src/pages/PolicyDetail.jsx
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import Button from '../components/common/Button';
import api from '../services/api';

const PolicyDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const statePolicy = location.state?.policy;

  const [policy, setPolicy] = useState(statePolicy || null);
  const [loading, setLoading] = useState(!statePolicy);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPolicyDetail = async () => {
      try {
        // 이미 state로 데이터가 넘어왔으면 로딩 생략 가능하지만, 최신 데이터 확인 차원에서 호출할 수도 있음
        // 여기서는 state가 있으면 일단 보여주고, API 호출은 백그라운드 업데이트 느낌으로 처리
        if (!statePolicy) setLoading(true);

        const response = await api.get(`/api/policy/${id}`);

        if (response.data.success) {
          setPolicy(prev => ({ ...prev, ...response.data.policy }));
        } else {
          if (!statePolicy) setError("정책 정보를 찾을 수 없습니다.");
        }
      } catch (err) {
        console.error("정책 상세 조회 실패:", err);
        if (!statePolicy) setError("서버와의 연결이 원활하지 않습니다.");
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchPolicyDetail();
    }
  }, [id, statePolicy]);

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"></div>
      <p className="text-gray-500">정보를 불러오는 중...</p>
    </div>
  );

  if (error && !policy) return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="text-4xl mb-4">😢</div>
      <p className="text-gray-500 mb-6">{error || "정책을 찾을 수 없습니다."}</p>
      <Button onClick={() => navigate(-1)}>뒤로 가기</Button>
    </div>
  );

  // HTML 엔티티 디코딩 함수 (&middot; -> · 등)
  const decodeHtml = (html) => {
    if (!html) return '';
    const txt = document.createElement('textarea');
    txt.innerHTML = html;
    return txt.value;
  };

  // 데이터 가공
  const formatMoney = (amount) => amount ? `${amount.toLocaleString()}만원` : '-';

  // 나이 표시 로직 개선
  const formatAge = () => {
    const min = policy.target_age_min;
    const max = policy.target_age_max;
    if (min && max) return `만 ${min}세 ~ ${max}세`;
    if (min) return `만 ${min}세 이상`;
    if (max) return `만 ${max}세 이하`;
    return "연령 제한 없음";
  };

  const displayData = {
    title: policy.title,
    badge: policy.category || "기타",
    summary: decodeHtml(policy.benefit || policy.description || "상세 혜택 정보가 없습니다."),

    // 구조화된 데이터 매핑
    age: formatAge(),
    employment: Array.isArray(policy.target_employment) && policy.target_employment.length > 0
      ? policy.target_employment.join(", ")
      : "제한 없음",
    income: policy.target_income_max
      ? `연소득 ${formatMoney(policy.target_income_max)} 이하`
      : "소득 무관",
    region: Array.isArray(policy.target_regions) && policy.target_regions.length > 0
      ? policy.target_regions.join(", ")
      : "전국",

    period: policy.deadline || "상시 신청",
    amount: policy.budget_max ? `최대 ${formatMoney(policy.budget_max)} 지원` : (policy.benefit || "자세히 보기"),

    // AI 설명 - match_reasons 우선 사용 (간결), 없으면 explanation
    match_reasons: statePolicy?.match_reasons || [],
    ai_explanation: statePolicy?.explanation ? decodeHtml(statePolicy.explanation) : null,

    // 혜택 요약 (200자 이내로 자르기)
    benefit_summary: (() => {
      const raw = decodeHtml(policy.benefit || policy.description || "");
      if (raw.length <= 200) return raw;
      return raw.substring(0, 200) + "...";
    })(),
    benefit_full: decodeHtml(policy.benefit || policy.description || "상세 혜택 정보가 없습니다."),

    // 신청 URL: application_url 있으면 사용, 없으면 온통청년 정책 상세페이지
    url: (() => {
      if (policy.application_url) return policy.application_url;

      const policyId = policy.policy_id || policy.id;
      if (policyId && policyId !== 'undefined') {
        // 온통청년 정책 상세 페이지 URL 패턴 (정확한 패턴)
        return `https://www.youthcenter.go.kr/youthPolicy/ythPlcyTotalSearch/ythPlcyDetail/${policyId}`;
      }

      return `https://www.google.com/search?q=${encodeURIComponent(policy.title + ' 청년정책 신청')}`;
    })()
  };

  return (
    <div className="bg-gray-50 min-h-screen flex justify-center animate-fadeIn" >
      <div className="w-full max-w-lg bg-white min-h-screen sm:min-h-0 sm:h-auto sm:my-10 sm:rounded-3xl shadow-xl flex flex-col">

        {/* 헤더 */}
        <div className="p-4 border-b flex items-center sticky top-0 bg-white z-10 sm:rounded-t-3xl">
          <button onClick={() => navigate(-1)} className="text-2xl mr-4 hover:text-blue-600 transition">
            ←
          </button>
          <span className="font-bold text-lg">정책 상세 정보</span>
        </div>

        {/* 본문 내용 */}
        <div className="p-6 flex-1 overflow-y-auto">
          {/* 뱃지 & 제목 */}
          <div className="mb-6">
            <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-bold">
              {displayData.badge}
            </span>
            <h1 className="text-2xl font-bold mt-3 mb-2 text-gray-900 break-keep leading-tight">{displayData.title}</h1>
            <p className="text-blue-600 font-bold text-xl">{displayData.amount}</p>
          </div>

          {/* AI 추천 사유 (match_reasons 우선, 없으면 explanation) */}
          {(displayData.match_reasons.length > 0 || displayData.ai_explanation) && (
            <div className="bg-blue-50 border border-blue-100 p-5 rounded-2xl mb-8 shadow-sm">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-lg">🤖</span>
                <h3 className="font-bold text-blue-800">AI 추천 사유</h3>
              </div>
              {displayData.match_reasons.length > 0 ? (
                <ul className="space-y-2">
                  {displayData.match_reasons.slice(0, 5).map((reason, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-gray-700 text-sm">
                      <span className="text-green-500 font-bold">✓</span>
                      <span>{reason}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-700 leading-relaxed text-sm whitespace-pre-wrap">
                  {displayData.ai_explanation}
                </p>
              )}
            </div>
          )}

          <div className="space-y-8">
            <BenefitSection summary={displayData.benefit_summary} full={displayData.benefit_full} />

            <div className="grid grid-cols-2 gap-6">
              <Section title="🎯 신청 연령" content={displayData.age} />
              <Section title="💰 소득 조건" content={displayData.income} />
              <Section title="💼 취업 상태" content={displayData.employment} />
              <Section title="📍 거주 지역" content={displayData.region} />
            </div>

            <Section title="📅 신청 기간" content={displayData.period} />

            {/* 기관 정보가 있다면 표시 */}
            {policy.agency && (
              <Section title="🏢 주관 기관" content={policy.agency} />
            )}
          </div>
        </div>

        {/* 하단 고정 버튼 */}
        <div className="p-4 border-t bg-white sm:rounded-b-3xl mt-auto">
          <Button onClick={() => window.open(displayData.url || 'https://youth.seoul.go.kr', '_blank')}>
            신청 홈페이지 바로가기 🔗
          </Button>
        </div>
      </div>
    </div >
  );
};

// 작은 섹션 컴포넌트
const Section = ({ title, content }) => (
  <div>
    <h3 className="text-sm font-bold text-gray-400 mb-1">{title}</h3>
    <p className="text-gray-800 font-medium break-keep">{content || "정보 없음"}</p>
  </div>
);

// 혜택 섹션 컴포넌트 (요약 + 더보기)
const BenefitSection = ({ summary, full }) => {
  const [expanded, setExpanded] = React.useState(false);
  const needsExpand = full && full.length > 200;

  return (
    <div>
      <h3 className="text-sm font-bold text-gray-400 mb-2">📢 지원 혜택</h3>
      <div className="text-gray-800 font-medium break-keep leading-relaxed">
        {expanded ? full : summary}
        {needsExpand && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="ml-2 text-blue-600 text-sm font-bold hover:underline"
          >
            {expanded ? "접기" : "더보기"}
          </button>
        )}
      </div>
    </div>
  );
};

export default PolicyDetail;