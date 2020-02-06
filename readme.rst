Handlers:

- node_one_handler

get storage by default and calls set_params on it
can have more workers, calls set_params on them

Workers:

- Openweather

reads weather conditions

- start server

    config = Config()

    Storage.set_engine(DictionaryEngine())
    storage = Storage()

    Task.set_storage(storage)

    serverSensor = SensorListener(storage, config)
    serverSensor.start()

