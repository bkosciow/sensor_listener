Handlers:

- node_one_handler

get storage by default and calls set_params on it
can have more workers, calls set_params on them

Workers:

- Openweather
- OpenAQ
- GIOŚ

reads weather conditions

- start server

    import time
    from node_listener.storage.storage import Storage
    from node_listener.storage.dictionary_engine import DictionaryEngine
    from node_listener.scheduler.task import Task
    from node_listener.server import SensorListener
    from node_listener.service.config import Config

    config = Config()

    Storage.set_engine(DictionaryEngine())
    storage = Storage()

    Task.set_storage(storage)

    serverSensor = SensorListener(storage, config)
    serverSensor.start()


