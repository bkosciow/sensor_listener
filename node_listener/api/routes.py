from sqlalchemy import Column, Integer, String, DateTime, func
from flask import Flask, request, jsonify
from node_listener.api.model.node import NodeModel
from sqlalchemy.ext.declarative import declarative_base
from functools import wraps
from node_listener.service.comm import send
import logging

logger = logging.getLogger(__name__)
Base = declarative_base()
API_TOKEN = None


def require_token(f):
    @wraps(f)  # Preserves the original function's metadata
    def decorated_function(*args, **kwargs):
        token = request.headers.get("X-API-Token")
        print(token)
        if token != API_TOKEN or API_TOKEN is None:
            return jsonify({"message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function


def init_api(app, cfg, storage):
    import node_listener.api.db_helper as db_helper
    global API_TOKEN
    API_TOKEN = cfg.get("api_key")
    db_helper.cfg = cfg
    db_helper.Base = Base
    db_helper.check_and_create_tables()

    @app.route("/api/nodes/ping")
    @require_token
    def ping():
        msg = {'event': "system.ping"}
        send(msg)

        return '', 204

    @app.route("/api/node/<int:node_id>/ping")
    @require_token
    def node_ping(node_id):
        try:
            db = next(db_helper.get_db())
            node = db.query(NodeModel).get(node_id)
            if node is None:
                return '', 404
            msg = {'event': "system.ping", "target": [node.node_name]}
            send(msg)
            return '', 204

        except Exception as e:
            print(f"Error pinging node {node_id}: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/nodes/microplate/hash")
    @require_token
    def hash_microplate():
        msg = {'event': "system.microplate.get_hash"}
        send(msg)

        return '', 204

    @app.route("/api/node/<int:node_id>/microplate/hash")
    @require_token
    def node_hash_microplate(node_id):
        try:
            db = next(db_helper.get_db())
            node = db.query(NodeModel).get(node_id)
            if node is None:
                return '', 404
            msg = {'event': "system.microplate.get_hash", "target": [node.node_name]}
            send(msg)
            return '', 204
        except Exception as e:
            print(f"Error pinging node {node_id}: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/nodes/userspace/hash")
    @require_token
    def hash_userspace():
        msg = {'event': "system.userspace.get_hash"}
        send(msg)

        return '', 204

    @app.route("/api/node/<int:node_id>/userspace/hash")
    @require_token
    def node_hash_userspace(node_id):
        try:
            db = next(db_helper.get_db())
            node = db.query(NodeModel).get(node_id)
            if node is None:
                return '', 404
            msg = {'event': "system.userspace.get_hash", "target": [node.node_name]}
            send(msg)
            return '', 204
        except Exception as e:
            print(f"Error pinging node {node_id}: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/nodes")
    @require_token
    def nodes():
        try:
            db = next(db_helper.get_db())
            nodes_list = db.query(NodeModel).all()
            nodes_data = []
            for node in nodes_list:
                node_data = {
                    "id": node.id,
                    "node_name": node.node_name,
                    "node_id": node.node_id,
                    "node_system": node.node_system,
                    "node_micropython_hash": node.node_micropython_hash,
                    "node_userspace_hash": node.node_userspace_hash,
                    "updated_at": str(node.updated_at),  # Convert datetime to string
                    "created_at": str(node.created_at),  # Convert datetime to string
                }
                nodes_data.append(node_data)
            return jsonify(nodes_data)
        except Exception as e:
            logger.error(f"Error fetching nodes: {e}")
            return jsonify({"error": str(e)}), 500
