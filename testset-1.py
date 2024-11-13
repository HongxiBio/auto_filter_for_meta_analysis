import os
import qianfan
import streamlit as st
import time

# Set up authentication for Qianfan API
os.environ["QIANFAN_ACCESS_KEY"] = "5a1d5bfe6e6f4a138caa443e66c4f29f"  # Replace with your actual AK
os.environ["QIANFAN_SECRET_KEY"] = "060ea48e515b493fbd67021d2f5c46d7"  # Replace with your actual SK

# Initialize the Qianfan ChatCompletion object
chat_comp = qianfan.ChatCompletion()

# Streamlit setup
st.title("生信科研助手")
st.write("A test for LLM API")

# Create a placeholder for the chat response (empty initially)
response_placeholder = st.empty()

# 初始化对话上下文
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 用户输入框（放在最下面）
user_input = st.chat_input("请输入你的消息:", key='user_input')

# 显示对话历史
for msg in st.session_state.messages:
    if msg['role'] == 'user':  # 如果是用户输入
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 10px;">
            <div style="margin-right: 10px;">
                <b>用户</b>
            </div>
            <div style="background-color: #f0f0f5; padding: 10px; border-radius: 15px; max-width: 90%; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                {msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif msg['role'] == 'assistant':  # 如果是助手回应
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; align-items: center; margin-bottom: 10px;">
            <div style="margin-left: 10px;">
                <b>助手</b>
            </div>
            <div style="background-color: #dfe8cc; padding: 10px; border-radius: 15px; max-width: 90%; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                {msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# 流式显示助手回应（动态创建占位符）
if user_input:
    # 将用户输入添加到对话历史中
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
        <div style="background-color: #f0f0f5; padding: 10px; border-radius: 15px; max-width: 90%; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            <b>用户:</b> {user_input}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 创建一个动态占位符，用于显示助手的流式响应
    response_placeholder = st.empty()
    sentence = ""  # 用于累积助手的流式响应

    # 向模型发送请求并获取流式响应
    resp = chat_comp.do(
        model="ERNIE-Speed-128K",
        stream=True,
        system="你是一个专业的生命科学和生物信息学的科研助手，能够提供用户准确且简洁的信息",
        messages=st.session_state.messages
    )

    # 实时展示助手的流式回应
    for r in resp:
        if "body" in r and "result" in r["body"]:
            # 获取当前流式响应的部分内容
            result_content = r["body"]["result"]

            # 更新累积的回答内容
            sentence += result_content

            # 实时更新占位符中的内容（以 Markdown 格式显示）
            response_placeholder.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                <div style="background-color: #dfe8cc; padding: 10px; border-radius: 15px; max-width: 90%; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                    <b>助手:</b> {sentence}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 小延时避免过快更新（可以根据需求调整）
            time.sleep(0.1)

    # 完成后，将完整的助手回复添加到对话历史
    st.session_state.messages.append({'role': 'assistant', 'content': sentence})