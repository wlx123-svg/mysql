import streamlit as st
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(page_title="数据智能分析平台", layout="wide")

# 导航逻辑处理
st.title("欢迎使用数据智能分析平台")
st.markdown("""
这是一个基于 Streamlit 构建的多页面交互式应用平台，集成了多种实用工具和数据分析功能。
您可以通过下方功能入口访问各个模块，体验不同的应用场景。
""")
st.divider()

# 核心功能模块（分栏展示现有功能）
st.subheader("✨ 功能模块")
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.subheader("🍝 南宁美食数据")
        st.write("展示南宁热门餐厅的人流量、评分及消费数据可视化分析")
        if st.button("进入美食数据页面", use_container_width=True):
            st.switch_page("pages/01_南宁美食数据.py")

with col2:
    with st.container(border=True):
        st.subheader("📄 个人简历生成器")
        st.write("快速创建个性化简历，支持信息填写与实时预览")
        if st.button("进入简历生成器", use_container_width=True):
            st.switch_page("pages/02_个人简历生成器.py")

with col3:
    with st.container(border=True):
        st.subheader("🐾 动物图鉴")
        st.write("浏览动物图片集，支持上下页切换查看")
        if st.button("进入动物图鉴", use_container_width=True):
            st.switch_page("pages/03_动物图鉴.py")

with col4:
    with st.container(border=True):
        st.subheader("🎓 数字档案")
        st.write("学生信息记录系统，支持数据录入与统计分析")
        if st.button("进入数字档案系统", use_container_width=True):
            st.switch_page("pages/04_数字档案.py")

# 数据可视化示例展示
st.subheader("📊 数据可视化示例")
col5, col6 = st.columns(2)

# 生成示例数据
df = pd.DataFrame({
    "日期": pd.date_range(start="2025-01-01", periods=12, freq="M"),
    "销售额": [120, 150, 180, 140, 200, 220, 250, 230, 280, 300, 320, 350],
    "用户数": [500, 600, 750, 650, 800, 900, 1000, 950, 1100, 1200, 1300, 1400]
})

with col5:
    st.subheader("月度销售额趋势")
    st.line_chart(df, x="日期", y="销售额", use_container_width=True)

with col6:
    st.subheader("月度用户增长情况")
    st.bar_chart(df, x="日期", y="用户数", use_container_width=True)

# 系统信息说明
st.divider()
st.subheader("ℹ️ 系统说明")
st.markdown("""
- 本平台包含四个功能模块，可通过上方按钮快速访问
- 所有数据处理均在浏览器端完成，确保信息安全
- 支持在各功能页面内进行交互式操作，实时查看结果
- 技术架构：基于 Python + Streamlit 构建，代码开源可扩展
""")

# 页脚信息
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    © 2025 数据智能分析平台 | 多页面应用展示
</div>
""", unsafe_allow_html=True)
