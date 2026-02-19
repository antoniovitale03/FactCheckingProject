#carica indice, riceve la query, fa recupero, costruisce il prompt e genera la risposta

import faiss
import json
from sentence_transformers import SentenceTransformer
from deep_translator import GoogleTranslator
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

embedder = SentenceTransformer("BAAI/bge-base-en-v1.5", device="cuda")

index = faiss.read_index("faiss_index.bin")

with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# ====== 4. Funzione RAG ======
def retrieval(query, top_k=5):
    # embedding query
    query_vector = embedder.encode([query], convert_to_numpy=True).astype("float32")

    # retrieval
    distances, indices = index.search(query_vector, top_k)

    retrieved_chunks = [chunks[i] for i in indices[0]]
    retrieved_metadata = [metadata[i] for i in indices[0]]
    print("\n--- CHUNKS RECUPERATI ---")
    for c in retrieved_chunks:
        print(c[:300], "\n")

if __name__ == "__main__":
    while True:
        italian_query = input("Affermazione: ")
        english_query = GoogleTranslator(source='it', target='en').translate(italian_query)
        retrieval(english_query)