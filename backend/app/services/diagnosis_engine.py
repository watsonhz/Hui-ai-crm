import json
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.crm_relationship import CrmRelationship
from app.models.action_item import ActionItem
from app.models.bidding import Bidding
from app.models.project import Project
from app.models.sys_config import SysConfig

SIGNAL_DEFS = {
    "S1": {"name": "拜访超期", "dimension": "时间"},
    "S2": {"name": "项目阶段卡顿", "dimension": "时间"},
    "S3": {"name": "拜访间隔拉长", "dimension": "时间"},
    "S4": {"name": "P0待办逾期", "dimension": "时间"},
    "S5": {"name": "关键人关系恶化", "dimension": "决策链"},
    "S6": {"name": "决策链缺口", "dimension": "决策链"},
    "S7": {"name": "关键人长期未接触", "dimension": "决策链"},
    "S8": {"name": "支持度与阶段不匹配", "dimension": "决策链"},
    "S9": {"name": "拜访产出低下", "dimension": "项目"},
    "S10": {"name": "竞品动态", "dimension": "项目"},
    "S11": {"name": "验收逾期", "dimension": "项目"},
    "S12": {"name": "回款延迟", "dimension": "项目"},
}

L1_TEMPLATES = {
    "S1": "{customer_name}上次拜访距今{days}天，超过{level}客户阈值{threshold}天",
    "S2": "项目{project_name}在阶段{stage_name}停留{days}天，超过预期{threshold}天",
    "S3": "最近3次拜访间隔呈递增趋势({i1}d→{i2}d→{i3}d)，活跃度下降",
    "S4": "存在{count}个P0待办逾期，需立即处理",
    "S5": "关键人{name}(权重{weight})连续{count}次关系降温",
    "S6": "当前阶段{stage}缺少必识别角色: {roles}",
    "S7": "关键人{name}(权重{weight})已{silence_days}天未接触",
    "S8": "决策链支持度{actual}低于当前阶段{stage}要求{required}",
    "S9": "连续{count}次拜访无P0/P1产出",
    "S10": "竞品{dynamic_type}动态: {detail}",
    "S11": "项目{project_name}验收已逾期{days}天",
    "S12": "项目{project_name}回款延迟{days}天",
}

L2_TEMPLATES = {
    "S1": "建议立即安排拜访，了解客户最新动态和需求变化",
    "S2": "分析阶段卡顿原因，制定推进计划，必要时升级处理",
    "S3": "提高拜访频率，主动提供价值信息，重建客户关系",
    "S4": "优先处理P0待办，调整资源分配，避免项目风险",
    "S5": "评估关系恶化原因，制定关系修复计划，安排高层拜访",
    "S6": "尽快识别并建立缺失角色的联系，完善决策链覆盖",
    "S7": "安排高层拜访或商务活动，重新激活关键人关系",
    "S8": "制定支持度提升计划，寻找内部支持者，增强方案价值展示",
    "S9": "提升拜访准备质量，每次拜访明确目标和产出计划",
    "S10": "分析竞品优劣势，制定差异化竞争策略，更新竞争话术",
    "S11": "加速验收流程，协调资源解决验收阻塞问题",
    "S12": "跟进回款进度，了解延迟原因，必要时启动催款流程",
}

L3_TEMPLATES = {
    "S1": {"action": "立即安排客户拜访", "owner": "销售经理", "deadline": "3天"},
    "S2": {"action": "组织项目推进会议", "owner": "项目经理", "deadline": "5天"},
    "S3": {"action": "制定客户活跃度提升计划", "owner": "销售代表", "deadline": "7天"},
    "S4": {"action": "处理逾期P0待办", "owner": "责任人", "deadline": "2天"},
    "S5": {"action": "制定关系修复计划", "owner": "销售总监", "deadline": "5天"},
    "S6": {"action": "识别并接触缺失角色", "owner": "销售经理", "deadline": "7天"},
    "S7": {"action": "安排高层拜访", "owner": "销售总监", "deadline": "5天"},
    "S8": {"action": "制定支持度提升计划", "owner": "销售经理", "deadline": "7天"},
    "S9": {"action": "提升拜访质量", "owner": "销售代表", "deadline": "持续"},
    "S10": {"action": "制定竞争应对策略", "owner": "销售经理", "deadline": "3天"},
    "S11": {"action": "加速验收流程", "owner": "项目经理", "deadline": "5天"},
    "S12": {"action": "跟进回款", "owner": "销售经理", "deadline": "7天"},
}

