# 🧠 DeepSeek RAG Assistant

这是一个基于 **DeepSeek-V3** 大模型与 **ChromaDB** 向量数据库构建的垂直领域文档问答助手。

它可以读取用户上传的 PDF 文档，通过 RAG (检索增强生成) 技术，实现基于私有知识库的精准问答。

## 🛠️ 技术栈 (Tech Stack)

- **LLM:** DeepSeek-Chat (via OpenAI SDK)
- **Database:** ChromaDB (Vector Store)
- **Frontend:** Streamlit
- **Tools:** PyPDF2, LangChain (Optional)

## 🚀 功能特点

1. **私有数据解析:** 支持上传 PDF 文档并进行自动化切片 (Chunking)。
2. **向量化存储:** 使用 Embedding 技术将文本持久化存储至 ChromaDB。
3. **语义检索:** 基于余弦相似度检索最相关的文档片段，拒绝幻觉。
4. **多轮对话:** 支持上下文记忆 (Context Awareness)。

## 📦 如何运行

1. 克隆项目
git clone https://github.com/hejing-new/DeepSeek-RAG-Assistant.git

2. 安装依赖
pip install streamlit openai chromadb pydPDF2

3. 运行应用
python -m streamlit run rag_chroma.py