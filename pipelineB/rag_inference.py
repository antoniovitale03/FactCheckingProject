#carica indice, riceve la query, fa recupero, costruisce il prompt e genera la risposta

import faiss
import json
from sentence_transformers import SentenceTransformer
from deep_translator import GoogleTranslator
import linecache
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

embedder = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")

index = faiss.read_index("faiss_index.bin")
index.nprobe = 64 #cluster esplorati durante la ricerca
#il numero ottimale sarebbe 32, ma ho deciso di avere maggiore accuratezza nel recupero, a costo
#di maggiore tempo richiesto per la ricerca dei chunk


def get_chunks(indices):
    indices = sorted(indices)
    chunks = []
    current_target = 0

    with open("chunks.jsonl", "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f):

            if current_target >= len(indices):
                break

            if line_number == indices[current_target]:
                italian_chunk = GoogleTranslator(source="en", target="it").translate(json.loads(line)["text"])
                chunks.append(italian_chunk)
                current_target += 1
    # restituisce nello stesso ordine originale
    return chunks



def retrieval(query, top_k=7):
    # embedding query
    query_vector = embedder.encode([query],
                                   convert_to_numpy=True,
                                   normalize_embeddings=True
                                   ).astype("float32")

    # retrieval
    distances, indices = index.search(query_vector, top_k)

    retrieved_chunks = get_chunks(indices[0])
    evidence = "".join(retrieved_chunks)
    return evidence

if __name__ == "__main__":
    with open("results_B.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for element in data:
            italian_query = element["Affermazione"]
            english_query = GoogleTranslator(source='it', target='en').translate(italian_query)
            evidence = retrieval(english_query)
            element["Evidenze"] = evidence
        with open("results_B.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)