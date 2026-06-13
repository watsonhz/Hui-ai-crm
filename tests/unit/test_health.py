"""
冒烟测试 — 验证测试框架本身可用。

这是整个测试体系的基线测试，确保：
- pytest 正确安装
- 项目模块可导入
- 基本断言工作正常
"""

import pytest


class TestFrameworkHealth:
    """验证 pytest 框架本身正常运作。"""

    def test_pytest_runs(self):
        """最基本的测试 — 证明 pytest 能运行。"""
        assert True

    def test_python_imports(self):
        """验证核心 Python 模块可导入。"""
        import sys
        import os

        assert sys.version_info >= (3, 8), f"Python 版本过低: {sys.version}"
        assert os.path.exists("pytest.ini"), "pytest.ini 配置文件缺失"

    def test_project_structure(self):
        """验证测试目录结构完整。"""
        import os

        required_dirs = [
            "tests/unit",
            "tests/integration",
            "tests/api",
            "tests/performance",
            "tests/security",
            "tests/reports",
        ]
        for d in required_dirs:
            assert os.path.isdir(d), f"目录缺失: {d}"
            assert os.path.isfile(os.path.join(d, "__init__.py")), \
                f"__init__.py 缺失: {d}"

    def test_backend_importable(self):
        """验证后端模块可导入。"""
        from backend.app.core.config import Settings
        assert Settings is not None

    def test_pytest_plugins_available(self):
        """验证关键 pytest 插件可用。"""
        plugins = [
            ("pytest_asyncio", "pytest_asyncio"),
            ("pytest_cov", "pytest_cov"),
            ("xdist", "pytest-xdist"),
            ("pytest_timeout", "pytest_timeout"),
        ]
        missing = []
        for import_name, display_name in plugins:
            try:
                __import__(import_name)
            except ImportError:
                missing.append(display_name)
        assert not missing, f"缺失 pytest 插件: {missing}"
