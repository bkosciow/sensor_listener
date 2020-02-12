import time
from node_listener.storage.storage import Storage
from node_listener.storage.dictionary_engine import DictionaryEngine
from node_listener.scheduler.task import Task
from node_listener.service.sensor_listener import SensorListener
from node_listener.service.config import Config

config = Config('../../config.ini')

Storage.set_engine(DictionaryEngine())
storage = Storage()

Task.set_storage(storage)

serverSensor = SensorListener(storage, config)
serverSensor.start()

while True:
    print("****************")
    # pprint.pprint(storage.get_all())
    time.sleep(2)

