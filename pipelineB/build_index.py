#carica i JSON estratti, li suddivide in chunk e li converte in
#vettori, per poi indicizzarli e salvarli.
import gc
import os
import re
import json
import faiss
from sentence_transformers import SentenceTransformer
import torch

embedder = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
DATA_FOLDER = "../data/extracted"




def clean_text(text):

    # rimuove riferimenti tipo [1]
    text = re.sub(r"\[\d+\]", "", text)

    # rimuove spazi multipli
    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"\(.*?\)", "", text)  # rimuove parentesi inutili

    return text.strip()


def chunk_text(text, chunk_size=250, overlap=80):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start += chunk_size - overlap

    return chunks

def create_chunks():
    chunks_file = open("chunks.jsonl", "w", encoding="utf-8")
    metadata_file = open("metadata.jsonl", "w", encoding="utf-8")
    #Scorri tutte le cartelle (AA, AB, AC, ...)
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
                        record_chunk = {"text": chunk}
                        record_metadata = {"title": title, "chunk_id": f"{title}_{i}"}
                        chunks_file.write(json.dumps(record_chunk) + "\n")
                        metadata_file.write(json.dumps(record_metadata) + "\n")

    chunks_file.close()
    metadata_file.close()
    print("chunks e metadata salvati")

def create_index():

    torch.set_num_threads(12)
    faiss.omp_set_num_threads(12)

    #creazione index
    dimension = embedder.get_sentence_embedding_dimension()
    quantizer = faiss.IndexFlatIP(dimension)
    index = faiss.IndexIVFPQ(quantizer, dimension, 4096, 64, 8)

    #training dell'index (200.000 chunk)
    train_samples = []
    MAX_TRAIN = 30000

    with open("chunks.jsonl", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= MAX_TRAIN:
                break
            obj = json.loads(line)
            train_samples.append(obj["text"])

    print("Embedding training sample...")

    train_embeddings = embedder.encode(
        train_samples,
        batch_size=384,
        convert_to_numpy=True,
        show_progress_bar=True,
        normalize_embeddings=True
    ).astype("float32")

    print("Training IVF-PQ...")
    print("Shape training embeddings:", train_embeddings.shape)
    index.train(train_embeddings)

    del train_embeddings
    del train_samples
    gc.collect()
    torch.cuda.empty_cache()

    print("Inizio indicizzazione")
    BLOCK_SIZE = 1000000  # 1 milione di chunk per volta
    block = []
    total = 0  # totale chunks

    with open("chunks.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            block.append(obj["text"])
            if len(block) == BLOCK_SIZE: #1 milione di chunk

                #eseguo volta per volta embedding di 40.000 chunk
                for i in range(0, len(block), 40000):
                    chunks = block[i:i + 40000]
                    embeddings = embedder.encode(chunks,
                                                 batch_size=384,
                                                 convert_to_numpy=True,
                                                 normalize_embeddings=True,
                                                 show_progress_bar=True,
                                                 ).astype("float32")


                    index.add(embeddings)
                    total += len(chunks)
                    print(f"Indicizzati: {total}")

                block = []
                gc.collect()
                torch.cuda.empty_cache()

    #ultimo blocco
    if block:
        for i in range(0, len(block), 40000):
            chunks = block[i: i+ 40000]
            embeddings = embedder.encode(chunks,
                                         batch_size=384,
                                         convert_to_numpy=True,
                                         normalize_embeddings=True,
                                         show_progress_bar=True,
                                         ).astype("float32")
            index.add(embeddings)

    # Salvataggio
    faiss.write_index(index, "faiss_index.bin")

    print("Indice costruito con successo!")

if __name__ == "__main__":
    create_chunks()
    create_index()

