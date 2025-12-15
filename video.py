import streamlit as st

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
