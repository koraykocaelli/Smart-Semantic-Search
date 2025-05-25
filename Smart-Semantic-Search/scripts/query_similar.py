import psycopg2
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to database (update credentials as needed)
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    dbname="semantic_search_db",
    user="postgres",
    password="your_password_here"
)
cursor = conn.cursor()

print("\n🔍 Semantic Search Terminal Interface")
print("Type a question to find the most relevant chunk.")
print("Type 'exit' to quit.\n")

while True:
    query = input("🔎 Your query: ")
    if query.lower().strip() == "exit":
        break

    # Generate embedding for the query
    embedding = model.encode([query])[0]
    vector_str = "[" + ",".join([str(x) for x in embedding]) + "]"

    # Search top 5 closest chunks
    cursor.execute("""
        SELECT name, content, embedding <-> %s AS distance
        FROM items
        ORDER BY distance
        LIMIT 5;
    """, (vector_str,))
    results = cursor.fetchall()

    if not results:
        print("❌ No results found.\n")
        continue

    closest_name, closest_content, closest_distance = results[0]

    print("\n📌 Top Match:")
    print(f"📝 File: {closest_name} (distance: {closest_distance:.4f})")
    print("📄 Content Preview:")
    print(closest_content.strip()[:800])  # show first 800 chars
    print("✅ Suggested as the most relevant chunk.\n")

    print("📋 Other similar chunks:")
    for row in results[1:]:
        print(f"- {row[0]} (distance: {row[2]:.4f})")

    print()

# Close connections
cursor.close()
conn.close()
