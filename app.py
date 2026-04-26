import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# --- ページ設定 ---
st.set_page_config(
    page_title="RAGナレッジベースアシスタント",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- スタイル調整 ---
st.markdown("""
<style>
.main-title { font-size: 2rem; font-weight: bold; margin-bottom: 0; }
.sub-title { color: #666; font-size: 0.9rem; margin-top: 0; }
</style>
""", unsafe_allow_html=True)

# --- ヘッダー ---
st.markdown('<p class="main-title">🤖 RAGナレッジベースアシスタント</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">RAGの概念・アーキテクチャ・評価手法などに関する質問にお答えします</p>', unsafe_allow_html=True)
st.divider()

# --- サイドバー ---
st.sidebar.header("⚙️ 設定")
k_value = st.sidebar.slider("参照するチャンク数", min_value=1, max_value=8, value=3,
                              help="多いほど広範囲を参照するが、ノイズも増える")
show_sources = st.sidebar.checkbox("参照チャンクを表示", value=False)
temperature = st.sidebar.slider("回答の多様性（Temperature）", min_value=0.0, max_value=1.0,
                                  value=0.0, step=0.1,
                                  help="0に近いほど安定した回答、1に近いほど多様な回答")

st.sidebar.divider()
st.sidebar.markdown("**💡 質問例**")
example_questions = [
    "RAGとは何ですか？",
    "RAGの3つのフェーズを教えてください",
    "HyDEとはどんな手法ですか？",
    "チャンクサイズが小さすぎるとどうなりますか？",
    "Faithfulnessスコアを教えてください",
]
for q in example_questions:
    if st.sidebar.button(q, use_container_width=True):
        st.session_state.example_question = q

st.sidebar.divider()
st.sidebar.markdown("**📊 システム情報**")
st.sidebar.markdown("- モデル: GPT-4o-mini")
st.sidebar.markdown("- Embedding: text-embedding-3-small")
st.sidebar.markdown("- VectorDB: Chroma（ローカル）")

# --- RAGの初期化 ---
@st.cache_resource
def load_rag(temperature_val):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    vectordb = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=temperature_val,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return vectordb, llm, embeddings

vectordb, llm, embeddings = load_rag(temperature)

# --- プロンプト ---
prompt = ChatPromptTemplate.from_template("""
あなたはRAG技術の専門家アシスタントです。
以下の技術資料をもとに、質問に正確に日本語で回答してください。

【回答ルール】
1. 必ず「参考資料」の内容のみを根拠に回答する
2. 数値やスコアなどは参考資料から正確に引用する
3. 参考資料に記載がない場合は「提供された資料には記載がありません」と明示する
4. 回答は箇条書きを活用して見やすく整理する
5. 技術用語には必要に応じて補足説明を加える

参考資料:
{context}

質問: {question}

回答:
""")

def format_docs(docs):
    return "\n\n".join([f"【資料{i+1}】\n{doc.page_content}" for i, doc in enumerate(docs)])

# --- チャット履歴の初期化 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "example_question" not in st.session_state:
    st.session_state.example_question = None

# --- チャット履歴の表示 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and show_sources and "sources" in message:
            with st.expander("📄 参照した資料チャンク"):
                for i, source in enumerate(message["sources"]):
                    st.markdown(f"**チャンク {i+1}:**")
                    st.text(source)
                    st.divider()

# --- 質問入力 ---
if st.session_state.example_question:
    question = st.session_state.example_question
    st.session_state.example_question = None
else:
    question = st.chat_input("RAGに関する質問を入力してください（例：RAGとは何ですか？）")

# --- 回答生成 ---
if question:
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("資料を検索して回答を生成中..."):
            retriever = vectordb.as_retriever(search_kwargs={"k": k_value})
            docs = retriever.invoke(question)
            context = format_docs(docs)

            rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            answer = rag_chain.invoke(question)

        st.markdown(answer)

        if show_sources:
            with st.expander("📄 参照した資料チャンク"):
                for i, doc in enumerate(docs):
                    st.markdown(f"**チャンク {i+1}:**")
                    st.text(doc.page_content)
                    st.divider()

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": [doc.page_content for doc in docs]
    })

# --- 会話リセットボタン ---
if st.session_state.messages:
    if st.button("🗑️ 会話をリセット", type="secondary"):
        st.session_state.messages = []
        st.rerun()