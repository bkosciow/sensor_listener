Handlers:

- node_one_handler
get storage by default and calls set_params on it
can have more workers, calls set_params on them

- start server

Storage.set_engine(DictionaryEngine())
serverSensor = SensorListener(Storage())