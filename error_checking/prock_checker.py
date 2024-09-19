import requests
import json
import logging
from rdflib import Graph

logger = logging.getLogger(__name__)

class PROCKChecker:
    API_ENDPOINT = "http://localhost:8085/defectCandidates"

    @staticmethod
    def check(ontology_file):
        logger.info("Sending PROCK API request...")
        try:
            rdf_data = ontology_file.read().decode('utf-8')
            g = Graph()
            g.parse(data=rdf_data, format="turtle")
            rdf_data = g.serialize(format="ttl")
            response = requests.post(
                url=PROCKChecker.API_ENDPOINT,
                headers={"Content-Type": "text/turtle"},
                data=rdf_data.encode('utf-8'),
                timeout=600  # 10 minutes timeout
            )
            return response.json()
        except requests.Timeout:
            logger.error("Timeout error for PROCK API request")
        except requests.RequestException as e:
            logger.error(f"Request error for PROCK API request: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response from PROCK: {e}")
        return None