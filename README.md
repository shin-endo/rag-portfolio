# 🤖 RAGナレッジベースQAシステム

RAG（検索拡張生成）技術を使った知識検索アシスタントです。
LangChain + Chroma + Streamlitで構築。
RAGの概念・アーキテクチャ・評価手法などの質問に答えます。

👉 **[デモアプリを試す](https://rag-portfolio-ckn5nbuqcddv3xkf9pbri9.streamlit.app/)**

---

## 🎯 このシステムを作った背景

機械設計エンジニアとして、文書翻訳や調べものの時短など
AIを日常的な道具として使っていました。

そのうちAIでできることの可能性に気づき、
「本気で業務効率化に使えないか」と意識が変わりました。

設計業務の8割は「データの収集・整理・精査」です。
膨大な仕様書・規格・評価データの中から必要な情報を探し出す作業、
知識の属人化・新人への情報共有の非効率さ・他部署からの問い合わせ対応。

「この課題、AIで解決できないか」

調べていくうちにRAGという技術に行き着きました。

**「どんな構造で・どんな労力で・何ができるのか」**

それを確かめるために作ったのがこのシステムです。

---

## 🛠️ 技術スタック

| カテゴリ | 技術 |
|---|---|
| LLM | OpenAI GPT-4o-mini |
| Embedding | OpenAI text-embedding-3-small |
| Vector DB | Chroma |
| Framework | LangChain |
| UI | Streamlit |
| 言語 | Python 3.12 |

---

## ✨ 機能

- RAG関連の技術仕様を自然言語で質問・回答
- 参照チャンクの表示（回答根拠の可視化）
- チャット形式のUI（会話履歴保持）
- 参照チャンク数・Temperatureのリアルタイム調整
- 資料にない質問への「記載なし」応答（ハルシネーション抑制）

---

## 💬 質問例

### ✅ 答えられる質問（資料に含まれる）

| 質問 | 回答の概要 |
|---|---|
| RAGとは何ですか？ | RAGの定義・LLMとの違い |
| RAGの3つのフェーズを教えてください | インデックス構築・検索・生成の流れ |
| HyDEとはどんな手法ですか？ | 仮想回答を使った検索精度向上手法 |
| チャンクサイズが小さすぎるとどうなりますか？ | 文脈が失われ回答が断片的になる |
| Faithfulnessスコアを教えてください | 0.917（RAGAS評価結果） |

### ❌ 意図的に答えられない質問（設計として除外）

| 質問 | 理由 |
|---|---|
| RAGはいつ誰が開発しましたか？ | 資料に含まれない情報 |
| LangChainとLlamaIndexの違いは？ | 資料に含まれない情報 |
| ChromaとPineconeのコストは？ | 資料に含まれない情報 |

> 💡 資料に含まれない質問には「提供された資料には記載がありません」と返答します。
> これはRAGの重要な特性である**ハルシネーション抑制**を意図した設計です。

---

## 📊 RAGASによる評価結果

| 指標 | スコア | 評価 |
|---|---|---|
| Faithfulness（忠実度） | 0.917 | ✅ 高い |
| Answer Relevancy（回答適合度） | 0.648 | ⚠️ 改善余地あり |
| Context Recall（検索網羅率） | 1.000 | ✅ 完全 |
| Context Precision（検索精度） | 1.000 | ✅ 完全 |

> Answer Relevancyが低い原因は質問文と資料の表現のズレによるものと分析しています。
> 今後のブラッシュアップ課題として認識しています。

---

## 🚀 ローカルでの実行方法

### 1. リポジトリをクローン
```bash
git clone https://github.com/shin-endo/rag-portfolio.git
cd rag-portfolio
```

### 2. 仮想環境を作成・有効化
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. ライブラリをインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数を設定
`.env` ファイルを作成し、OpenAI APIキーを設定：
```
OPENAI_API_KEY=sk-...
```

### 5. ベクトルDBを構築
```bash
python build_db.py
```

### 6. アプリを起動
```bash
streamlit run app.py
```

---

## 📁 ファイル構成

```
rag-portfolio/
├── app.py              # メインアプリ（Streamlit）
├── build_db.py         # ベクトルDB構築スクリプト
├── documents/
│   └── rag_knowledge.txt  # RAG技術知識ベース
├── requirements.txt    # 必要なライブラリ一覧
├── .gitignore
└── README.md
```

---

## 👨‍💻 作者について

機械設計エンジニアとして製造業に従事。
AIを日常的に活用する中で業務課題の解決策としてRAGに行き着き、独学で構築。

- 機械設計の現場課題 × AI技術という実体験に基づくアプローチ
- 機械設計 × AI という専門性の掛け合わせを強みとして展開中
- 詳しい経緯は **[Zenn記事](https://zenn.dev)** をご覧ください

---

## 📝 関連記事

- [機械設計エンジニアがRAGを作った理由（Zenn）](https://zenn.dev)
