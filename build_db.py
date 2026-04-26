import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

print("1. ドキュメントを読み込み中...")
loader = DirectoryLoader(
    "documents/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)
docs = loader.load()
print(f"   {len(docs)}ファイル読み込み完了")
for doc in docs:
    print(f"   - {doc.metadata['source']} ({len(doc.page_content)}文字)")

print("\n2. チャンク分割中...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=80,
    separators=["\n\n", "\n", "。", ".", " "]
)
chunks = splitter.split_documents(docs)
print(f"   {len(chunks)}チャンクに分割完了")

print("\n3. ベクトルDBを構築中...")
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY")
)
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
print(f"   ベクトルDB構築完了（{len(chunks)}チャンク保存済み）")

print("\n4. 検索テスト:")
test_queries = [
    "RAGとは何ですか？",
    "チャンク分割の適切なサイズは？",
    "HyDEとはどんな手法ですか？",
]
for q in test_queries:
    results = vectordb.similarity_search(q, k=2)
    print(f"\n   質問: {q}")
    print(f"   → {results[0].page_content[:80]}...")

print("\n✅ ベクトルDB構築完了！次は app.py を実行してください。")