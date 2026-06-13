from datetime import datetime, timezone, timedelta
from app.models.crm_relationship import CrmRelationship
from app.models.action_item import ActionItem
from app.services.diagnosis_engine import (
    signal_s1_visit_overdue, signal_s2_stage_stall, signal_s3_visit_gap_increase,
    signal_s4_p0_overdue, signal_s5_warmth_drop, signal_s6_decision_gap,
    signal_s7_keyperson_silence, signal_s9_low_outcome, signal_s10_competitor,
    signal_s11_acceptance_overdue, signal_s12_payment_delay,
    run_full_diagnosis, SignalResult,
)


class TestSignalS1:
    def test_no_visits(self, db):
        result = signal_s1_visit_overdue(db, 99999)
        assert result.triggered is False

    def test_has_visits(self, db):
        db.add(CrmRelationship(customer_id=1, visit_date=datetime.now(timezone.utc) - timedelta(days=1)))
        db.commit()
        result = signal_s1_visit_overdue(db, 1)
        assert result.triggered is False


class TestSignalS2:
    def test_no_project(self, db):
        result = signal_s2_stage_stall(db, 99999)
        assert result.triggered is False


class TestSignalS3:
    def test_insufficient_visits(self, db):
        result = signal_s3_visit_gap_increase(db, 99999)
        assert result.triggered is False


class TestSignalS4:
    def test_no_overdue(self, db):
        result = signal_s4_p0_overdue(db, 99999)
        assert result.triggered is False

    def test_has_overdue(self, db):
        db.add(ActionItem(title="逾期P0", priority=0, is_done=False,
                          due_date=datetime.now(timezone.utc) - timedelta(days=5), project_id=1))
        db.commit()
        result = signal_s4_p0_overdue(db, 1)
        assert result.triggered is True


class TestSignalS5:
    def test_no_contacts(self):
        result = signal_s5_warmth_drop(None, [])
        assert result.triggered is False

    def test_warmth_drop_detected(self):
        contacts = [{"name": "张总", "weight": 6, "consecutive_cool": 3}]
        result = signal_s5_warmth_drop(None, contacts)
        assert result.triggered is True
        assert result.severity >= 1


class TestSignalS6:
    def test_gap_detected(self):
        result = signal_s6_decision_gap(1, ["销售"], {"1": ["技术", "财务", "高管"]})
        assert result.triggered is True
        assert "技术" in result.diagnosis

    def test_no_gap(self):
        result = signal_s6_decision_gap(1, ["技术", "财务", "高管"], {"1": ["技术", "财务", "高管"]})
        assert result.triggered is False


class TestSignalS7:
    def test_no_contacts(self):
        result = signal_s7_keyperson_silence(None, [])
        assert result.triggered is False


class TestSignalS9:
    def test_insufficient_visits(self, db):
        result = signal_s9_low_outcome(db, 99999)
        assert result.triggered is False


class TestSignalS10:
    def test_no_competitor(self):
        result = signal_s10_competitor([])
        assert result.triggered is False

    def test_competitor_detected(self):
        result = signal_s10_competitor([{"type": "价格战", "detail": "竞品降价20%"}])
        assert result.triggered is True
        assert result.severity == 2


class TestSignalS11:
    def test_no_project(self, db):
        result = signal_s11_acceptance_overdue(db, 99999)
        assert result.triggered is False


class TestSignalS12:
    def test_no_project(self, db):
        result = signal_s12_payment_delay(db, 99999)
        assert result.triggered is False


class TestSignalResult:
    def test_to_dict(self):
        r = SignalResult("S1", True, severity=2, diagnosis="测试诊断", advice="测试建议")
        d = r.to_dict()
        assert d["signal_id"] == "S1"
        assert d["severity"] == 2
        assert d["triggered"] is True


class TestFullDiagnosis:
    def test_basic(self, db):
        results = run_full_diagnosis(db, customer_id=1)
        assert len(results) >= 3

    def test_with_project(self, db):
        results = run_full_diagnosis(db, customer_id=1, project_id=1)
        assert len(results) >= 6

    def test_with_contacts(self, db):
        results = run_full_diagnosis(db, customer_id=1, contacts=[{"name": "test", "weight": 8, "last_contact_days": 30, "consecutive_cool": 2}])
        assert len(results) >= 4
