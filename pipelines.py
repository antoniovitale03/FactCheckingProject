#questo file permette di automatizzare il processo di creazione dei prompt di verifica.
#N.B.: i prompt sono sempre inseriti manualmente nell'LLM

import json
from deep_translator import GoogleTranslator

# Carica dataset
with open("dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Carica prompt template
with open("verification_prompt_A.txt", "r", encoding="utf-8") as f:
    template_prompt_A = f.read()

with open("pipelineB/verification_prompt_B.txt", "r", encoding="utf-8") as f:
    template_prompt_B = f.read()

with open("pipelineB/evidence_faithfullness.txt", "r", encoding="utf-8") as f:
    evidence_faithfullness_prompt = f.read()

with open("pipelineB/verdict-evidence_consistency.txt", "r", encoding="utf-8") as f:
    verdict_evidence_consistency_prompt = f.read()

with open("pipelineB/evidence-precision.txt", "r", encoding="utf-8") as f:
    evidence_precision_prompt = f.read()

with open("pipelineC/triples_extraction_prompt.txt", "r", encoding="utf-8") as f:
    triples_extraction_prompt = f.read()

with open("pipelineC/triples_normalization_prompt.txt", "r", encoding="utf-8") as f:
    triples_normalization_prompt = f.read()

def pipeline_A():
    for e in dataset:
        print(f"N. {e["id"]} ----------------------")
        prompt = template_prompt_A.replace("{AFFERMAZIONE}", e["Affermazione"])
        print(prompt)

def pipeline_B():
    with open("pipelineB/results_B.json", "r", encoding="utf-8") as f:
        results_B = json.load(f)
    #for e in results_B:
        #print(f"N. {e["id"]} ----------------------")
        #prompt = template_prompt_B.replace("{AFFERMAZIONE}", e["Affermazione"]).replace("{EVIDENZE}", e["Evidenze"])
        #print(prompt)
    for e in results_B:
        print(f"N. {e["id"]} ----------------------")
        evidence_faithfullness_prompt = (evidence_faithfullness_prompt
                                         .replace("{AFFERMAZIONE}", e["Affermazione"])
                                         .replace("{EVIDENZE}", e["Evidenze"])
                                         .replace("{SPIEGAZIONE}", e["Spiegazione"]))
        print(evidence_faithfullness_prompt)

    for e in results_B:
        print(f"N. {e["id"]} ----------------------")
        verdict_evidence_consistency_prompt = (verdict_evidence_consistency_prompt
                                         .replace("{AFFERMAZIONE}", e["Affermazione"])
                                         .replace("{EVIDENZE}", e["Evidenze"])
                                         .replace("{VERDETTO}", e["Predizione"]))
        print(verdict_evidence_consistency_prompt)

    for e in results_B:
        print(f"N. {e["id"]} ----------------------")
        evidence_precision_prompt = (evidence_precision_prompt
                                         .replace("{AFFERMAZIONE}", e["Affermazione"])
                                         .replace("{EVIDENZE}", e["Evidenze"])
                                         .replace("{VERDETTO}", e["Predizione"]))
        print(evidence_precision_prompt)

def pipeline_C():
    with open("pipelineC/results_C.json", "r", encoding="utf-8") as f:
        results_C = json.load(f)
    #for e in results_C:
        #print(f"N. {e["id"]} ----------------------")
        #english_claim = GoogleTranslator(source="it", target="en").translate(e["Affermazione"])
        #prompt = triples_extraction_prompt.replace("{AFFERMAZIONE}", english_claim])
        #print(prompt)
    for e in results_C:
        print(f"N. {e["id"]} ----------------------")
        prompt = triples_normalization_prompt.replace("{TRIPLE}", f"{e["Triple"]}" )
        print(prompt)

if __name__ == "__main__":
    pipeline_C()


