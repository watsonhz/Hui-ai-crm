# /qa — QA 测试工作流 (PC5)

## 触发命令
```
/qa          # 全量测试（unit + integration + api + security）
/qa-only     # 仅 API 快速测试 (smoke)
/benchmark   # 性能基准测试
```

## 执行流程

### Stage 1: 单元测试
```bash
cd C:\DevProjects\ai-crm\backend
pytest tests/ -m unit -v --tb=short --timeout=15
```

### Stage 2: 集成测试 (DB)
```bash
pytest tests/ -m integration -v --tb=short --timeout=30
```

### Stage 3: API 端点测试
```bash
pytest tests/ -m api -v --tb=short --timeout=60
```

### Stage 4: 安全验证测试
```bash
pytest tests/security/ -v --tb=short
```

### Stage 5: 覆盖率报告
```bash
pytest tests/ --cov=app --cov-report=html:tests/reports/coverage --cov-report=term
```

### Stage 6: 性能基准 (可选)
```bash
cd C:\DevProjects\ai-crm\backend
python -m locust -f tests/performance/locustfile.py --headless -u 10 -r 2 -t 30s
```

## QA 报告格式

```markdown
# QA REPORT: <PR-XXX>
- **执行日期**: YYYY-MM-DD HH:MM
- **测试环境**: Windows / Python 3.x
- **通过率**: X/Y (Z%)
- **覆盖率**: X%
- **P0 Bug**: 0
- **P1 Bug**: 0
- **结论**: APPROVED / REJECTED
```

## 回归测试
Windows 计划任务: 每日凌晨 3:00 自动执行 `pytest tests/ -m smoke`

## 相关文件
- pytest.ini: 测试配置
- tests/unit/: 单元测试
- tests/integration/: 集成测试
- tests/api/: API 测试
- tests/security/: 安全验证
- tests/performance/: 性能测试
- tests/reports/: 测试报告
