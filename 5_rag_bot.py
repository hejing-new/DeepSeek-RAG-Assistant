# python -m streamlit run 5_rag_bot.py

import streamlit as st
from openai import OpenAI
import PyPDF2  # 专门用来读 PDF 的库

# --- 1. 页面设置 ---
st.set_page_config(page_title="我的私有知识库助手", layout="wide")
st.title("📚 私有文件问答助手 (RAG Demo)")
st.caption("上传 PDF，DeepSeek 帮你读！")

# --- 2. 侧边栏：上传文件 ---
with st.sidebar:
    st.header("📂 第一步：上传文件")
    uploaded_file = st.file_uploader("请上传一个 PDF 文件", type=["pdf"])
    
    # 填入 Key (你可以写死在这里，或者在网页侧边栏输入)
    api_key = st.text_input("请输入 DeepSeek API Key", type="password", value="sk-这里填你的Key")

# --- 3. 初始化 DeepSeek ---
client = OpenAI(
    api_key=input("请输入Key:"),
    base_url="https://api.deepseek.com"
)

# 初始化 Session State (记忆)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_content" not in st.session_state:
    st.session_state.file_content = ""

# --- 4. 核心逻辑：读取 PDF ---
if uploaded_file and st.session_state.file_content == "":
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        # 一页一页把字抠出来拼在一起
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # 存到记忆里
        st.session_state.file_content = text
        st.success(f"✅ 文件读取成功！共 {len(text)} 个字。现在可以提问了。")
        
    except Exception as e:
        st.error(f"读取失败：{e}")

# --- 5. 显示聊天界面 ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. 处理提问 (RAG 的精髓在这里) ---
if user_input := st.chat_input("关于这个文件，你想问什么？"):
    
    # A. 显示用户问题
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # B. 构造“作弊小抄” (Prompt Engineering)
    # 我们把 PDF 的内容偷偷塞给 AI，告诉它：“必须根据下面这段话回答”
    # 这就是最简单的 RAG！
    if st.session_state.file_content:
        system_prompt = f"""
        你是一个专业的文档分析助手。
        请根据以下【参考文档】的内容回答用户的问题。
        如果文档里没有提到，就直接说"文档里没写"。
        
        【参考文档】：
        {st.session_state.file_content}
        """
    else:
        system_prompt = "你是一个助手，目前用户还没有上传任何文件。"

    # C. 调用 API
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages # 加上历史对话
            ]
        )
        ai_reply = response.choices[0].message.content

        # D. 显示 AI 回复
        with st.chat_message("assistant"):
            st.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
    except Exception as e:
        st.error(f"出错了：{e}")