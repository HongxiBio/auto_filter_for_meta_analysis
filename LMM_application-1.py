import time
import streamlit as st
from qianfan import Qianfan  # Make sure you have configured the qianfan SDK access

# Initialize the Qianfan client
client = Qianfan(
    access_key= "5a1d5bfe6e6f4a138caa443e66c4f29f",
    secret_key= "060ea48e515b493fbd67021d2f5c46d7",
    app_id="116214329"
)

# 初始化对话上下文
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': '聊天助手'}]

# 标题
st.title("智能助手对话")

# 用户输入
user_input = st.text_input("请输入你的消息:")

# 处理用户输入
if user_input:
    # 将用户输入添加到对话历史中
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    
    # 初始化一个流式显示区域
    assistant_reply_display = st.empty()
    current_reply = ""

    # 向模型发送请求，设置流模式为True
    response = client.chat.completions.create(
        model="ERNIE-Speed-128K",
        messages=st.session_state.messages,
        stream=True
    )
    
    time.sleep(3)
    
    # 逐步接收流式数据并显示
    for chunk in response:
        chunk_content = chunk['choices'][0]['delta'].get('content', '')
        current_reply += chunk_content
        assistant_reply_display.markdown(f"**助手:** {current_reply}")

    # 将最终回复添加到对话历史中
    st.session_state.messages.append({'role': 'assistant', 'content': current_reply})

# 显示对话历史
for msg in st.session_state.messages:
    if msg['role'] == 'user':
        st.write(f"**用户:** {msg['content']}")
    elif msg['role'] == 'assistant':
        st.write(f"**助手:** {msg['content']}")