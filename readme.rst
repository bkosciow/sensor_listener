Handlers:

- node_one_handler
- 3D printer

get storage by default and calls set_params on it
can have more workers, calls set_params on them

Workers:

- Openweather
- OpenAQ
- GIOŚ

Start:
node_listener/server.py

Serve

- via gRPC

    from node_listener.grpc.storage_pb2_grpc import *
    from node_listener.grpc.storage_pb2 import *
    import json

    channel = grpc.insecure_channel('localhost:8765')
    stub = ProviderStub(channel)


    for response in stub.get_changes(EmptyRequest()):
        print(response)


## Run as a service (pi user)

- Copy sensor_listener.service to /lib/systemd/system/sensor_listener.service

- chmod 0644 /lib/systemd/system/sensor_listener.service

- systemctl start sensor_listener