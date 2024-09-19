from flask_restx import Resource, fields, Namespace
from werkzeug.datastructures import FileStorage
from services.error_checker import ErrorChecker

api = Namespace('error_checking', description='Error checking operations')

ontology_upload = api.parser()
ontology_upload.add_argument('ontology', location='files', type=FileStorage, required=True)

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

@api.route('/check_prock')
class CheckPROCKResource(Resource):
    @api.doc(description='Perform PROCK error check on an ontology')
    @api.expect(ontology_upload)
    @api.response(200, 'Success', fields.List(fields.Nested(prock_error_model)))
    @api.response(400, 'Validation Error')
    @api.response(500, 'Internal Server Error')
    def post(self):
        args = ontology_upload.parse_args()
        ontology_file = args['ontology']
        
        if not ontology_file.filename.endswith('.ttl'):
            api.abort(400, "Ontology file must be in Turtle format (.ttl)")
        
        prock_errors = ErrorChecker.check_prock(ontology_file)
        if prock_errors is None:
            api.abort(500, "Error processing ontology with PROCK")
        
        return prock_errors

@api.route('/check_oops')
class CheckOOPSResource(Resource):
    @api.doc(description='Perform OOPS! error check on an ontology')
    @api.expect(ontology_upload)
    @api.response(200, 'Success', fields.List(fields.Nested(oops_error_model)))
    @api.response(400, 'Validation Error')
    @api.response(500, 'Internal Server Error')
    def post(self):
        args = ontology_upload.parse_args()
        ontology_file = args['ontology']
        
        if not ontology_file.filename.endswith('.ttl'):
            api.abort(400, "Ontology file must be in Turtle format (.ttl)")
        
        oops_errors = ErrorChecker.check_oops(ontology_file)
        if oops_errors is None:
            api.abort(500, "Error processing ontology with OOPS!")
        
        return oops_errors