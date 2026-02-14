import json
from openai import OpenAI
import time
time.sleep(1)

client = OpenAI(api_key="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")

# Carica dataset
with open("dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Carica prompt template
with open("verification_prompt_A.txt", "r", encoding="utf-8") as f:
    template_prompt = f.read()

prompt = template_prompt.replace("{AFFERMAZIONE}", "I cani parlano italiano.")
response = client.responses.create(
            model="gpt-3.5-turbo",
            input=[{"role": "user", "content": prompt}],
        )


print(response.output_text)
