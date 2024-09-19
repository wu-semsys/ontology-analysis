import rdflib
from models.ontology_metrics import OntologyMetrics
import logging

logger = logging.getLogger(__name__)

class OntologyMetricsService:
    @staticmethod
    def calculate_metrics(ontology_file):
        try:
            graph = rdflib.Graph()
            graph.parse(ontology_file, format="turtle")
            
            metrics = OntologyMetrics(graph)
            return metrics.calculate_ontology_metrics(), None
        except Exception as e:
            logger.exception("An error occurred while processing the ontology")
            return None, str(e)

    @staticmethod
    def explain_expressivity(expressivity):
        try:
            metrics = OntologyMetrics()
            return metrics.explain_dl_expressivity(expressivity), None
        except Exception as e:
            logger.exception("An error occurred while explaining expressivity")
            return None, str(e)