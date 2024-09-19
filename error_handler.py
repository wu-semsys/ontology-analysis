from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

    @app.errorhandler(503)
    def service_unavailable_error(error):
        return jsonify({"error": "Service Unavailable", "message": str(error)}), 503