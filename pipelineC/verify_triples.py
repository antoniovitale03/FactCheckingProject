import json

from SPARQLWrapper import SPARQLWrapper, JSON
DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

with open("results_C.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

def expand_uri(term):
    term = term.strip()
    if term.startswith("dbr:"):
        return f"<http://dbpedia.org/resource/{term[4:]}>"
    elif term.startswith("dbo:"):
        return f"<http://dbpedia.org/ontology/{term[4:]}>"
    else: return term

#verifica l'esistenza della tripla
def find_triple(subject, relation, object):
    sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(10)

    subject = expand_uri(subject)
    relation = expand_uri(relation)
    object = expand_uri(object)

    query = f"""
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        ASK {{
            {subject} {relation} {object} .
        }}
        """
    sparql.setQuery(query)
    result = sparql.query().convert()
    return result["boolean"]

#94 affermazioni verificabili su cui vengono calcolate le metriche
if __name__ == "__main__":
    for e in dataset:
        if e["Triple Normalizzate"]:
            e["Risultati"] = []
            e["Predizione"] = ""
            for triple in e["Triple Normalizzate"]:
                triple = triple[1:-1].split(",")
                triple = [e.strip() for e in triple]
                is_true = find_triple(triple[0],
                                        triple[1],
                                        triple[2])
                if is_true == True:
                    e["Risultati"].append("Vero")
                else: e["Risultati"].append("Falso")
            if all(x == "Vero" for x in e["Risultati"]):
                e["Predizione"] = "Vero"
            else: e["Predizione"] = "Falso"

    print(c)

    with open("results_C.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)