import streamlit as st

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
