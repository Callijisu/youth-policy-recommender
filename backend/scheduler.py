"""
정책 데이터 자동 갱신 스케줄러
매일 새벽 3시에 온통청년 API에서 최신 정책 데이터를 수집합니다.
"""

import logging
from datetime import datetime
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger("scheduler")

class PolicyRefreshScheduler:
    """정책 데이터 자동 갱신 스케줄러"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.last_refresh: Optional[datetime] = None
        self.last_result: Optional[dict] = None
    
    async def refresh_policies(self):
        """온통청년 API에서 정책 데이터 갱신"""
        from import_policies import import_policies_from_api
        
        logger.info("🔄 정책 데이터 자동 갱신 시작...")
        start_time = datetime.now()
        
        try:
            # 정책 데이터 가져오기
            result = import_policies_from_api()
            
            self.last_refresh = datetime.now()
            self.last_result = {
                "success": True,
                "start_time": start_time.isoformat(),
                "end_time": self.last_refresh.isoformat(),
                "duration_seconds": (self.last_refresh - start_time).total_seconds(),
                "message": result.get("message", "정책 갱신 완료")
            }
            
            logger.info(f"✅ 정책 데이터 갱신 완료: {self.last_result['message']}")
            return self.last_result
            
        except Exception as e:
            self.last_refresh = datetime.now()
            self.last_result = {
                "success": False,
                "start_time": start_time.isoformat(),
                "end_time": self.last_refresh.isoformat(),
                "error": str(e)
            }
            logger.error(f"❌ 정책 데이터 갱신 실패: {e}")
            return self.last_result
    
    def start(self):
        """스케줄러 시작 - 매일 새벽 3시 실행"""
        # 매일 새벽 3시에 실행
        self.scheduler.add_job(
            self.refresh_policies,
            CronTrigger(hour=3, minute=0),
            id="policy_refresh",
            name="정책 데이터 자동 갱신",
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("📅 정책 자동 갱신 스케줄러 시작 (매일 03:00)")
    
    def stop(self):
        """스케줄러 중지"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("📅 정책 자동 갱신 스케줄러 중지")
    
    def get_status(self) -> dict:
        """스케줄러 상태 조회"""
        next_run = None
        job = self.scheduler.get_job("policy_refresh")
        if job and job.next_run_time:
            next_run = job.next_run_time.isoformat()
        
        return {
            "scheduler_running": self.scheduler.running,
            "next_refresh": next_run,
            "last_refresh": self.last_refresh.isoformat() if self.last_refresh else None,
            "last_result": self.last_result
        }


# 전역 스케줄러 인스턴스
_scheduler: Optional[PolicyRefreshScheduler] = None

def get_scheduler() -> PolicyRefreshScheduler:
    """스케줄러 싱글톤 인스턴스 반환"""
    global _scheduler
    if _scheduler is None:
        _scheduler = PolicyRefreshScheduler()
    return _scheduler
