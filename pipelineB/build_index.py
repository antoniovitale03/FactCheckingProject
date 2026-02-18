#carica i JSON estratti, li suddivide in chunk e li converte in
#vettori, per poi indicizzarli e salvarli.

import os
import re
import json
import faiss
from sentence_transformers import SentenceTransformer

def clean_text(text):

    # rimuove riferimenti tipo [1]
    text = re.sub(r"\[\d+\]", "", text)

    # rimuove spazi multipli
    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"\(.*?\)", "", text)  # rimuove parentesi inutili

    return text.strip()

def chunk_text(text, chunk_size=350, overlap=80):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start += chunk_size - overlap

    return chunks

DATA_FOLDER = "../data/extracted"

# Carica modello embedding
#model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

all_chunks = []
metadata = []

# Scorri tutte le cartelle (AA, AB, AC, ...)
for subfolder in os.listdir(DATA_FOLDER):
    subfolder_path = os.path.join(DATA_FOLDER, subfolder)

    if not os.path.isdir(subfolder_path):
        continue

    print(f"Processing folder: {subfolder}")

    for filename in os.listdir(subfolder_path):

        file_path = os.path.join(subfolder_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    doc = json.loads(line)
                except json.JSONDecodeError:
                    continue

                title = doc.get("title", "")
                text = doc.get("text", "")

                if title.lower().startswith("list of"):
                    continue

                if "(disambiguation)" in title.lower():
                    continue

                if not text:
                    continue

                text = clean_text(text)

                if len(text) < 1000:
                    continue

                chunks = chunk_text(text)

                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    metadata.append({
                        "title": title,
                        "chunk_id": f"{title}_{i}"
                    })

                MAX_CHUNKS = 1000000
                if len(all_chunks) >= MAX_CHUNKS:
                    break

print(f"Totale chunk: {len(all_chunks)}")
with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f)

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f)

#Embedding
print("Calcolo embeddings...")
embeddings = model.encode(all_chunks,
                          batch_size=256,
                          show_progress_bar=True,
                          convert_to_numpy=True,
                          normalize_embeddings=True).astype("float32")

#FAISS
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

#index = faiss.IndexFlatL2(dimension)
#index.add(embeddings)

#Salvataggio
faiss.write_index(index, "faiss_index.bin")

print("Indice costruito con successo!")
