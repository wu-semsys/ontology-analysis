from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp,
          title='Ontology Analysis API',
          version='1.0',
          description='API for analyzing ontologies, extracting information from documents, and performing error checks',
          doc='/')  # This line ensures Swagger UI is at the root

from .routes.ontology_routes import api as ontology_ns
from .routes.document_routes import api as document_ns
from .routes.error_checking_routes import api as error_checking_ns
from .routes.analysis_routes import api as analysis_ns

api.add_namespace(ontology_ns, path='/ontology')
api.add_namespace(document_ns, path='/document')
api.add_namespace(error_checking_ns, path='/error_checking')
api.add_namespace(analysis_ns, path='/analysis')