"""项目级常量与入口模块的单元测试。"""

from pathlib import Path

import streamlit as st

from app.app import FEATURE_CARDS, feature_summary, render
from app.core.project_info import APP_NAME, APP_VERSION, PORT, PORT_MAX

DATA_TRAIN = Path(__file__).resolve().parents[1] / "data" / "train.csv"
DATA_TEST = Path(__file__).resolve().parents[1] / "data" / "test.csv"


def test_project_constants_match_requirements() -> None:
    # 需求约束:仓库名/容器名 banksys_lixiaohua,端口 8888(主机 8888~8898 回退)
    assert APP_NAME == "banksys_lixiaohua"
    assert PORT == 8888
    assert PORT_MAX == 8898
    assert PORT <= PORT_MAX


def test_app_version_semver() -> None:
    parts = APP_VERSION.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)


def test_app_entry_defines_render() -> None:
    # 入口必须暴露 render(),由 __main__ 调用;模块可被测试导入
    assert callable(render)


def test_feature_summary_lists_both_features() -> None:
    summary = feature_summary()
    assert len(FEATURE_CARDS) == 2
    assert "数据分析" in summary
    assert "在线预测" in summary


def test_render_uses_project_constants(monkeypatch) -> None:
    # 用假 streamlit 调用录制渲染动作,验证页面使用项目常量(名称/端口)
    recorded: list[tuple[str, dict]] = []

    def fake(*args, **kwargs) -> None:
        recorded.append((str(args), kwargs))

    for name in ("set_page_config", "title", "caption", "write", "markdown", "info"):
        monkeypatch.setattr(st, name, fake)

    render()

    texts = " ".join(str(text) for text, _ in recorded)
    assert APP_NAME in texts
    assert str(PORT) in texts
    assert "银行营销认购预测系统" in texts


def test_train_data_available_in_repo() -> None:
    # 公开教学数据进 Git,保证 CI 干净 runner 与服务器可复现(见 standards/05 排错)
    assert DATA_TRAIN.exists()
    assert DATA_TRAIN.stat().st_size > 0
    assert DATA_TEST.exists()
    assert DATA_TEST.stat().st_size > 0
