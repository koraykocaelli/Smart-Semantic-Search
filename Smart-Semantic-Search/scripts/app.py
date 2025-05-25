import streamlit as st
import psycopg2
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Database connection (adjust these as needed)
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    dbname="semantic_search_db",
    user="postgres",
    password="your_password_here"
)
cursor = conn.cursor()

# Streamlit UI setup
st.set_page_config(page_title="Semantic Search", page_icon="🔍")
st.title("🔍 Semantic Search Explorer")
st.markdown("Ask a question to find the most relevant content from your documents.")

# User input
query = st.text_input("🧠 Your question:")

if query:
    embedding = model.encode([query])[0]
    vector_str = "[" + ",".join([str(x) for x in embedding]) + "]"

    cursor.execute("""
        SELECT name, content, embedding <-> %s AS distance
        FROM items
        ORDER BY distance
        LIMIT 1;
    """, (vector_str,))
    result = cursor.fetchone()

    if result:
        name, content, distance = result
        st.success(f"✅ Closest match found in `{name}` (distance: {distance:.4f})")

        # Display answer suggestion
        last_line = content.strip().split("\n")[-1]
        st.markdown(f"**💬 Suggested Answer:** {last_line}")

        with st.expander("📄 View Full Chunk"):
            st.code(content.strip()[:1000])
    else:
        st.warning("⚠️ No results found.")

# Close DB connection on session end
cursor.close()
conn.close()
