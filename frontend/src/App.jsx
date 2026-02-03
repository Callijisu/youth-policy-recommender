// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Survey from './pages/Survey';
import PolicyDetail from './pages/PolicyDetail';
import Saved from './pages/Saved';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* 메인 화면: 설문조사 */}
          <Route path="/" element={<Survey />} />

          {/* 상세 화면: /policy/1, /policy/2 등 ID에 따라 바뀜 */}
          <Route path="/policy/:id" element={<PolicyDetail />} />

          {/* 내 보관함 */}
          <Route path="/saved" element={<Saved />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;