L4_SCRIPTS = {
    "S1": "{customer_name}您好，距离上次沟通已有一段时间，我们非常关注贵司的最新需求，方便近期安排一次交流吗？",
    "S2": "{project_name}项目当前进展需要我们一起review，我们建议尽快组织一次项目推进会，您看什么时间方便？",
    "S3": "我们整理了近期行业动态和案例，希望能为您提供有价值的参考，方便安排一次交流吗？",
    "S4": "关于{project_name}的紧急事项需要尽快处理，我们已安排相关人员，请您一并确认优先级。",
    "S5": "感谢{name}一直以来的支持，我们希望近期安排一次拜访，就后续合作深入交流。",
    "S10": "我们注意到市场上出现了一些新动态，希望能与您分享我们的分析和应对思路。",
}

SEVERITY_THRESHOLDS = {
    "S1": (30, (lambda d, t: d > t * 3, lambda d, t: d > t * 1.5)),
    "S2": (14, (lambda d, t: d > t * 3, lambda d, t: d > t * 1.5)),
    "S3": (None, (lambda d: d[-1] > d[0] * 2, lambda d: d[-1] > d[0] * 1.3)),
    "S4": (None, (lambda c: c >= 5, lambda c: c >= 2)),
    "S7": (21, (lambda d, t: d > t * 3, lambda d, t: d > t * 1.5)),
    "S11": (7, (lambda d, t: d > t * 2, lambda d, t: d > t)),
    "S12": (30, (lambda d, t: d > t * 2, lambda d, t: d > t)),
}


def get_config(db: Session, key: str, default=None):
    row = db.query(SysConfig).filter(SysConfig.config_key == key).first()
    if row:
        try:
            return json.loads(row.config_value)
        except (json.JSONDecodeError, TypeError):
            return row.config_value
    return default


class SignalResult:
    def __init__(self, signal_id: str, triggered: bool, severity: int = 1,
                 diagnosis: str = "", advice: str = "", action: dict = None, script: str = ""):
        self.signal_id = signal_id
        self.name = SIGNAL_DEFS.get(signal_id, {}).get("name", signal_id)
        self.dimension = SIGNAL_DEFS.get(signal_id, {}).get("dimension", "")
        self.triggered = triggered
        self.severity = severity
        self.diagnosis = diagnosis
        self.advice = advice
        self.action = action or {}
        self.script = script

    def to_dict(self):
        return {
            "signal_id": self.signal_id,
            "name": self.name,
            "dimension": self.dimension,
            "triggered": self.triggered,
            "severity": self.severity,
            "diagnosis": self.diagnosis,
            "advice": self.advice,
            "action": self.action,
            "script": self.script,
        }


def _calc_severity(signal_id: str, value, threshold=None):
    rules = SEVERITY_THRESHOLDS.get(signal_id)
    if not rules:
        return 1
    default_threshold, (sev3_check, sev2_check) = rules
    t = threshold if threshold is not None else default_threshold
    if t is None:
        if sev3_check(value):
            return 3
        if sev2_check(value):
            return 2
        return 1
    if sev3_check(value, t):
        return 3
    if sev2_check(value, t):
        return 2
    return 1


def signal_s1_visit_overdue(db: Session, customer_id: int) -> SignalResult:
    last_visit = db.query(func.max(CrmRelationship.visit_date)).filter(
        CrmRelationship.customer_id == customer_id
    ).scalar()
    if not last_visit:
        return SignalResult("S1", False)
    days = (datetime.now(timezone.utc) - last_visit).days
    thresholds = get_config(db, "s1_visit_overdue_days", {"normal": 30})
    threshold = thresholds.get("normal", 30)
    triggered = days > threshold
    severity = _calc_severity("S1", days, threshold) if triggered else 0
    return SignalResult(
        signal_id="S1", triggered=triggered, severity=severity,
        diagnosis=L1_TEMPLATES["S1"].format(customer_name=f"客户{customer_id}", days=days, level="普通", threshold=threshold),
        advice=L2_TEMPLATES["S1"],
        action=L3_TEMPLATES["S1"],
        script=L4_SCRIPTS["S1"].format(customer_name=f"客户{customer_id}"),
    )


def signal_s2_stage_stall(db: Session, project_id: int) -> SignalResult:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return SignalResult("S2", False)
    days = (datetime.now(timezone.utc).replace(tzinfo=None) - project.updated_at.replace(tzinfo=None)).days
    thresholds = get_config(db, "s2_stage_stall_days", {"default": 14})
    threshold = thresholds.get("default", 14)
    triggered = days > threshold
    severity = _calc_severity("S2", days, threshold) if triggered else 0
    return SignalResult(
        signal_id="S2", triggered=triggered, severity=severity,
        diagnosis=L1_TEMPLATES["S2"].format(project_name=project.name, stage_name=f"阶段{project.stage}", days=days, threshold=threshold),
        advice=L2_TEMPLATES["S2"],
        action=L3_TEMPLATES["S2"],
    )


