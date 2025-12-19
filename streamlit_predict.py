import streamlit as st
import pickle
import pandas as pd
import os

def introduce_page():
    """当选择简介页面时，将呈现该函数的内容"""
    st.write("# 欢迎使用！")
    st.sidebar.success("单击“预测医疗费用”")
    
    st.markdown("""  
    # 医疗费用预测应用  
    这个应用利用机器学习模型来预测医疗费用，为保险公司的保险定价提供参考。
    """)
    
    # 背景介绍
    st.markdown("# 背景介绍")
    st.markdown("- 开发目标：帮助保险公司合理定价保险产品，控制风险。")
    st.markdown("- 模型算法：利用随机森林回归算法训练医疗费用预测模型。")
    
    # 使用指南
    st.markdown("## 使用指南")
    st.markdown("- 输入准确完整的被保险人信息，可以得到更准确的费用预测。")
    st.markdown("- 预测结果可以作为保险定价的重要参考，但需审慎决策。")
    st.markdown("- 有任何问题欢迎联系我们的技术支持。")
    
    st.markdown("技术支持: email:: support@example.com")

def predict_page():
    """当选择预测费用页面时，将呈现该函数的内容"""
    st.markdown("""
    ## 使用说明
    这个应用利用机器学习模型来预测医疗费用，为保险公司的保险定价提供参考。
    - **输入信息**：在下面输入被保险人的个人信息、疾病信息等。
    - **费用预测**：应用会预测被保险人的未来医疗费用支出。
    """)
    
    # 检查模型文件是否存在
    if not os.path.exists('rfr_model.pkl'):
        st.error("❌ 模型文件 'rfr_model.pkl' 不存在！")
        st.info("请先运行 `save_model.py` 训练模型")
        return
    
    # 运用表单和表单提交按钮
    with st.form('user_inputs'):
        age = st.number_input('年龄', min_value=0, value=30)
        sex = st.radio('性别', options=['女性', '男性'], index=0)
        bmi = st.number_input('BMI', min_value=0.0, value=25.0)
        children = st.number_input("子女数量:", step=1, min_value=0, value=0)
        smoke = st.radio("是否吸烟", ("否", "是"), index=0)  # 注意顺序：否、是
        region = st.selectbox('区域', ('东南部', '西南部', '东北部', '西北部'), index=0)
        submitted = st.form_submit_button('预测费用')
    
    if submitted:
        # 数据预处理
        sex_female, sex_male = (1, 0) if sex == '女性' else (0, 1)
        smoke_no, smoke_yes = (1, 0) if smoke == '否' else (0, 1)
        
        # 区域编码
        region_northeast = 1 if region == '东北部' else 0
        region_southeast = 1 if region == '东南部' else 0
        region_northwest = 1 if region == '西北部' else 0
        region_southwest = 1 if region == '西南部' else 0
        
        # 注意：特征顺序必须与save_model.py中完全一致
        format_data = [
            age, bmi, children,
            sex_female, sex_male,
            smoke_no, smoke_yes,
            region_northeast, region_northwest, region_southeast, region_southwest
        ]
        
        try:
            # 加载模型
            with open('rfr_model.pkl', 'rb') as f:
                rfr_model = pickle.load(f)
            
            # 创建DataFrame
            if hasattr(rfr_model, 'feature_names_in_'):
                columns = rfr_model.feature_names_in_
            else:
                # 手动指定列名（必须与save_model.py中一致）
                columns = [
                    '年龄', 'BMI', '子女数量',
                    '性别_女', '性别_男',
                    '是否吸烟_否', '是否吸烟_是',
                    '区域_东北部', '区域_西北部', '区域_东南部', '区域_西南部'
                ]
            
            format_data_df = pd.DataFrame([format_data], columns=columns)
            
            # 预测
            predict_result = rfr_model.predict(format_data_df)[0]
            
            # 显示结果
            st.success(f'✅ 预测完成！')
            st.write(f'**根据您输入的数据，预测该客户的医疗费用是：${round(predict_result, 2):,.2f}**')
            
        except Exception as e:
            st.error(f"❌ 预测失败: {str(e)}")
            st.info("可能的原因：")
            st.info("1. 模型文件损坏")
            st.info("2. 特征数量或顺序不匹配")
            st.info("3. 缺少必要的依赖库")
            
            # 显示模拟结果
            st.warning("显示模拟结果（基于简单公式）：")
            predict_result = age * 1000 + bmi * 200 + children * 500
            if smoke == '是':
                predict_result += 5000
            st.write(f'模拟医疗费用：${round(predict_result, 2):,.2f}')
        
        st.write("---")
        st.write("技术支持: email:: support@example.com")

# 设置页面的标题、图标
st.set_page_config(
    page_title="医疗费用预测",
    page_icon="$",
)

# 在左侧添加侧边栏并设置单选按钮
nav = st.sidebar.radio("导航", ["简介", "预测医疗费用"])
# 根据选择的结果，展示不同的页面
if nav == "简介":
    introduce_page()
else:
    predict_page()
