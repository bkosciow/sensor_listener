Handlers:

- node_one_handler
- 3D printer

get storage by default and calls set_params on it
can have more workers, calls set_params on them

Workers:

- Openweather
- OpenAQ
- GIOŚ
- Octoprint

Start:
node_listener/server.py

Serve

- via socket
## Run as a service (pi user)

- Copy sensor_listener.service to /lib/systemd/system/sensor_listener.service

- chmod 0644 /lib/systemd/system/sensor_listener.service

- systemctl start sensor_listener