import pytest
import os
import sys

# 添加 src 目錄到 Python 路徑，確保可以導入模組
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture(scope="session")
def test_data_dir():
    """提供測試數據目錄路徑"""
    return os.path.join(os.path.dirname(__file__), 'data')

# 配置 pytest-html 報告的自定義信息
def pytest_html_report_title(report):
    """自定義 HTML 報告標題"""
    report.title = "中國象棋引擎測試報告"

def pytest_html_results_summary(prefix, summary, postfix):
    """自定義 HTML 報告摘要"""
    prefix.extend([
        "<h2>測試概覽</h2>",
        "<p>此報告包含中國象棋引擎的完整測試結果，涵蓋：</p>",
        "<ul>",
        "<li>ChessEngine 核心功能測試</li>",
        "<li>各棋子移動驗證器測試</li>", 
        "<li>遊戲規則與邏輯測試</li>",
        "<li>OCP 原則遵循驗證</li>",
        "</ul>"
    ])

def pytest_configure(config):
    """配置 pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )

# 測試用例標記
def pytest_collection_modifyitems(config, items):
    """根據測試名稱自動添加標記"""
    for item in items:
        # 為測試添加適當的標記
        if "test_chess_engine" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "test_move_validators" in item.nodeid:
            item.add_marker(pytest.mark.unit) 