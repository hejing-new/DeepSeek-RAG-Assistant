import streamlit as st
from openai import OpenAI
import PyPDF2
import chromadb # <--- 新朋友：向量数据库

# --- 1. 页面设置 ---
st.set_page_config(page_title="RAG 专业版 (ChromaDB)", layout="wide")
st.title("🧠 也就是所谓的“第二大脑” (ChromaDB 版)")
st.caption("现在，你可以上传几百页的书，我也能瞬间找到答案！")

# --- 2. 初始化 ChromaDB (持久化存储) ---
# 这行代码会在你当前目录下创建一个叫 "my_knowledge_base" 的文件夹用来存数据
# 哪怕你关掉网页，数据依然在！
chroma_client = chromadb.PersistentClient(path="./my_knowledge_base")

# 创建或获取一个“集合”（类似于数据库里的表）
collection = chroma_client.get_or_create_collection(name="my_documents")

# --- 3. 初始化 DeepSeek ---
with st.sidebar:
    api_key = st.text_input("请输入 DeepSeek API Key", type="password", value="sk-这里填你的Key")

client = OpenAI(
    api_key=input("请输入Key:"),
    base_url="https://api.deepseek.com"
)

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. 辅助函数：文本切片 (Chunking) ---
# 工业级应用里通常用 LangChain 切，这里我们手写一个简单的
# 把长文章切成每块 300 字的小段
def split_text(text, chunk_size=300):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

# --- 5. 侧边栏：上传并处理文件 ---
with st.sidebar:
    st.header("📂 知识库管理")
    uploaded_file = st.file_uploader("上传 PDF 投喂给数据库", type=["pdf"])
    
    if uploaded_file:
        # 按钮：防止每次刷新都重新读文件
        if st.button("开始处理并存入数据库"):
            with st.spinner("正在切片并存入 Chroma... (第一次运行需下载模型，请稍候)"):
                try:
                    # A. 读取 PDF
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    full_text = ""
                    for page in pdf_reader.pages:
                        full_text += page.extract_text()
                    
                    # B. 切片 (Chunking)
                    chunks = split_text(full_text)
                    st.write(f"📊 文章已切分为 {len(chunks)} 个片段")

                    # C. 存入 Chroma
                    # ids 必须是唯一的，我们简单用文件名+序号
                    ids = [f"{uploaded_file.name}_{i}" for i in range(len(chunks))]
                    
                    # 这一步最关键！Chroma 会自动把文字变成向量存起来
                    collection.add(
                        documents=chunks,
                        ids=ids
                    )
                    st.success("✅ 成功存入向量数据库！")
                except Exception as e:
                    st.error(f"出错啦：{e}")

    # 显示数据库当前状态
    count = collection.count()
    st.info(f"📚 当前知识库里共有 {count} 个知识片段")
    
    if st.button("清空知识库"):
        chroma_client.delete_collection("my_documents")
        st.experimental_rerun()

# --- 6. 聊天界面 ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 7. 核心逻辑：检索 (Retrieval) + 生成 (Generation) ---
if user_input := st.chat_input("请问知识库..."):
    
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # A. 检索 (Retrieval)
    # 去 Chroma 里搜，找出跟问题最相关的 3 个片段 (n_results=3)
    results = collection.query(
        query_texts=[user_input],
        n_results=3
    )
    
    # 把搜到的 3 段文字拼起来
    retrieved_text = "\n\n".join(results['documents'][0])
    
    # 调试信息：让你看看 AI 到底参考了哪些内容（开发时很有用）
    with st.expander("🕵️‍♂️ 我参考了以下片段 (RAG Debug)"):
        st.text(retrieved_text)

    # B. 生成 (Generation)
    system_prompt = f"""
    你是一个基于知识库的智能助手。
    请严格根据下面的【参考资料】回答用户问题。
    如果资料里没有提到，就说不知道。

    【参考资料】：
    {retrieved_text}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ]
        )
        ai_reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
    except Exception as e:
        st.error(f"API 出错：{e}")