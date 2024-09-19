from rdflib import Graph
import logging

logger = logging.getLogger(__name__)

def validate_and_convert_to_owl(rdf_data):
    try:
        g = Graph()
        g.parse(data=rdf_data, format="turtle")
        return g.serialize(format='xml')
    except Exception as e:
        logger.error(f"RDF validation/conversion error: {e}")
        return None