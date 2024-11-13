import streamlit as st
import os
from qianfan import Qianfan  # 确保你已经配置好qianfan SDK的访问


client = Qianfan(
 
    # 方式一：使用安全认证AK/SK鉴权
    # 替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk，如何获取请查看https://cloud.baidu.com/doc/Reference/s/9jwvz2egb
    access_key= "access_key",
    secret_key= "secret_key",
    app_id="116214329"

    # 方式二：使用应用BearerToken鉴权
    # 替换下列示例中参数，将your_BearerToken替换为真实值，如何获取请查看https://cloud.baidu.com/doc/IAM/s/Mm2x80phi
    #api_key="your_BearerToken" 
    #app_id="", # 选填，不填写则使用默认appid
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
    
    # 向模型发送请求
    completion = client.chat.completions.create(
        model="ERNIE-Speed-128K",
        messages=st.session_state.messages
    )
    
    # 获取助手回复并添加到对话历史中
    assistant_reply = completion.choices[0].message.content
    st.session_state.messages.append({'role': 'assistant', 'content': assistant_reply})

# 显示对话历史
for msg in st.session_state.messages:
    if msg['role'] == 'user':
        st.write(f"**用户:** {msg['content']}")
    elif msg['role'] == 'assistant':
        st.write(f"**助手:** {msg['content']}")
