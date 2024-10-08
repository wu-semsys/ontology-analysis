# Ontology Analysis API

This API offers functions for analyzing ontologies, extracting relevant metrics (class count, property count, etc.) and performing error checks. In addition, there is a local LLM functionality for extracting competency questions from PDF documents. 

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- PROCK service running locally
- Access to OOPS! web service

## Installation

1. Clone this repository:
   ```
   git clone https://git.ai.wu.ac.at/semsys/ontology-benchmark.git
   cd ontology-benchmark
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the `.env.template` file to `.env`:
   ```
   cp .env.template .env
   ```

2. Edit the `.env` file to configure your OLLAMA service and other settings:
   ```
   # OLLAMA Configuration
   OLLAMA_HOST=https://semsys-chat-api.ai.wu.ac.at/
   OLLAMA_MODEL=llama3.1
   
   # Error Checking Configuration
   PROCK_API_ENDPOINT=http://localhost:8085/defectCandidates
   OOPS_API_ENDPOINT=https://oops.linkeddata.es/rest
   ```

   Adjust these settings according to your OLLAMA configuration and PROCK local setup.

## Error Checking Services Setup

### OOPS!
OOPS! is a web service. Ensure it's accessible at https://oops.linkeddata.es/ before using the OOPS! error checking functionality.

### PROCK
The service for Defect checking with Prock's method needs to be run locally. Follow these steps to set it up:

1. Clone the PROCK repository:
   ```
   git clone https://github.com/wu-semsys/ontology-defect-heuristics
   cd ontology-defect-heuristics
   ```

2. Follow the installation and running instructions in the ontology-defect-heuristics repository's README.

3. Ensure ontology-defect-heuristics is running and accessible at the endpoint specified in your `.env` file (default: http://localhost:8085/defectCandidates).

## Usage

1. Ensure PROCK (ontology-defect-heuristics) is running locally and OOPS! service is accessible.

2. Start the Flask application:
   ```
   python app.py
   ```

3. The API will be available at `http://localhost:5000`.

4. Access the Swagger UI documentation at `http://localhost:5000/` for detailed information about the available endpoints and how to use them.

5. The API provides the following main endpoints:
   - `/analysis/analyze_ontology`: Analyzes an ontology file and related PDF document (Requires both PDF and the Ontology)
   - `/ontology/ontology_metrics`: Calculates metrics for an ontology file (Requires only the ontology)
   - `/document/extract_document`: Extracts information from a PDF document (Requires only the PDF)
   - `/error_checking/check_prock`: Performs PROCK error checking on an ontology
   - `/error_checking/check_oops`: Performs OOPS! error checking on an ontology

6. Example usage with curl:
   
   a. Analyze ontology and document:
   ```
   curl -X POST -F "ontology=@path/to/your/ontology.ttl" -F "document=@path/to/your/document.pdf" http://localhost:5000/analysis/analyze_ontology
   ```
   
   b. Calculate ontology metrics:
   ```
   curl -X POST -F "ontology=@path/to/your/ontology.ttl" http://localhost:5000/ontology/ontology_metrics
   ```
   
   c. Extract document information:
   ```
   curl -X POST -F "document=@path/to/your/document.pdf" http://localhost:5000/document/extract_document
   ```
   
   d. Perform PROCK error checking:
   ```
   curl -X POST -F "ontology=@path/to/your/ontology.ttl" http://localhost:5000/error_checking/check_prock
   ```
   
   e. Perform OOPS! error checking:
   ```
   curl -X POST -F "ontology=@path/to/your/ontology.ttl" http://localhost:5000/error_checking/check_oops
   ```


## Project Structure

```
ontology-analysis/
│
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── analysis_routes.py
│       ├── document_routes.py
│       ├── error_checking_routes.py
│       └── ontology_routes.py
│
├── error_checking/
│   ├── __init__.py
│   ├── oops_checker.py
│   └── prock_checker.py
│
├── models/
│   ├── document_processor.py
│   └── ontology_metrics.py
│
├── services/
│   ├── document_processor.py
│   ├── error_checker.py
│   └── ontology_processor.py
│
├── utils/
│   └── rdf_utils.py
│
├── app.py
├── config.py
├── extensions.py
└── requirements.txt
```

- `app.py`: Main application file, creates and runs the Flask app
- `config.py`: Configuration settings for the application
- `extensions.py`: Flask extensions initialization
- `api/`: Contains API routes and endpoint definitions
- `error_checking/`: Implementations for PROCK and OOPS! error checkers
- `models/`: Core logic for document processing and ontology metrics
- `services/`: Service layer implementations
- `utils/`: Utility functions for RDF processing

## Testing

You can use the `test_api.py` script to test the API endpoints:

```
python test_api.py --endpoint analyze --api-url http://localhost:5000 --ontology-path path/to/test_ontology.ttl --pdf-path path/to/test_document.pdf
```

Available options for `--endpoint` are: `metrics`, `document`, `analyze`, `check_prock`, and `check_oops`.

## Important Information

**CAUTION:** If your documents contain personal or sensitive information, ensure that you're using OLLAMA locally. This ensures that sensitive data remains on your local system and is not sent to external services.

## Future Work

- **Anonymization/Pseudonymization**: Implementing an option to automatically anonymize or pseudonymize personal data in documents before processing them with LLMs. This will add an extra layer of privacy protection.
- **Enhanced Error Checking**: Expand the error checking capabilities by integrating more tools and providing more detailed analysis of ontology issues.
- **Performance Optimization**: Improve the performance of ontology processing and document analysis for larger files.

## License

MIT

## Contact

Semantics Systems Group @ WU (https://semantic-systems.org/contact/)