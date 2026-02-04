import json
token = "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"
from groq import Groq

#carico i due dataset
with open("FEVER-it_dataset.json", "r", encoding="utf-8") as f:
    FEVER = json.load(f)

with open("PolitiFact_dataset.json", "r", encoding="utf-8") as p:
    PolitiFact = json.load(p)

model = "gemma2-9b-it"

client = Groq(api_key=token)
with open("decomposition_prompt.txt", "r", encoding="utf-8") as f:
    decomposition_prompt = f.read()  # legge tutto il file come stringa

affermazione = "L'Italia ha vinto il Campionato Europeo di calcio nel 2021"
decomposition_prompt = decomposition_prompt.replace("<AFFERMAZIONE DA INSERIRE>", affermazione)

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": decomposition_prompt
        }
    ],
    temperature=0,
    max_tokens=200
)

print(completion.choices[0].message.content)