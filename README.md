# 🧠 SmartSemanticSearch

SmartSemanticSearch is a lightweight semantic search system that retrieves the most relevant chunks from text documents using vector similarity. It's ideal for AI-driven document search, knowledge base querying, and chatbot context injection.

---
## 💡 Overview

Instead of feeding entire documents to a chatbot or API, this project helps identify and retrieve the **most relevant text chunk** based on a user's question. This improves accuracy and efficiency in response generation.

---

## ⚙️ Tech Stack

- Python 3.10+
- PostgreSQL 15+ with `pgvector` extension
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Streamlit (for optional UI)

---

## 🔧 Setup Instructions

1. ✅ **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. ✅ Start PostgreSQL and enable pgvector:
   ```bash
   CREATE EXTENSION vector;
    ```
3. ✅ Prepare your text documents as .md files under data/ folder.


4. ✅ Run embedding pipeline:
   ```bash
   python scripts/chunk_and_embed.py
   ```
5. ✅ Search from terminal:
   ```bash
   python scripts/query_similar.py
   ```
6. ✅ (Optional) Launch the Streamlit UI:
   ```bash
   streamlit run scripts/app.py
   ```
💡 How It Works

    .md documents are chunked into ~300-token blocks.

    Each chunk is embedded using all-MiniLM-L6-v2.

    Embeddings are stored in a PostgreSQL vector column.

    When a user asks a question:

        The question is embedded.

        Semantic similarity search (<->) is performed.

        The top matching chunk is retrieved and displayed.

📁 Sample Questions

    What is the speaker's view on AI safety?
    Who supports stricter regulations in this transcript?
    What actions are proposed regarding data privacy?

📬 Notes

    This is a simplified prototype. In a production environment, vector index creation, LLM integration, or hybrid search may be applied.
---

## 🗄️ Database Setup

This project assumes a local PostgreSQL instance with the pgvector extension installed.
You do not need to use the same credentials or port.

Please update the connection parameters in the following files according to your local setup:

- `scripts/chunk_and_embed.py`
- `scripts/query_similar.py`
- `scripts/app.py` (optional Streamlit UI)

Replace this section in the code if needed:
```python
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    dbname="semantic_search_db",
    user="postgres",
    password="your_password_here"
)
```



