from node_listener.storage.storage import Storage
import logging
from node_listener.service.config import Config
from flask import Flask
from node_api.api.routes import init_api


app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

config = Config('config.ini')

Storage.set_engine(config.get_storage_engine())
storage = Storage()

init_api(app, config['api'], storage)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(config.get('api.port')), use_reloader=False)
