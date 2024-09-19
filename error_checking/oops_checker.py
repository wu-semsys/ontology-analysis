import requests
import xmltodict
import logging
from utils.rdf_utils import validate_and_convert_to_owl

logger = logging.getLogger(__name__)

class OOPSChecker:
    API_ENDPOINT = "https://oops.linkeddata.es/rest"

    @staticmethod
    def check(ontology_file):
        logger.info("Sending OOPS! API request...")
        try:
            rdf_data = ontology_file.read().decode('utf-8')
            owl_data = validate_and_convert_to_owl(rdf_data)
            if not owl_data:
                return None

            body = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <OOPSRequest>
                        <OntologyURI></OntologyURI>
                        <OntologyContent><![CDATA[{owl_data}]]></OntologyContent>
                        <Pitfalls>P01,P02,P03,P04,P05,P06,P07,P08,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22,P23,P24,P25,P26,P27,P28,P29,P30,P31,P32,P33,P34,P35,P36,P37,P38,P39,P40,P41</Pitfalls>
                        <OutputFormat>RDF/XML</OutputFormat>
                    </OOPSRequest>"""
            
            response = requests.post(
                url=OOPSChecker.API_ENDPOINT,
                headers={"Content-Type": "text/xml"},
                data=body.encode('utf-8'),
                timeout=600  # 10 minutes timeout
            )
            errors_oops_xml = response.text
            if "unexpected_error" in errors_oops_xml:
                logger.error("Unexpected error from OOPS!")
                return None
            oops_dict = xmltodict.parse(errors_oops_xml)
            errors_oops = []
            for s in oops_dict.get("rdf:RDF", {}).get("rdf:Description", []):
                if isinstance(s, dict) and s.get("oops:hasName"):
                    errors_oops.append({
                        "name": s.get("oops:hasName", {}).get("#text"),
                        "description": s.get("oops:hasDescription", {}).get("#text"),
                        "importanceLevel": s.get("oops:hasImportanceLevel", {}).get("#text"),
                        "code": s.get("oops:hasCode", {}).get("#text"),
                        "numberAffectedElements": int(s.get("oops:hasNumberAffectedElements", {}).get("#text", 0))
                    })
            return errors_oops
        except requests.Timeout:
            logger.error("Timeout error for OOPS! API request")
        except requests.RequestException as e:
            logger.error(f"Request error for OOPS! API request: {e}")
        except Exception as e:
            logger.error(f"Error processing OOPS! response: {e}")
        return None