def signal_s3_visit_gap_increase(db: Session, customer_id: int) -> SignalResult:
    visits = db.query(CrmRelationship.visit_date).filter(
        CrmRelationship.customer_id == customer_id
    ).order_by(CrmRelationship.visit_date.desc()).limit(4).all()
    if len(visits) < 3:
        return SignalResult("S3", False)
    dates = [v[0] for v in visits[:3]]
    gaps = [(dates[i] - dates[i + 1]).days for i in range(len(dates) - 1)]
    triggered = len(gaps) >= 2 and gaps[0] > gaps[1]
    severity = _calc_severity("S3", gaps) if triggered else 0
    return SignalResult(
        signal_id="S3", triggered=triggered, severity=severity,
        diagnosis=L1_TEMPLATES["S3"].format(i1=gaps[0], i2=gaps[1], i3=gaps[2] if len(gaps) > 2 else gaps[1]),
        advice=L2_TEMPLATES["S3"],
        action=L3_TEMPLATES["S3"],
    )


def signal_s4_p0_overdue(db: Session, project_id: int) -> SignalResult:
    count = db.query(func.count(ActionItem.id)).filter(
        ActionItem.project_id == project_id,
        ActionItem.priority == 0,
        ActionItem.is_done == False,
        ActionItem.due_date < datetime.now(timezone.utc),
    ).scalar()
    threshold = int(get_config(db, "s4_p0_overdue_count", 2))
    triggered = count >= threshold
    severity = _calc_severity("S4", count) if triggered else 0
    return SignalResult(
        signal_id="S4", triggered=triggered, severity=severity,
        diagnosis=L1_TEMPLATES["S4"].format(count=count),
        advice=L2_TEMPLATES["S4"],
        action=L3_TEMPLATES["S4"],
    )


def signal_s5_warmth_drop(_db: Session, contacts: list[dict]) -> SignalResult:
    if not contacts:
        return SignalResult("S5", False)
    for c in contacts:
        if c.get("weight", 0) >= 5 and c.get("consecutive_cool", 0) >= 2:
            return SignalResult(
                signal_id="S5", triggered=True, severity=2 if c["weight"] >= 7 else 1,
                diagnosis=L1_TEMPLATES["S5"].format(name=c["name"], weight=c["weight"], count=c["consecutive_cool"]),
                advice=L2_TEMPLATES["S5"],
                action=L3_TEMPLATES["S5"],
            )
    return SignalResult("S5", False)


def signal_s6_decision_gap(project_stage: int, identified_roles: list[str], required_roles: dict) -> SignalResult:
    stage_key = str(project_stage)
    required = required_roles.get(stage_key, [])
    missing = [r for r in required if r not in identified_roles]
    triggered = len(missing) > 0
    return SignalResult(
        signal_id="S6", triggered=triggered, severity=len(missing),
        diagnosis=L1_TEMPLATES["S6"].format(stage=project_stage, roles=", ".join(missing)) if triggered else "",
        advice=L2_TEMPLATES["S6"],
        action=L3_TEMPLATES["S6"],
    )


def signal_s7_keyperson_silence(db: Session, contacts: list[dict]) -> SignalResult:
    threshold = int(get_config(db, "s7_keyperson_silence_days", 21))
    min_weight = int(get_config(db, "s7_keyperson_min_weight", 7))
    for c in contacts:
        if c.get("weight", 0) >= min_weight and c.get("last_contact_days", 0) > threshold:
            severity = _calc_severity("S7", c["last_contact_days"], threshold)
            return SignalResult(
                signal_id="S7", triggered=True, severity=severity,
                diagnosis=L1_TEMPLATES["S7"].format(name=c["name"], weight=c["weight"], silence_days=c["last_contact_days"]),
                advice=L2_TEMPLATES["S7"],
                action=L3_TEMPLATES["S7"],
            )
    return SignalResult("S7", False).to_dict()


def signal_s8_support_mismatch(project_stage: int, support_level: int, expected_support: dict) -> SignalResult:
    expected = expected_support.get(str(project_stage), 0)
    triggered = support_level < expected
    return SignalResult(
        signal_id="S8", triggered=triggered, severity=expected - support_level if triggered else 0,
        diagnosis=L1_TEMPLATES["S8"].format(actual=support_level, stage=project_stage, required=expected) if triggered else "",
        advice=L2_TEMPLATES["S8"],
        action=L3_TEMPLATES["S8"],
    )


