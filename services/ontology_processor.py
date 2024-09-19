from services.ontology_metrics import OntologyMetricsService

class OntologyProcessor:
    @staticmethod
    def process_ontology(ontology_file):
        return OntologyMetricsService.calculate_metrics(ontology_file)