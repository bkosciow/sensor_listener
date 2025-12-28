import logging
import flask
from flask import jsonify


logger = logging.getLogger(__name__)


def init_api(app, cfg, storage):
    @app.route("/api/keys")
    def get_keys():
        """
        """
        data = storage.get_all()

        return jsonify({"keys": list(data.keys())})


    @app.route("/api/key/<key>")
    def get_key(key):
        """
        Get data for a specific key
        """
        try:
            data = storage.get(key)
            if data is None:
                return jsonify({"error": "Key not found"}), 404
            return jsonify({"key": key, "value": data}), 200
        except Exception as e:
            logger.error(f"Error retrieving key {key}: {e}")
            return jsonify({"error": "Internal server error"}), 500

