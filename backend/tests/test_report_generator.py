from datetime import datetime, timezone
from app.services.report_generator import (
    daily_report, weekly_report, monthly_report, regenerate_report,
    _load_prompt, _save_report,
)
from app.models.ai_work_summary import AiWorkSummary


class TestPromptLoading:
    def test_load_daily(self):
        prompt = _load_prompt("daily_report.txt")
        assert "日报" in prompt or "daily" in prompt.lower() or "今日" in prompt

    def test_load_weekly(self):
        prompt = _load_prompt("weekly_report.txt")
        assert "周报" in prompt or "weekly" in prompt.lower()

    def test_load_monthly(self):
        prompt = _load_prompt("monthly_report.txt")
        assert "月报" in prompt or "monthly" in prompt.lower()


class TestDailyReport:
    def test_generate(self, db):
        report = daily_report(db)
        assert report.report_type == "daily"
        assert report.title.startswith("日报")
        assert report.content

    def test_custom_date(self, db):
        target = datetime(2026, 6, 1, tzinfo=timezone.utc)
        report = daily_report(db, date=target)
        assert report.period_start.year == 2026
        assert report.period_start.month == 6


class TestWeeklyReport:
    def test_generate(self, db):
        report = weekly_report(db)
        assert report.report_type == "weekly"
        assert report.title.startswith("周报")


class TestMonthlyReport:
    def test_generate(self, db):
        report = monthly_report(db)
        assert report.report_type == "monthly"
        assert report.title.startswith("月报")


class TestRegenerate:
    def test_nonexistent(self, db):
        result = regenerate_report(db, 99999)
        assert result is None

    def test_regenerate_daily(self, db):
        original = daily_report(db)
        result = regenerate_report(db, original.id)
        assert result is not None
        assert result.report_type == "daily"


class TestSaveReport:
    def test_save(self, db):
        now = datetime.now(timezone.utc)
        report = _save_report(db, "daily", "测试日报", "测试内容", now, now)
        assert report.id is not None
        saved = db.query(AiWorkSummary).filter(AiWorkSummary.id == report.id).first()
        assert saved is not None
