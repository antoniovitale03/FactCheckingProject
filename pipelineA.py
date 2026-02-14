import json
from idlelib.iomenu import encoding

token = "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"
from groq import Groq
#
#carico i due dataset
with open("dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)


model = "gemma2-9b-it"
#
client = Groq(api_key=token)
with open("decomposition_prompt.txt", "r", encoding="utf-8") as f:
    decomposition_prompt = f.read()  # legge tutto il file come stringa

with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

decomposition_prompt = decomposition_prompt.replace("<DATASET>", f"{dataset}")

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": decomposition_prompt
        }
    ],
    temperature=0,
    max_tokens=5000
)

print(completion.choices[0].message.content)