import streamlit as st
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
