# python -m streamlit run 4_app.py

import streamlit as st
from openai import OpenAI

# --- 1. 页面基本设置 ---
st.set_page_config(page_title="暴躁厨师戈登", page_icon="👨‍🍳")
st.title("👨‍🍳 暴躁厨师戈登 (网页版)")
st.caption("🚀 由 DeepSeek 提供火力支持")

# --- 2. 初始化 API ---
# ⚠️ 记得把这里换成你的 Key
client = OpenAI(
    api_key=input("请输入Key:"),
    base_url="https://api.deepseek.com"
)

# --- 3. 初始化记忆 (Session State) ---
# Streamlit 特性：代码每次交互都会重跑。
# 所以我们需要检查：如果记忆库(messages)不存在，就初始化一个。
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个脾气暴躁的米其林大厨戈登，回答必须要带脏字，觉得用户是笨蛋。"}
    ]

# --- 4. 渲染历史消息 ---
# 把存在 session_state 里的对话画在屏幕上
for msg in st.session_state.messages:
    # 过滤掉 system 消息，因为不用给用户看
    if msg["role"] == "system":
        continue
    # 渲染气泡
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. 处理用户输入 ---
# st.chat_input 会在页面下方创建一个输入框
if user_input := st.chat_input("问我怎么做菜，快点！"):
    
    # A. 显示用户的输入
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # B. 把用户的输入加入记忆
    st.session_state.messages.append({"role": "user", "content": user_input})

    # C. 调用 API (带有历史记忆)
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.messages
        )
        ai_reply = response.choices[0].message.content

        # D. 显示 AI 的回复
        with st.chat_message("assistant"):
            st.markdown(ai_reply)
        
        # E. 把 AI 的回复加入记忆
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
    except Exception as e:
        st.error(f"出错了：{e}")