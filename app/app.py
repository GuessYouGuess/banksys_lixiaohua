"""banksys_lixiaohua 应用入口。

运行:streamlit run app/app.py
入口只负责页面渲染,业务逻辑全部在 app/core/ 下(纯函数,可单测)。
"""

import streamlit as st

from app.core.project_info import APP_NAME, APP_VERSION, PORT, PORT_MAX

# 主页面功能卡片:纯数据,可单测
FEATURE_CARDS = [
    ("数据分析", "交互式浏览、筛选、可视化客户特征与认购关系"),
    ("在线预测", "点选客户特征,预测是否认购及概率"),
]


def feature_summary() -> str:
    """生成功能列表摘要文本。"""
    return "\n".join(f"- **{name}**:{desc}" for name, desc in FEATURE_CARDS)


def render() -> None:
    """渲染主页面:项目导航与概览。"""
    st.set_page_config(page_title=APP_NAME, page_icon="🏦", layout="wide")
    st.title(f"🏦 {APP_NAME}")
    st.caption(f"v{APP_VERSION} · 银行营销认购预测系统")
    st.write("本项目基于银行电话营销数据集,提供两个功能页面:")
    st.markdown(feature_summary())
    st.info(f"服务端口:{PORT}(容器内固定,主机 {PORT}~{PORT_MAX} 回退)")


if __name__ == "__main__":
    render()
