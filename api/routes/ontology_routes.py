from flask_restx import Resource, fields
from werkzeug.datastructures import FileStorage
from services.ontology_processor import OntologyProcessor
from api import api

ontology_upload = api.parser()
ontology_upload.add_argument('ontology', location='files', type=FileStorage, required=True)

ontology_metrics_model = api.model('OntologyMetrics', {
    'ontology_metrics': fields.Raw(description='Metrics of the ontology')
})

@api.route('/ontology_metrics')
class OntologyMetricsResource(Resource):
    @api.doc(description='Get metrics for an ontology file')
    @api.expect(ontology_upload)
    @api.response(200, 'Success', ontology_metrics_model)
    @api.response(400, 'Validation Error')
    @api.response(500, 'Internal Server Error')
    def post(self):
        args = ontology_upload.parse_args()
        ontology_file = args['ontology']
        
        if not ontology_file.filename.endswith('.ttl'):
            api.abort(400, "Ontology file must be in Turtle format (.ttl)")
        
        metrics, error = OntologyProcessor.process_ontology(ontology_file)
        if error:
            api.abort(500, f"Error processing ontology: {error}")
        return {"ontology_metrics": metrics}
