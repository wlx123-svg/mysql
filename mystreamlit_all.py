import streamlit as st
import pandas as pd
from datetime import datetime, time
st.title("mystreamlit 简单应用")
tab1, tab2, tab3 , tab4, tab5, tab6= st.tabs(["学生信息管理", "南宁美食记录", "图片展示","视频展示","音频播放","简历生成器"])

with tab1:
    st.title("📝 简易学生信息记录系统")

    st.header("1. 基础信息录入")

    st.text("请填写以下学生基础信息（支持实时预览）")

    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("姓名")
            gender = st.selectbox("性别", ["男", "女", "其他"])
            age = st.number_input("年龄", min_value=10, max_value=25, step=1)
        with col2:
            grade = st.text_input("年级（如：2023级）")
            major = st.text_input("专业（如：计算机科学）")
            score = st.number_input("平均分", min_value=0, max_value=100, step=1)
        
        submit_btn = st.form_submit_button("✅ 添加学生信息", type="primary")

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

    st.header("2. 数据概览")
    total_students = len(st.session_state.student_list)
    avg_score = sum([s["平均分"] for s in st.session_state.student_list])/total_students if total_students > 0 else 0

    # 关键指标展示（metric）
    col1, col2 = st.columns(2)
    with col1:
        st.metric("总记录学生数", total_students, delta=total_students)  # delta显示变化值
    with col2:
        st.metric("学生平均分（整体）", round(avg_score, 1), delta=round(avg_score, 1))

    st.subheader("3. 学生信息列表")
    if st.session_state.student_list:
        # 转换为DataFrame，用table展示
        df = pd.DataFrame(st.session_state.student_list)
        st.table(df)  # 基础表格（也可用st.dataframe，table更轻量化）
    else:
        st.text("暂无学生信息，请先添加！")

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

with tab2:
    st.title("🍝南宁美食数据可视化")
    st.header('🧍‍♂️店铺人流量展示')
    #-------图1---表格
    test={
        '餐厅':['三街两巷唐伯牛烤肉','三个椰子','潮汕牛肉自自助锅','陶鲜生','大叔的虾'],
        '评分':[3.2,4.6,3.8,2.9,4.8],
        '人均消费':[70,65,73,50,60],
        '月份':['01月','02月','03月','04月','05月','06月','07月','08月','09月','10月','11月','12月'],
        }
    data={
        '三街两巷唐伯牛烤肉':[67,500,565,700,123,677,676,566,567,787,345,678],
        '三个椰子':[200,500,565,700,746,676,566,567,787,345,678,567],
        '潮汕牛肉自自助锅':[200,500,565,700,789,676,566,567,787,345,678,567],
        '陶鲜生':[200,500,565,700,798,676,566,567,787,345,678,567],
        '大叔的虾':[200,500,565,700,7,676,566,567,787,345,678,567]
    }
    index=pd.Series(test['月份'],name='月份')
    df=pd.DataFrame(data,index=index)
    st.dataframe(df)
    #------图2----折线图
    st.header('🥐店铺评分')
    test2={
        '评分':test['评分']
        }
    index=pd.Series(test['餐厅'],name='餐厅')
    df2=pd.DataFrame(test2,index=index)
    st.line_chart(df2)
    #------图3---条形图
    st.header('🤠人均销量')
    test2={
        '人均消费':test['人均消费']
        }
    index=pd.Series(test['餐厅'],name='餐厅')
    df2=pd.DataFrame(test2,index=index)
    st.bar_chart(df2)

    #------图4---地图定位
    st.header('🌍地图展示')
    map_data={
        "latitude": [22.813610,22.813610, 22.845949, 22.814264,22.769247],
        "longitude": [108.319567,108.319567,108.322783,108.321350,108.432327]
        }
    mp_df=pd.DataFrame(map_data)
    st.map(mp_df)

with tab3:
    st.set_page_config(page_title='相册',page_icon='😃')
    images=[{'url':'http://seopic.699pic.com/photo/10028/5740.jpg_wh1200.jpg',
             'text':'p1'},
            {'url':'https://img.shetu66.com/2023/07/18/1689659210837955.png',
             'text':'p2'},
            {'url':'https://img-baofun.zhhainiao.com/fs/222d88fd1fb1d2289884bec4b62e60e1.jpg',
             'text':'p3'}
            ]
    st.title('我的相册')
    if 'ind' not in st.session_state:
        st.session_state['ind']=0
    st.image(images[st.session_state['ind']]['url'],caption=images[st.session_state['ind']]['text'])

    def nextImg():
        st.session_state['ind']=(st.session_state['ind']+1) % len(images)
    def pveImg():
        st.session_state['ind']=(st.session_state['ind']-1) % len(images)
        
    c1,c2=st.columns(2)
    with c1:
        st.button('上一张',on_click=pveImg,use_container_width=True)
    with c2:
        st.button('下一张',on_click=nextImg,use_container_width=True)
