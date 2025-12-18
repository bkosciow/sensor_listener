import logging


logger = logging.getLogger(__name__)


def init_api(app, cfg, storage):
    @app.route("/api/keys")
    def ping():
        """

        """

        return '', 204
