// src/pages/PolicyDetail.jsx
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Button from '../components/common/Button';

// 가짜 상세 데이터 (DB 대용)
const POLICY_DB = {
  1: {
    title: "청년 월세 지원",
    badge: "주거",
    summary: "월 최대 20만원씩 12개월간 월세를 지원해드립니다.",
    target: "만 19세 ~ 34세 무주택 청년 (소득 기준 충족 시)",
    period: "2024.02.26 ~ 2025.02.25",
    content: "경제적 어려움을 겪는 청년층의 주거비 부담을 덜어드리기 위해 국토교통부에서 월세를 한시적으로 지원하는 사업입니다.",
    amount: "월 20만원",
  },
  2: {
    title: "청년 도약 계좌",
    badge: "금융",
    summary: "5년 만기 적금 가입 시 정부 기여금과 비과세 혜택 제공",
    target: "만 19세 ~ 34세 청년 (개인소득 7,500만원 이하)",
    period: "매월 가입 신청 기간 운영",
    content: "청년들의 중장기 자산 형성을 돕기 위한 정책 금융 상품입니다. 매월 70만원 한도 내에서 자유롭게 납입 가능합니다.",
    amount: "최대 5,000만원",
  },
  3: {
    title: "기후동행카드 청년 할인",
    badge: "교통",
    summary: "월 5만원대로 서울 시내 대중교통 무제한 이용",
    target: "만 19세 ~ 39세 청년",
    period: "상시 신청 가능",
    content: "기후 위기 대응과 교통비 절감을 위해 서울시에서 운영하는 무제한 대중교통 정기권입니다. 청년은 일반권보다 7,000원 할인된 가격에 이용 가능합니다.",
    amount: "월 7,000원 할인",
  }
};

const PolicyDetail = () => {
  const { id } = useParams(); // URL에서 숫자(id) 가져오기
  const navigate = useNavigate();
  const [policy, setPolicy] = useState(null);

  useEffect(() => {
    // DB에서 id에 맞는 데이터 꺼내오기
    const data = POLICY_DB[id];
    setPolicy(data);
  }, [id]);

  if (!policy) return <div className="p-10 text-center">정보를 불러오는 중...</div>;

  return (
    <div className="bg-gray-50 min-h-screen flex justify-center">
      <div className="w-full max-w-lg bg-white min-h-screen sm:min-h-0 sm:h-auto sm:my-10 sm:rounded-3xl shadow-xl flex flex-col">
        
        {/* 헤더: 뒤로가기 버튼 */}
        <div className="p-4 border-b flex items-center">
          <button onClick={() => navigate(-1)} className="text-2xl mr-4">
            ←
          </button>
          <span className="font-bold text-lg">정책 상세 정보</span>
        </div>

        {/* 본문 내용 */}
        <div className="p-6 flex-1 overflow-y-auto">
          {/* 뱃지 & 제목 */}
          <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-bold">
            {policy.badge}
          </span>
          <h1 className="text-2xl font-bold mt-3 mb-2 text-gray-900">{policy.title}</h1>
          <p className="text-blue-600 font-bold text-xl mb-6">{policy.amount}</p>

          <div className="space-y-6">
            <Section title="📢 한줄 요약" content={policy.summary} />
            <Section title="🎯 지원 대상" content={policy.target} />
            <Section title="📅 신청 기간" content={policy.period} />
            
            <div className="bg-gray-50 p-4 rounded-xl">
              <h3 className="font-bold mb-2 text-gray-700">상세 내용</h3>
              <p className="text-gray-600 leading-relaxed text-sm">
                {policy.content}
              </p>
            </div>
          </div>
        </div>

        {/* 하단 고정 버튼 */}
        <div className="p-4 border-t bg-white sm:rounded-b-3xl mt-auto">
           <Button onClick={() => window.open('https://youth.seoul.go.kr', '_blank')}>
             신청 홈페이지 바로가기 🔗
           </Button>
        </div>
      </div>
    </div>
  );
};

// 작은 섹션 컴포넌트 (내부용)
const Section = ({ title, content }) => (
  <div>
    <h3 className="text-sm font-bold text-gray-400 mb-1">{title}</h3>
    <p className="text-gray-800 font-medium">{content}</p>
  </div>
);

export default PolicyDetail;