#questo file permette di automatizzare il processo di creazione dei prompt di verifica.
#N.B.: i prompt sono sempre inseriti manualmente nell'LLM

import json

# Carica dataset
with open("dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Carica prompt template
with open("verification_prompt_A.txt", "r", encoding="utf-8") as f:
    template_prompt_A = f.read()

with open("pipelineB/verification_prompt_B.txt", "r", encoding="utf-8") as f:
    template_prompt_B = f.read()

def pipeline_A():
    for e in dataset:
        print(f"N. {e["id"]} ----------------------")
        prompt = template_prompt_A.replace("{AFFERMAZIONE}", e["Affermazione"])
        print(prompt)

def pipeline_B():
    with open("pipelineB/results_B.json", "r", encoding="utf-8") as f:
        results_B = json.load(f)
    for e in results_B:
        print(f"N. {e["id"]} ----------------------")
        prompt = template_prompt_B.replace("{AFFERMAZIONE}", e["Affermazione"]).replace("{EVIDENZE}", e["Evidenze"])
        print(prompt)

def pipeline_C():
    with open("results_C.json", "r", encoding="utf-8") as f:
        results_C = json.load(f)


if __name__ == "__main__":
    pipeline_B()


