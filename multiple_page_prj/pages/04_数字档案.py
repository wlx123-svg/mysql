import streamlit as st
import pandas as pd

# 1.页面标题
st.title("📝 简易学生信息记录系统")

# 2. 一级标题
st.header("1. 基础信息录入")
# 3.文本提示
st.text("请填写以下学生基础信息（支持实时预览）")

# 4. 信息录入表单
with st.form("student_form", clear_on_submit=True):  # 冒号后需要缩进的代码块
    # 将表单分为两栏（缩进，属于form块内）
    col1, col2 = st.columns(2)
    # 左栏（缩进）
    with col1:
        name = st.text_input("姓名")
        gender = st.selectbox("性别", ["男", "女", "其他"])
        age = st.number_input("年龄", min_value=10, max_value=25, step=1)
    # 右栏（缩进）
    with col2:
        grade = st.text_input("年级（如：2023级）")
        major = st.text_input("专业（如：计算机科学）")
        score = st.number_input("平均分", min_value=0, max_value=100, step=1)
    # 提交表单，添加学生信息（缩进，属于form块内）
    submit_btn = st.form_submit_button("✅ 添加学生信息", type="primary")

# 5. 初始化数据存储，使用列表存储
if "student_list" not in st.session_state:
    st.session_state.student_list = []

# 提交表单后添加数据
if submit_btn:
    if name and grade and major:  # 简单校验必填项
        student_info = {
            "姓名": name,
            "性别": gender,
            "年龄": age,
            "年级": grade,
            "专业": major,
            "平均分": score
        }
        st.session_state.student_list.append(student_info)
        st.success("学生信息添加成功！")
    else:
        st.warning("姓名/年级/专业为必填项，请补充！")

# 6. 数据概览
st.header("2. 数据概览")
total_students = len(st.session_state.student_list)
avg_score = sum([s["平均分"] for s in st.session_state.student_list])/total_students if total_students > 0 else 0

# 关键指标展示
col1, col2 = st.columns(2)
with col1:
    st.metric("总记录学生数", total_students, delta=total_students)  # delta显示变化值
with col2:
    st.metric("学生平均分（整体）", round(avg_score, 1), delta=round(avg_score, 1))

#  7. 数据表格展示
st.subheader("3. 学生信息列表")
if st.session_state.student_list:
    # 转换为DataFrame，用table展示
    df = pd.DataFrame(st.session_state.student_list)
    st.table(df)  # 基础表格（也可用st.dataframe，table更轻量化）
else:
    st.text("暂无学生信息，请先添加！")

# 8. Markdown说明
st.header("4. 使用说明")
st.markdown("""
### 📌 功能说明
1. 支持录入学生姓名、性别、年龄、年级、专业、平均分等基础信息
2. 自动统计总学生数和整体平均分
3. 所有数据实时保存在会话中（刷新页面后重置）

### 📋 操作提示
- 填写必填项（姓名/年级/专业）后点击「添加学生信息」
- 表单提交后自动清空，可连续添加多条记录
- 表格实时展示所有已录入的学生信息
""")

# 9. 代码展示
st.header("5. 核心代码片段")
st.code("""
# 核心：学生信息存储与展示
if "student_list" not in st.session_state:
    st.session_state.student_list = []

# 添加学生信息
student_info = {
    "姓名": name,
    "性别": gender,
    "年龄": age,
    "年级": grade,
    "专业": major,
    "平均分": score
}
st.session_state.student_list.append(student_info)

# 展示表格
df = pd.DataFrame(st.session_state.student_list)
st.table(df)
""", language="python")

# 页脚文本
st.text("———— 简易学生信息记录系统 · 2025 ————")