def signal_s9_low_outcome(db: Session, customer_id: int) -> SignalResult:
    threshold = int(get_config(db, "s9_low_outcome_count", 2))
    recent = db.query(CrmRelationship).filter(
        CrmRelationship.customer_id == customer_id
    ).order_by(CrmRelationship.visit_date.desc()).limit(threshold).all()
    if len(recent) < threshold:
        return SignalResult("S9", False)
    triggered = all(r.outcome_level == 0 for r in recent)
    severity = 3 if triggered and len(recent) >= threshold + 1 and all(r.outcome_level == 0 for r in recent[:threshold + 1]) else (2 if triggered else 0)
    return SignalResult(
        signal_id="S9", triggered=triggered, severity=severity,
        diagnosis=L1_TEMPLATES["S9"].format(count=threshold) if triggered else "",
        advice=L2_TEMPLATES["S9"],
        action=L3_TEMPLATES["S9"],
    )


def signal_s10_competitor(competitor_entries: list[dict]) -> SignalResult:
    triggered = len(competitor_entries) > 0
    if not triggered:
        return SignalResult("S10", False)
    latest = competitor_entries[0]
    return SignalResult(
        signal_id="S10", triggered=True, severity=2,
        diagnosis=L1_TEMPLATES["S10"].format(dynamic_type=latest.get("type", "未知"), detail=latest.get("detail", "")),
        advice=L2_TEMPLATES["S10"],
        action=L3_TEMPLATES["S10"],
        script=L4_SCRIPTS["S10"],
    )


def signal_s11_acceptance_overdue(db: Session, project_id: int) -> SignalResult:
    project = db.query(Project).filter(Project.id == project_id, Project.stage == 9).first()
    if not project or not project.end_date:
        return SignalResult("S11", False)
    days = (datetime.now().date() - project.end_date).days
    threshold = int(get_config(db, "s11_acceptance_overdue_days", 7))
    triggered = days > threshold
    severity = _calc_severity("S11", days, threshold) if triggered else 0
    return SignalResult(
        signal_id="S11", triggered=triggered, severity=severity,
        diagnosis=L1_TEMPLATES["S11"].format(project_name=project.name, days=days),
        advice=L2_TEMPLATES["S11"],
        action=L3_TEMPLATES["S11"],
    )


def signal_s12_payment_delay(db: Session, project_id: int) -> SignalResult:
    project = db.query(Project).filter(Project.id == project_id, Project.stage == 10).first()
    if not project or not project.updated_at:
        return SignalResult("S12", False)
    days = (datetime.now(timezone.utc).replace(tzinfo=None) - project.updated_at.replace(tzinfo=None)).days
    threshold = int(get_config(db, "s12_payment_delay_days", 30))
    triggered = days > threshold
    severity = _calc_severity("S12", days, threshold) if triggered else 0
    return SignalResult(
        signal_id="S12", triggered=triggered, severity=severity,
        diagnosis=L1_TEMPLATES["S12"].format(project_name=project.name, days=days),
        advice=L2_TEMPLATES["S12"],
        action=L3_TEMPLATES["S12"],
    )


def run_full_diagnosis(db: Session, customer_id: int, project_id: int = None,
                       contacts: list[dict] = None, competitor_entries: list[dict] = None,
                       identified_roles: list[str] = None, required_roles: dict = None,
                       support_level: int = 0, expected_support: dict = None) -> list[dict]:
    results = []
    results.append(signal_s1_visit_overdue(db, customer_id).to_dict())
    if project_id:
        results.append(signal_s2_stage_stall(db, project_id).to_dict())
        results.append(signal_s4_p0_overdue(db, project_id).to_dict())
        results.append(signal_s11_acceptance_overdue(db, project_id).to_dict())
        results.append(signal_s12_payment_delay(db, project_id).to_dict())
    results.append(signal_s3_visit_gap_increase(db, customer_id).to_dict())
    if contacts:
        results.append(signal_s5_warmth_drop(db, contacts).to_dict())
        results.append(signal_s7_keyperson_silence(db, contacts).to_dict())
    if identified_roles is not None and required_roles:
        results.append(signal_s6_decision_gap(1, identified_roles, required_roles).to_dict())
    if support_level and expected_support:
        results.append(signal_s8_support_mismatch(1, support_level, expected_support).to_dict())
    results.append(signal_s9_low_outcome(db, customer_id).to_dict())
    if competitor_entries:
        results.append(signal_s10_competitor(competitor_entries).to_dict())
    return results
