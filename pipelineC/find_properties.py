from SPARQLWrapper import SPARQLWrapper, JSON
DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

#ottengo le proprietà sia nel caso l'entità sia un soggetto che sia un oggetto
def get_properties(entity_uri):
    sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(10)

    queries = [
        # Entità come soggetto
        f"""
            SELECT DISTINCT ?property
            WHERE {{
              <{entity_uri}> ?property ?value .
              FILTER(STRSTARTS(STR(?property), "http://dbpedia.org/ontology/"))
            }}
            LIMIT 200
            """,
        # Entità come oggetto
        f"""
            SELECT DISTINCT ?property
            WHERE {{
              ?subject ?property <{entity_uri}> .
              FILTER(STRSTARTS(STR(?property), "http://dbpedia.org/ontology/"))
            }}
            LIMIT 200
            """
    ]

    properties = set()

    for query in queries:
        sparql.setQuery(query)
        try:
            results = sparql.query().convert()
            for result in results["results"]["bindings"]:
                uri = result["property"]["value"]
                dbo_name = "dbo:" + uri.split("/")[-1]
                properties.add(dbo_name)
        except Exception as e:
            print("Errore SPARQL:", e)

    return list(properties)

#per ogni tripla trovo tutte le proprietà candidate
def get_candidate_properties(subject_uri, object_uri):
    props_subject = get_properties(subject_uri)
    props_object = get_properties(object_uri)
    return list(set(props_subject + props_object))

