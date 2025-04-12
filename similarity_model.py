from rdflib.namespace import RDF
from rdflib import Graph, Namespace
from sentence_transformers import SentenceTransformer, util

# Load ontology
g = Graph()
g.parse("disaster_ontology.rdf")

# Load BERT model
model = SentenceTransformer('all-MiniLM-L6-v2') 

# Define namespace
EX = Namespace("http://www.semanticweb.org/zakar/ontologies/2025/1/DisasterOntology#")

def get_instance_descriptions():
    event_descriptions = []

    for event in g.subjects(RDF.type, EX.DisasterEvent):
        disaster_group = g.value(event, EX.disasterGroup)
        subgroup = g.value(event, EX.disasterSubgroup)
        subtype = g.value(event, EX.disasterSubtype)

        # Note the corrected typo: "ocurredAt"
        location = g.value(event, EX.ocurredAt)

        #if location:
        #    print(f"Location {location}")
        #    for p, o in g.predicate_objects(location):
        #       print(f"  {p} -> {o}")


        # Check if the location has country, region, subregion properties
        country = g.value(location, EX.country) if location else None
        region = g.value(location, EX.region) if location else None
        subregion = g.value(location, EX.subregion) if location else None

        # Build a clean string of all parts
        parts = [str(x) for x in [subtype, disaster_group, subgroup, country, region, subregion] if x]
        if parts:
            description = " ".join(parts).lower()
            event_descriptions.append(description)

    return event_descriptions

def preprocess_message(msg):
    return msg.strip().lower()

def compare_to_ontology_instances(message: str) -> float:
    instances = get_instance_descriptions()
    if not instances:
        print("No disaster instances found.")
        return 0.0

    print(f"Preprocessed message: {message}")
    #for inst in instances:
    #    print(f"Instance: {inst}")

    message_embedding = model.encode(preprocess_message(message), convert_to_tensor=True)
    instance_embeddings = model.encode(instances, convert_to_tensor=True)

    similarity_scores = util.cos_sim(message_embedding, instance_embeddings)
    return float(similarity_scores.max())
