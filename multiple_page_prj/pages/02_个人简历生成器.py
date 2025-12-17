import streamlit as st
from datetime import datetime, time

# 页面配置
st.set_page_config(page_title='个人简历生成器', layout='wide')
st.title('📄 个人简历生成器')

# 分左右两列布局
c1, c2 = st.columns([1, 2])

# 左侧：信息填写区域
with c1:
    st.subheader('👤 基本信息填写')
    
    # 基础文本输入
    user_name = st.text_input('姓名', placeholder='请输入您的姓名')
    user_employ = st.text_input('应聘职位', placeholder='请输入应聘职位')
    user_phone = st.text_input('联系电话', placeholder='请输入手机号码')
    user_email = st.text_input('电子邮箱', placeholder='请输入邮箱地址')
    
    # 生日选择（日期组件）
    user_bir = st.date_input(
        '出生日期',
        value=datetime(1990, 1, 1),
        min_value=datetime(1950, 1, 1),
        max_value=datetime.now(),
        format='YYYY-MM-DD'
    )
    
    # 性别单选框
    user_sex = st.radio('性别', options=['男', '女', '保密'], horizontal=True)
    
    # 学历下拉选择框
    user_xueli = st.selectbox(
        '学历',
        options=['小学', '初中', '高中/中专', '大专', '本科', '硕士', '博士', '其他']
    )
    
    # 掌握语言多选框
    user_lange = st.multiselect(
        '掌握语言',
        options=['中文', '英语', '日语', '韩语', '法语', '德语', '西班牙语', '其他'],
        default=['中文']
    )
    
    # 专业技能多选框
    user_skill = st.multiselect(
        '专业技能',
        options=['Python', 'Java', 'JavaScript', 'SQL', '数据分析', 'UI设计', '项目管理', 
                '市场营销', '财务分析', '人力资源管理', '其他'],
        placeholder='请选择掌握的技能'
    )
    
    # 工作经验滑块
    user_exp = st.slider('工作经验（年）', min_value=0, max_value=40, value=0, step=1)
    
    # 期望薪资滑块（范围选择）
    user_money = st.slider(
        '期望薪资范围（元/月）',
        min_value=5000,
        max_value=100000,
        value=(10000, 20000),
        step=1000
    )
    
    # 个人简介文本域
    user_detail = st.text_area(
        '个人简介',
        placeholder='请简要介绍您的工作经历、专业能力、职业规划等（不少于50字）',
        height=150
    )
    
    # 最佳联系时间
    user_best_ass = st.time_input(
        '每日最佳联系时间',
        value=time(14, 0),
        step=3600  # 步长1小时
    )
    
    # 上传个人照片
    user_photo = st.file_uploader(
        '上传个人照片',
        type=['jpg', 'png', 'jpeg'],
        help='请上传清晰的正面照，大小不超过5MB'
    )
    
    # 生成简历按钮（仅用于触发下载）
    generate_btn = st.button('📋 生成并下载简历', type='primary')

# 右侧：简历预览区域（实时更新）
with c2:
    st.subheader('📄 简历预览')
    
    # 简历卡片布局（实时显示已填写内容）
    with st.container(border=True):
        # 简历头部（照片+基本信息）
        preview_col1, preview_col2 = st.columns([1, 4])
        
        with preview_col1:
            # 默认头像，用户上传后更新
            if user_photo:
                st.image(user_photo, width=120, caption=user_name if user_name else "未填写姓名")
            else:
                st.image('https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png', 
                         width=120, caption="请上传照片")
        
        with preview_col2:
            # 姓名和应聘职位
            name_part = f"### {user_name}" if user_name else "### 请填写姓名"
            employ_part = f" | {user_employ}" if user_employ else ""
            st.markdown(f"{name_part}{employ_part}")
            
            # 实时显示已填写的信息项
            if user_xueli:
                st.markdown(f"- 🎓 学历：{user_xueli}")
            if user_bir:
                st.markdown(f"- 🎂 出生日期：{user_bir.strftime('%Y年%m月%d日')}")
            if user_sex:
                st.markdown(f"- 🚻 性别：{user_sex}")
            if user_phone:
                st.markdown(f"- 📞 电话：{user_phone}")
            if user_email:
                st.markdown(f"- 📧 邮箱：{user_email}")
            if user_best_ass:
                st.markdown(f"- 🕒 最佳联系时间：{user_best_ass.strftime('%H:%M')}")
            if user_exp is not None:
                st.markdown(f"- 💼 工作经验：{user_exp}年")
            if user_money:
                st.markdown(f"- 💰 期望薪资：{user_money[0]} - {user_money[1]} 元/月")
    
    # 技能部分（实时显示）
    with st.container(border=True):
        st.markdown("### 🛠️ 专业技能")
        if user_skill:
            st.write(' | '.join(user_skill))
        else:
            st.write('未填写')
        
        st.markdown("### 🗣️ 掌握语言")
        if user_lange:
            st.write(' | '.join(user_lange))
        else:
            st.write('未填写')
    
    # 个人简介部分（实时显示）
    with st.container(border=True):
        st.markdown("### 📝 个人简介")
        if user_detail:
            st.write(user_detail)
        else:
            st.write('未填写')
    
    # 下载功能（保持不变）
    if generate_btn:
        if not user_name or not user_phone or not user_email:
            st.error('⚠️ 姓名、联系电话、电子邮箱为必填项，请补充完整！')
        else:
            resume_text = f"""
            个人简历
            ==========
            姓名：{user_name}
            应聘职位：{user_employ if user_employ else '未填写'}
            学历：{user_xueli}
            出生日期：{user_bir.strftime('%Y年%m月%d日')}
            性别：{user_sex}
            联系电话：{user_phone}
            电子邮箱：{user_email}
            最佳联系时间：{user_best_ass.strftime('%H:%M')}
            工作经验：{user_exp}年
            期望薪资：{user_money[0]} - {user_money[1]} 元/月
            
            掌握语言：{','.join(user_lange) if user_lange else '暂无'}
            专业技能：{','.join(user_skill) if user_skill else '暂无'}
            
            个人简介：
            {user_detail if user_detail else '暂无'}
            """
            
            st.download_button(
                label='📥 下载简历（纯文本）',
                data=resume_text,
                file_name=f'{user_name}_简历.txt',
                mime='text/plain'
            )

# 页脚信息
st.markdown("---")
st.caption('© 2025 个人简历生成器 | 使用 Streamlit 构建')