with tab4:

    # 设置页面标题
    st.title('还珠格格第一部第1集')

    # 视频列表
    video_list = [
        {'url': 'https://www.w3school.com.cn/example/html5/mov_bbb.mp4', 'title': '第一集'},
        {'url': 'https://www.w3schools.com/html/movie.mp4', 'title': '第二集'},
        {'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4', 'title': '第三集'},
        {'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4', 'title': '第四集'},
        {'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4', 'title': '第五集'},
        {'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4', 'title': '第六集'},
        {'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4', 'title': '第七集'},
        {'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4', 'title': '第八集'},
        {'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4', 'title': '第九集'},
        {'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4', 'title': '第十集'},
        {'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4', 'title': '第十一集'},
        {'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4', 'title': '第十二集'}
    ]

    # 初始化会话状态，记录当前播放的索引
    if 'ind' not in st.session_state:
        st.session_state['ind'] = 0

    # 显示当前选中的视频
    st.video(video_list[st.session_state['ind']]['url'], autoplay=True)

    # 定义切换视频的函数
    def play(i):
        st.session_state['ind'] = int(i)

    # 定义每行的列数（3列）和总行数（4行）
    cols_per_row = 3
    total_videos = len(video_list)

    # 循环创建行和列，放置按钮
    for row in range(0, total_videos, cols_per_row):
        # 为当前行创建3个列
        cols = st.columns(cols_per_row)
        # 遍历当前行的每个列，分配对应的视频按钮
        for col_idx in range(cols_per_row):
            # 计算当前视频的索引
            video_idx = row + col_idx
            # 避免索引超出视频列表长度
            if video_idx < total_videos:
                with cols[col_idx]:
                    # 创建按钮，点击时触发play函数
                    st.button(
                        f'第{video_idx + 1}集',
                        use_container_width=True,
                        on_click=play,
                        args=[video_idx]
                    )
with tab5:
    st.set_page_config(page_title='简单音乐播放页面', page_icon='🎵')

    # 图片数据
    images = [
        {
            'audio_url': 'https://music.163.com/song/media/outer/url?id=3322357952.mp3',
            'picurl': 'http://seopic.699pic.com/photo/10028/5740.jpg_wh1200.jpg',
            'name': '晴朗天空',
            'geshou': '朕润泽'
        },
        {
            'audio_url': 'https://music.163.com/song/media/outer/url?id=2746857577.mp3',
            'picurl': 'https://img.shetu66.com/2023/07/18/1689659210837955.png',
            'name': '暮色森林',
            'geshou': '欧阳娜娜'
        },
        {
            'audio_url': 'https://music.163.com/song/media/outer/url?id=3327141886.mp3',
            'picurl': 'https://img-baofun.zhhainiao.com/fs/222d88fd1fb1d2289884bec4b62e60e1.jpg',
            'name': '大东北我的家乡',
            'geshou': '袁娅维'
        }
    ]

    st.title('我的音乐收藏')

    # 初始化索引
    if 'ind' not in st.session_state:
        st.session_state['ind'] = 0

    # 创建1:2比例的列布局
    col1, col2 = st.columns([1, 2])

    # 图片展示区域
    with col1:
        current_img = images[st.session_state['ind']]
        st.image(current_img['picurl'], width=300)
        #st.markdown(f"**{current_img['name']}**\n\n{current_img['geshou']}")

    # 音频和按钮区域
    with col2:
        # 使用空容器动态更新音频
        audio_container = st.empty()
        
        # 显示当前歌曲信息
        st.markdown("#### 正在播放")
        current_song = images[st.session_state['ind']]
        st.markdown(f"**{current_song['name']}** - {current_song['geshou']}")
        
        # 播放当前音频
        audio_container.audio(current_song['audio_url'])
        
        # 导航按钮
        c1, c2 = st.columns(2)
        
        with c1:
            if st.button('上一首', key='prev', use_container_width=True):
                st.session_state['ind'] = (st.session_state['ind'] - 1) % len(images)
                # 手动触发页面刷新（Streamlit限制）
                st.rerun()
        
        with c2:
            if st.button('下一首', key='next', use_container_width=True):
                st.session_state['ind'] = (st.session_state['ind'] + 1) % len(images)
                st.rerun()
with tab6:
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

      
