import os
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.ai_work_summary import AiWorkSummary
from app.models.crm_relationship import CrmRelationship
from app.models.action_item import ActionItem
from app.models.project import Project

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "prompts")

def _load_prompt(name: str) -> str:
    path = os.path.join(PROMPTS_DIR, name)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""


def _call_llm(prompt: str) -> str:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key or api_key.startswith("sk-your-"):
        return "[AI报告占位] DeepSeek API Key 未配置，请设置 DEEPSEEK_API_KEY 环境变量。"
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[AI报告生成失败] {str(e)}"


def _save_report(db: Session, report_type: str, title: str, content: str,
                 period_start: datetime, period_end: datetime) -> AiWorkSummary:
    report = AiWorkSummary(
        report_type=report_type,
        title=title,
        content=content,
        period_start=period_start,
        period_end=period_end,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def daily_report(db: Session, date: Optional[datetime] = None) -> AiWorkSummary:
    target_date = date or datetime.now(timezone.utc)
    start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    visits = db.query(CrmRelationship).filter(
        CrmRelationship.visit_date >= start,
        CrmRelationship.visit_date < end,
    ).all()
    actions = db.query(ActionItem).filter(
        ActionItem.due_date >= start,
        ActionItem.due_date < end,
    ).all()
    visit_lines = []
    for v in visits:
        visit_lines.append(f"- [{v.visit_date.strftime('%H:%M')}] 客户{v.customer_id} {['','电话','拜访','会议','邮件','微信'][v.visit_type]} 产出等级={v.outcome_level}")
    action_lines = []
    for a in actions:
        status = "done" if a.is_done else "pending"
        action_lines.append(f"- [{status}] {a.title} (优先级={a.priority})")
    prompt = _load_prompt("daily_report.txt").format(
        visit_data="\n".join(visit_lines) if visit_lines else "无拜访记录",
        action_items="\n".join(action_lines) if action_lines else "无行动项",
    )
    content = _call_llm(prompt)
    title = f"日报-{target_date.strftime('%Y-%m-%d')}"
    return _save_report(db, "daily", title, content, start, end)


def weekly_report(db: Session, week_start: Optional[datetime] = None) -> AiWorkSummary:
    today = datetime.now(timezone.utc)
    if week_start is None:
        week_start = today - timedelta(days=today.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = week_start + timedelta(days=7)
    daily_reports = db.query(AiWorkSummary).filter(
        AiWorkSummary.report_type == "daily",
        AiWorkSummary.period_start >= week_start,
        AiWorkSummary.period_start < week_end,
    ).all()
    daily_text = "\n\n".join([f"### {r.title}\n{r.content}" for r in daily_reports])
    total_visits = db.query(func.count(CrmRelationship.id)).filter(
        CrmRelationship.visit_date >= week_start,
        CrmRelationship.visit_date < week_end,
    ).scalar()
    done_actions = db.query(func.count(ActionItem.id)).filter(
        ActionItem.updated_at >= week_start,
        ActionItem.updated_at < week_end,
        ActionItem.is_done == True,
    ).scalar()
    new_projects = db.query(func.count(Project.id)).filter(
        Project.created_at >= week_start,
        Project.created_at < week_end,
    ).scalar()
    stats = f"本周拜访: {total_visits}次 | 完成任务: {done_actions}个 | 新项目: {new_projects}个"
    prompt = _load_prompt("weekly_report.txt").format(
        daily_reports=daily_text if daily_text else "本周暂无日报",
        weekly_stats=stats,
    )
    content = _call_llm(prompt)
    title = f"周报-{week_start.strftime('%Y-W%W')}"
    return _save_report(db, "weekly", title, content, week_start, week_end)


def monthly_report(db: Session, year: Optional[int] = None, month: Optional[int] = None) -> AiWorkSummary:
    today = datetime.now(timezone.utc)
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    month_start = datetime(year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        month_end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        month_end = datetime(year, month + 1, 1, tzinfo=timezone.utc)
    weekly_reports = db.query(AiWorkSummary).filter(
        AiWorkSummary.report_type == "weekly",
        AiWorkSummary.period_start >= month_start,
        AiWorkSummary.period_start < month_end,
    ).all()
    weekly_text = "\n\n".join([f"### {r.title}\n{r.content}" for r in weekly_reports])
    total_visits = db.query(func.count(CrmRelationship.id)).filter(
        CrmRelationship.visit_date >= month_start,
        CrmRelationship.visit_date < month_end,
    ).scalar()
    won_projects = db.query(func.count(Project.id)).filter(
        Project.stage.in_([9, 10, 11]),
        Project.updated_at >= month_start,
        Project.updated_at < month_end,
    ).scalar()
    lost_projects = db.query(func.count(Project.id)).filter(
        Project.stage == 12,
        Project.updated_at >= month_start,
        Project.updated_at < month_end,
    ).scalar()
    total_new = db.query(func.count(Project.id)).filter(
        Project.created_at >= month_start,
        Project.created_at < month_end,
    ).scalar()
    metrics = f"拜访: {total_visits}次 | 新项目: {total_new}个 | 赢单: {won_projects}个 | 丢单: {lost_projects}个"
    prompt = _load_prompt("monthly_report.txt").format(
        weekly_reports=weekly_text if weekly_text else "本月暂无周报",
        monthly_metrics=metrics,
    )
    content = _call_llm(prompt)
    title = f"月报-{year}年{month}月"
    return _save_report(db, "monthly", title, content, month_start, month_end)


def regenerate_report(db: Session, report_id: int) -> Optional[AiWorkSummary]:
    report = db.query(AiWorkSummary).filter(AiWorkSummary.id == report_id).first()
    if not report:
        return None
    generators = {"daily": daily_report, "weekly": weekly_report, "monthly": monthly_report}
    fn = generators.get(report.report_type)
    if not fn:
        return None
    if report.report_type == "daily":
        new_report = fn(db, report.period_start)
    elif report.report_type == "weekly":
        new_report = fn(db, report.period_start)
    else:
        new_report = fn(db, report.period_start.year, report.period_start.month)
    return new_report
