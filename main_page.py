import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pickle  
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# 全局配置
st.set_page_config(
    page_title="学生成绩分析与预测系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 中文显示配置
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False

# 读取CSV文件里的数据
@st.cache_data
def load_real_data():
    try:

        raw_cols = [
            "学号", "性别", "专业", "每周学习时长（小时）", 
            "上课出勤率", "期中考试分数", "作业完成率", "期末考试分数"
        ]
        # 读取真实数据文件（必须确保该文件存在于运行目录）
        df = pd.read_csv("student_data_adjusted_rounded.csv")
        
        # 检查列名是否匹配
        missing_cols = [col for col in raw_cols if col not in df.columns]
        if missing_cols:
            st.error(f"❌ CSV文件缺少列：{', '.join(missing_cols)}")
            st.stop()
        
        # 仅保留需要的列
        df = df[raw_cols].copy()
        
        # 1. 专业性别比例汇总
        gender_ratio = df.groupby("专业")["性别"].value_counts(normalize=True).unstack(fill_value=0)
        if "男" not in gender_ratio.columns: gender_ratio["男"] = 0.0
        if "女" not in gender_ratio.columns: gender_ratio["女"] = 0.0
        gender_ratio = gender_ratio.rename(columns={"男": "男生比例", "女": "女生比例"}).reset_index()
        
        # 2. 专业学习指标汇总
        major_agg = df.groupby("专业").agg({
            "每周学习时长（小时）": "mean",
            "上课出勤率": "mean",
            "期中考试分数": "mean",
            "期末考试分数": "mean",
            "作业完成率": "mean"
        }).reset_index()
        
        major_df = pd.merge(gender_ratio, major_agg, on="专业", how="inner")
         
        major_df = major_df.rename(columns={
            "每周学习时长（小时）": "每周平均学时",
            "期中考试分数": "期中考试平均分",
            "期末考试分数": "期末考试平均分",
            "上课出勤率": "平均出勤率",
            "作业完成率": "作业完成率"
        })
        
        # 训练数据
        train_df = df.dropna().copy()
        
        return major_df, train_df, df  # 返回原始df用于展示原始列名数据
    
    except FileNotFoundError:
        st.error("❌ 未找到 student_data_adjusted_rounded.csv 文件，请检查文件是否在运行目录下！")
        st.stop()
    except Exception as e:
        st.error(f"❌ 数据读取失败：{str(e)}")
        st.stop()

# 加载真实数据
major_df, train_df, raw_df = load_real_data()

# 侧边栏导航 
st.sidebar.title("导航菜单")
page = st.sidebar.radio(
    "",
    ["项目介绍", "专业数据分析", "成绩预测"],
    index=0
)

# 项目介绍页面 
if page == "项目介绍":
    st.title("📚 学生成绩分析与预测系统")
    st.divider()
    col1, col2 = st.columns([0.5, 0.5])
    st.divider()
    with col1:
        st.markdown("## 📋 项目概述")  # 用 Markdown 二级标题
        st.write("本项目是一个基于 Streamlit 的学生成绩分析平台，通过数据可视化和机器学习技术，帮助教育工作者和学生深入了解学业表现，并预测期末考试成绩。")
        st.markdown("## ✨ 主要特点")  # 用 Markdown 二级标题代替
        st.write("""
        - 📊 **数据可视化**：多维度展示学生学业数据
        - 🎯 **专业分析**：按专业分类的详细统计分析
        - 🤖 **智能预测**：基于机器学习模型的成绩预测
        - 💡 **学习建议**：根据预测结果提供个性化反馈
        """)
    
    with col2:
        st.image(
            "images/图片1.png",
            caption="学生数据分析示意图",
            use_container_width=True
        )
    
    st.markdown("## 🎯 项目目标")
    col_target1, col_target2, col_target3 = st.columns(3)
    with col_target1:
        st.markdown("### 🎯目标一: 分析影响因素")
        st.write("""- 识别关键学习指标\n- 探索成绩相关因素\n- 提供数据支撑决策""")
    with col_target2:
        st.markdown("### 🎯目标二:可视化展示")
        st.write("""- 专业对比分析\n- 性别差异研究\n- 学习模式识别""")
    with col_target3:
        st.markdown("### 🎯目标三:成绩预测")

        st.write("""- 机器学习建模\n- 个性化预测\n- 及时干预预警""")
    st.divider()
    st.markdown("## ⚙️ 技术架构")
    col_tech1, col_tech2, col_tech3, col_tech4 = st.columns(4)
    with col_tech1:
        st.write("**前端框架:** Streamlit")
    with col_tech2:
        st.write("**数据处理：** Pandas、nNumPy")
    with col_tech3:
        st.write("**可视化：** Plotly、Matplotlib")
    with col_tech4:
        st.write("**机器学习：** Scikit-learn")

        
# 专业数据分析页面 
elif page == "专业数据分析":
    st.title("📈 专业数据分析")
    
    # 模块1：各专业男女性别比例
    st.subheader("1. 各专业男女性别比例")
    col1_1, col1_2 = st.columns([0.7, 0.3])
    
    with col1_1:
        fig1 = px.bar(
            major_df,
            x="专业",
            y=["男生比例", "女生比例"],
            barmode="group",
            labels={"value": "比例", "variable": "性别"},
            title="各专业性别比例分布",
            color_discrete_map={"男生比例": "#1E88E5", "女生比例": "#0D47A1"}
        )
        fig1.update_layout(
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02
            )
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col1_2:
        st.write("**性别比例数据**")
        gender_data = major_df[["专业", "男生比例", "女生比例"]].round(4)
        gender_data = gender_data.rename(columns={"男生比例": "男", "女生比例": "女"})
        st.dataframe(gender_data, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # 模块2：各专业学习指标对比
    st.subheader("2. 各专业学习指标对比")
    col2_1, col2_2 = st.columns([0.7, 0.3])
    
    with col2_1:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=major_df["专业"],
            y=major_df["每周平均学时"],
            name="平均学习时间",
            marker_color="#81D4FA",
            yaxis="y1"
        ))
        fig2.add_trace(go.Scatter(
            x=major_df["专业"],
            y=major_df["期中考试平均分"],
            name="平均期中成绩",
            mode="lines+markers",
            line=dict(color="#FF9800", width=2),
            marker=dict(size=6),
            yaxis="y2"
        ))
        fig2.add_trace(go.Scatter(
            x=major_df["专业"],
            y=major_df["期末考试平均分"],
            name="平均期末成绩",
            mode="lines+markers",
            line=dict(color="#4CAF50", width=2),
            marker=dict(size=6),
            yaxis="y2"
        ))
        fig2.update_layout(
            title="各专业平均学习时间与成绩对比",
            xaxis_title="专业",
            yaxis=dict(
                title=dict(text="平均学习时间（小时）", font=dict(color="#81D4FA")),
                tickfont=dict(color="#81D4FA"),
                range=[0, 30]
            ),
            yaxis2=dict(
                title=dict(text="平均分（分数）", font=dict(color="#4CAF50")),
                tickfont=dict(color="#4CAF50"),
                overlaying="y",
                side="right",
                range=[70, 90]
            ),
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1.06,
                xanchor="left",
                x=0,
            ),
            barmode="group",
            margin=dict(l=50, r=100, t=50, b=50)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2_2:
        st.write("**详细数据**")
        score_data = major_df[["专业", "每周平均学时", "期中考试平均分", "期末考试平均分"]].round(1)
        score_data = score_data.rename(columns={
            "每周平均学时": "每周学习时长（小时）",
            "期中考试平均分": "期中考试分数",
            "期末考试平均分": "期末考试分数"
        })
        st.dataframe(score_data, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # 模块3：各专业出勤率分析
    st.subheader("3. 各专业出勤率分析")
    col3_1, col3_2 = st.columns([0.7, 0.3])
    
    with col3_1:
        fig3 = px.bar(
            major_df,
            x="专业",
            y="平均出勤率",
            title="各专业平均出勤率",
            color="平均出勤率",
            color_continuous_scale=px.colors.sequential.YlGnBu
        )
        fig3.update_layout(
            coloraxis_colorbar=dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02
            )
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col3_2:
        st.write("**出勤率排名**")
        attendance_ranking = major_df[["专业", "平均出勤率"]].sort_values("平均出勤率", ascending=False)
        attendance_ranking["平均出勤率"] = attendance_ranking["平均出勤率"].apply(lambda x: f"{x:.2%}")
        attendance_ranking["排名"] = range(1, len(attendance_ranking)+1)
        attendance_ranking = attendance_ranking.rename(columns={"平均出勤率": "上课出勤率"})
        attendance_ranking = attendance_ranking[["排名", "专业", "上课出勤率"]]
        st.dataframe(attendance_ranking, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # 模块4：大数据管理专业专项分析
    st.subheader("4. 大数据管理专业专项分析")
    bigdata_raw = raw_df[raw_df["专业"].str.contains("大数据", na=False)].copy()
    bigdata_mask = major_df["专业"].str.contains("大数据", na=False)
    
    if bigdata_mask.any() and not bigdata_raw.empty:
        bigdata_df = major_df[bigdata_mask].iloc[0]
        
        # 指标卡片
        col4_1, col4_2, col4_3, col4_4 = st.columns(4)
        with col4_1:
            st.write("平均出勤率")
            st.metric(label="", value=f"{bigdata_df['平均出勤率']:.1%}", delta=None)
        with col4_2:
            st.write("平均期末分数")
            st.metric(label="", value=f"{bigdata_df['期末考试平均分']:.1f}分", delta=None)
        with col4_3:
            pass_rate = (bigdata_raw["期末考试分数"] >= 60).mean()
            st.write("通过率")
            st.metric(label="", value=f"{pass_rate:.1%}", delta=None)
        with col4_4:
            st.write("平均学习时长")
            st.metric(label="", value=f"{bigdata_df['每周平均学时']:.1f}小时", delta=None)
        
        # 专项图表
        col4_5, col4_6 = st.columns(2)
        with col4_5:
            fig4 = px.histogram(
                bigdata_raw,
                x="期末考试分数",
                title="大数据管理专业期末成绩分布",
                color_discrete_sequence=["#1E88E5"],
                nbins=20
            )
            fig4.update_layout(xaxis_title="期末考试分数", yaxis_title="count", margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig4, use_container_width=True)
        
        with col4_6:
            fig5 = px.box(
                bigdata_raw,
                y="每周学习时长（小时）",
                title="大数据管理专业学习时长分布",
                color_discrete_sequence=["#1E88E5"]
            )
            fig5.update_layout(yaxis_title="每周学习时长（小时）", xaxis_visible=False, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig5, use_container_width=True)
        

# 成绩预测页面
elif page == "成绩预测":
    st.title("🔮 期末成绩预测")
    st.write("请输入学生的学习信息，系统将预测其期末成绩并提供学习建议")
    
    # 表单布局
    with st.form("predict_form", clear_on_submit=False):
        col_left, col_right = st.columns(2)
        
        with col_left:
            student_id = st.text_input("学号", placeholder="例如：123456")
            gender = st.selectbox("性别", ["", "男", "女"], index=0)
            major_list = [""] + major_df["专业"].dropna().unique().tolist()
            major = st.selectbox("专业", major_list, index=0)
        
        with col_right:
            study_hours = st.slider("每周学习时长(小时)", 0, 50, 0, 1)
            attendance_slider = st.slider("上课出勤率(%)", 0, 100, 0, 1)
            mid_score = st.slider("期中考试分数", 0, 100, 0, 1)
            homework_slider = st.slider("作业完成率(%)", 0, 100, 0, 1)
        
        submit_btn = st.form_submit_button("预测期末成绩", type="primary")
    
    if submit_btn:
        if not student_id or gender == "" or major == "":
            st.error("❌ 请填写完整的学号、性别、专业信息！")
        else:
            try:
                # 加载保存的模型
                with open('score_model.pkl', 'rb') as f:
                    model = pickle.load(f)
                
                # 准备输入特征
                input_features = {
                    '每周学习时长（小时）': study_hours,
                    '上课出勤率': attendance_slider / 100.0,
                    '作业完成率': homework_slider / 100.0,
                    '期中考试分数': mid_score
                }
                
                # 转换为模型需要的DataFrame格式
                input_df = pd.DataFrame([input_features])
                
                # 预测并修正范围
                pred_score = model.predict(input_df)[0]
                pred_score = np.clip(pred_score, 0, 100)
                
                # 成绩等级评估
                if pred_score < 60:
                    grade = "不及格"
                    grade_desc = "需要紧急提升"
                elif 60 <= pred_score < 80:
                    grade = "及格"
                    grade_desc = "表现合格，仍有提升空间"
                elif 80 <= pred_score < 90:
                    grade = "良好"
                    grade_desc = "表现不错，继续保持"
                else:
                    grade = "优秀"
                    grade_desc = "表现优异，值得称赞"
                
                #  匹配图片的展示布局 
                st.subheader("预测结果")
                # 1. 预测分数
                st.metric("预测期末成绩:", f"{pred_score:.1f}分")
                
                
                # 3. 对应等级的图片
                if grade == "优秀":
                    st.image(
                        "images/优秀.png", 
                        caption="Congratulations!",
                        
                    )
                elif grade == "良好":
                    st.image(
                        "images/良好.png",
                        caption="做得不错！继续保持",
                       
                    )
                elif grade == "及格":
                    st.image(
                        "images/及格.png",
                        caption="合格通过，仍需努力",
                        
                    )
                else:
                    st.image(
                        "images/不及格.png",
                        caption="需要加油！提升成绩",
                        
                    )
                
                # 4. 分级学习建议
                if grade == "不及格":
                    st.warning("⚠️ 你的成绩不及格，需要重点提升学习表现！")
                    st.write(f"""
                    💡 学习建议：
                    1. 大幅增加每周学习时长（当前{study_hours}小时，建议≥25小时）；
                    2. 务必提高上课出勤率（当前{attendance_slider}%，建议≥95%）；
                    3. 系统复习期中考试内容（当前{mid_score}分）；
                    4. 确保100%完成作业（当前{homework_slider}%）。
                    """)
                elif grade == "及格":
                    st.info("ℹ️ 你的成绩及格，但有较大提升空间！")
                    st.write(f"""
                    💡 学习建议：
                    1. 适当增加学习时长（当前{study_hours}小时，建议≥20小时）；
                    2. 保持较高出勤率（当前{attendance_slider}%，建议≥90%）；
                    3. 针对性复习期中考试薄弱环节；
                    4. 提高作业完成质量（当前{homework_slider}%）。
                    """)
                elif grade == "良好":
                    st.success("✅ 你的成绩良好，继续保持！")
                    st.write(f"""
                    💡 学习建议：
                    1. 维持当前学习时长（当前{study_hours}小时）；
                    2. 保持出勤稳定性；
                    3. 重点攻克难点知识，向优秀冲刺；
                    4. 保持作业高质量完成。
                    """)
                else:  # 优秀
                    st.balloons()
                    st.success("🏆 你的成绩优异，值得表扬！")
                    st.write(f"""
                    💡 学习建议：
                    1. 保持当前高效的学习节奏；
                    2. 可以尝试拓展相关领域知识；
                    3. 适当帮助同学共同进步；
                    4. 注意劳逸结合，保持良好状态。
                    """)
                    
            except FileNotFoundError:
                st.error("❌ 未找到模型文件 score_model.pkl，请先运行save_score_model.py生成模型")
            except Exception as e:
                st.error(f"❌ 预测出错：{str(e)}")
