from flask_restx import Resource, fields
from werkzeug.datastructures import FileStorage
from services.document_processor import DocumentProcessor
from api import api

document_upload = api.parser()
document_upload.add_argument('document', location='files', type=FileStorage, required=True)

document_extract_model = api.model('DocumentExtract', {
    'ontology_description': fields.String(description='Description of the ontology'),
    'application_domain': fields.String(description='Application domain of the ontology'),
    'competency_questions': fields.List(fields.String, description='List of competency questions')
})

@api.route('/extract_document')
class ExtractDocumentResource(Resource):
    @api.doc(description='Extract information from a document file')
    @api.expect(document_upload)
    @api.response(200, 'Success', document_extract_model)
    @api.response(400, 'Validation Error')
    @api.response(500, 'Internal Server Error')
    def post(self):
        args = document_upload.parse_args()
        document_file = args['document']
        
        if not document_file.filename.endswith('.pdf'):
            api.abort(400, "Document file must be in PDF format (.pdf)")
        
        result, error = DocumentProcessor.process_document(document_file)
        
        if error:
            api.abort(500, f"Error processing document: {error}")
        
        return result