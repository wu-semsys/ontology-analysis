import requests
import json
import argparse

def test_ontology_metrics(api_url, ontology_path):
    print("\nTesting /ontology/ontology_metrics endpoint:")
    files = {
        'ontology': ('test_ontology.ttl', open(ontology_path, 'rb'), 'text/turtle')
    }
    try:
        response = requests.post(f"{api_url}/ontology/ontology_metrics", files=files)
        print_response(response)
    finally:
        files['ontology'][1].close()

def test_extract_document(api_url, pdf_path):
    print("\nTesting /document/extract_document endpoint:")
    files = {
        'document': ('test_document.pdf', open(pdf_path, 'rb'), 'application/pdf')
    }
    try:
        response = requests.post(f"{api_url}/document/extract_document", files=files)
        print_response(response)
    finally:
        files['document'][1].close()

def test_analyze_ontology(api_url, ontology_path, pdf_path):
    print("\nTesting /analysis/analyze_ontology endpoint:")
    files = {
        'ontology': ('test_ontology.ttl', open(ontology_path, 'rb'), 'text/turtle'),
        'document': ('test_document.pdf', open(pdf_path, 'rb'), 'application/pdf')
    }
    try:
        response = requests.post(f"{api_url}/analysis/analyze_ontology", files=files)
        print_response(response)
    finally:
        for file in files.values():
            file[1].close()

def test_check_prock(api_url, ontology_path):
    print("\nTesting /error_checking/check_prock endpoint:")
    files = {
        'ontology': ('test_ontology.ttl', open(ontology_path, 'rb'), 'text/turtle')
    }
    try:
        response = requests.post(f"{api_url}/error_checking/check_prock", files=files)
        print_response(response)
    finally:
        files['ontology'][1].close()

def test_check_oops(api_url, ontology_path):
    print("\nTesting /error_checking/check_oops endpoint:")
    files = {
        'ontology': ('test_ontology.ttl', open(ontology_path, 'rb'), 'text/turtle')
    }
    try:
        response = requests.post(f"{api_url}/error_checking/check_oops", files=files)
        print_response(response)
    finally:
        files['ontology'][1].close()

def print_response(response):
    if response.status_code == 200:
        result = response.json()
        print("API Response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: API returned status code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Ontology Analysis API endpoints.")
    parser.add_argument('--endpoint', choices=['metrics', 'document', 'analyze', 'check_prock', 'check_oops'],
                        default='metrics', help="Specify which endpoint to test (default: metrics).")
    parser.add_argument('--api-url', default='http://localhost:5000',
                        help="The base URL of the API (default: http://localhost:5000)")
    parser.add_argument('--ontology-path', default='test_data/test_ontology.ttl',
                        help="Path to the test ontology file (default: test_data/test_ontology.ttl)")
    parser.add_argument('--pdf-path', default='test_data/test_document.pdf',
                        help="Path to the test PDF document (default: test_data/test_document.pdf)")
    
    args = parser.parse_args()

    try:
        if args.endpoint == 'metrics':
            test_ontology_metrics(args.api_url, args.ontology_path)
        elif args.endpoint == 'document':
            test_extract_document(args.api_url, args.pdf_path)
        elif args.endpoint == 'analyze':
            test_analyze_ontology(args.api_url, args.ontology_path, args.pdf_path)
        elif args.endpoint == 'check_prock':
            test_check_prock(args.api_url, args.ontology_path)
        elif args.endpoint == 'check_oops':
            test_check_oops(args.api_url, args.ontology_path)
    except requests.RequestException as e:
        print(f"An error occurred while making the request: {e}")