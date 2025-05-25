import psycopg2
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to split documents based on heading markers
def chunk_text(text):
    chunks = []
    current_chunk = []

    for line in text.split("\n"):
        if line.strip().startswith("###"):
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
        current_chunk.append(line)

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks

# Locate .md files
data_folder = Path('data')
all_md_files = list(data_folder.glob("*.md"))

# Connect to PostgreSQL (adjust your settings)
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    dbname="semantic_search_db",
    user="postgres",
    password="your_password_here"
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id serial PRIMARY KEY,
        name text,
        embedding vector(384),
        content text
    );
""")

# Process each markdown file
for file_path in all_md_files:
    print(f"\n📄 Processing file: {file_path.name}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = chunk_text(content)
    print(f"🔹 Chunks created: {len(chunks)}")

    embeddings = model.encode(chunks, show_progress_bar=True)

    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        vector_str = "[" + ",".join([str(x) for x in vector]) + "]"
        cursor.execute(
            "INSERT INTO items (name, embedding, content) VALUES (%s, %s, %s)",
            (f"{file_path.name} - chunk {i + 1}", vector_str, chunk)
        )

# Finalize
conn.commit()
cursor.close()
conn.close()
print("\n✅ All documents embedded and stored successfully.")
