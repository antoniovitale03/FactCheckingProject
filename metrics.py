import json
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report

with open("dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

def pipeline_A():
    with open("results_A.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    y_true = [item["Etichetta"] for item in dataset]
    y_pred = [item["Predizione"] for item in results]

    print("Pipeline A")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("Precision:", precision_score(y_true, y_pred, pos_label="Vero"))
    print("Recall:", recall_score(y_true, y_pred, pos_label="Vero"))
    print("F1-score:", f1_score(y_true, y_pred, pos_label="Vero"))

def calculate_evidence_metrics():
    evidence_faithfulness = 0
    verdict_evidence_consistency = 0
    evidence_precision = 0
    hallucinations_rate = 0
    with open("pipelineB/results_B.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    for e in results:
        evidence_faithfulness += e["Evidence Faithfulness"]["Punteggio"]
        verdict_evidence_consistency += e["Verdict-Evidence Consistency"]["Punteggio"]
        evidence_precision += e["Evidence Precision"]["Punteggio"]
        hallucinations_rate += e["Hallucination Rate"]["Punteggio"]
    return evidence_faithfulness/100, verdict_evidence_consistency/100, evidence_precision/100, hallucinations_rate/100



def pipeline_B():
    with open("pipelineB/results_B.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    y_true = [item["Etichetta"] for item in dataset]
    y_pred = [item["Predizione"] for item in results]

    print("Pipeline B")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("Precision:", precision_score(y_true, y_pred, pos_label="Vero"))
    print("Recall:", recall_score(y_true, y_pred, pos_label="Vero"))
    print("F1-score:", f1_score(y_true, y_pred, pos_label="Vero"))
    evidence_faithfulness, verdict_evidence_consistency, evidence_precision, hallucinations_rate = calculate_evidence_metrics()
    print("Evidence Faithfulness", evidence_faithfulness)
    print("Verdict Evidence consistency", verdict_evidence_consistency)
    print("Evidence Precision", evidence_precision)
    print("Hallucinations Rate", hallucinations_rate, "%")

def pipeline_C():
    with open("pipelineC/results_C.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    # id delle affermazioni non verificabili, da ignorare nel calcolo delle metriche
    id_to_ignore = [10, 26, 28, 76, 78, 59 ]
    y_true = [item["Etichetta"] for item in dataset if item["id"] not in id_to_ignore]
    y_pred = [item["Predizione"] for item in results if item["id"] not in id_to_ignore]

    print("Pipeline C")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("Precision:", precision_score(y_true, y_pred, pos_label="Vero"))
    print("Recall:", recall_score(y_true, y_pred, pos_label="Vero"))
    print("F1-score:", f1_score(y_true, y_pred, pos_label="Vero"))

if __name__ == "__main__":
    pipeline_A()
    pipeline_B()
    pipeline_C()


