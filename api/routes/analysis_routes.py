from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from services.ontology_processor import OntologyProcessor
from services.document_processor import DocumentProcessor
from services.error_checker import ErrorChecker

api = Namespace('analysis', description='Combined analysis operations')

analysis_upload = api.parser()
analysis_upload.add_argument('ontology', location='files', type=FileStorage, required=True)
analysis_upload.add_argument('document', location='files', type=FileStorage, required=True)

prock_error_model = api.model('PROCKError', {
    'name': fields.String(description='Name of the error'),
    'candidates': fields.List(fields.Raw(description='Error candidates'))
})

oops_error_model = api.model('OOPSError', {
    'name': fields.String(description='Name of the error'),
    'description': fields.String(description='Description of the error'),
    'importanceLevel': fields.String(description='Importance level of the error'),
    'code': fields.String(description='Error code'),
    'numberAffectedElements': fields.Integer(description='Number of affected elements')
})

ontology_analysis_model = api.model('OntologyAnalysis', {
    'ontology_description': fields.String(description='Description of the ontology'),
    'application_domain': fields.String(description='Application domain of the ontology'),
    'competency_questions': fields.List(fields.String, description='List of competency questions'),
    'ontology_metrics': fields.Raw(description='Metrics of the ontology'),
    'prock_errors': fields.List(fields.Nested(prock_error_model), description='PROCK errors'),
    'oops_errors': fields.List(fields.Nested(oops_error_model), description='OOPS! errors')
})

@api.route('/analyze_ontology')
class AnalyzeOntologyResource(Resource):
    @api.doc(description='Analyze ontology, extract information from a document, and perform error checks')
    @api.expect(analysis_upload)
    @api.response(200, 'Success', ontology_analysis_model)
    @api.response(400, 'Validation Error')
    @api.response(500, 'Internal Server Error')
    def post(self):
        args = analysis_upload.parse_args()
        ontology_file = args['ontology']
        document_file = args['document']

        if not ontology_file.filename.endswith('.ttl'):
            api.abort(400, "Ontology file must be in Turtle format (.ttl)")

        if not document_file.filename.endswith('.pdf'):
            api.abort(400, "Document file must be in PDF format (.pdf)")

        # Process ontology
        metrics, ontology_error = OntologyProcessor.process_ontology(ontology_file)
        if ontology_error:
            api.abort(500, f"Error processing ontology: {ontology_error}")

        # Process document
        document_data, document_error = DocumentProcessor.process_document(document_file)
        if document_error:
            api.abort(500, f"Error processing document: {document_error}")

        # Perform error checks
        prock_errors = ErrorChecker.check_prock(ontology_file)
        oops_errors = ErrorChecker.check_oops(ontology_file)

        result = {
            "ontology_description": document_data.get('ontology_description', ''),
            "application_domain": document_data.get('application_domain', ''),
            "competency_questions": document_data.get('competency_questions', []),
            "ontology_metrics": metrics,
            "prock_errors": prock_errors,
            "oops_errors": oops_errors
        }

        return result