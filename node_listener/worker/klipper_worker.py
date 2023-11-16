from node_listener.worker import Worker
import requests
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.klipper import KlipperApi
import node_listener.model.printer3d_model as model


class KlipperWorker(Worker):
    def __init__(self, configs):
        if type(configs) is not dict:
            raise ValueError("octoprints must be a dict")
        self.printers = {}
        Dump.module_status({'name': 'Klipp', 'status': 2})

        for name in configs:
            klipper = KlipperApi(name, configs[name][0])
            self._initialize(klipper)
            self.printers[name] = klipper

    def _initialize(self, klipper):
        try:
            response = klipper.get('/machine/update/status?refresh=false')
            response_json = response.json()
            klipper.version = response_json['result']['version_info']['klipper']['version']

            response = klipper.get('/printer/info')
            response_json = response.json()
            if response_json['result']['state'] == "ready":
                klipper.connection['port'] = "default"
                klipper.connection['baudrate'] = "default"

            klipper.status.initialized = True
            klipper.status.message = ''
        except requests.exceptions.ConnectionError as e:
            Dump.module_status({'name': 'Klipp', 'status': 4})
            klipper.status.message = "no connection"
        except Exception as e:
            raise e
            Dump.module_status({'name': 'Klipp', 'status': 5})
            klipper.status.unrecoverable = True
            klipper.status.message = str(e)

    def _get_data(self, klipper):
        data = model.get_data()
        data['connection'] = klipper.connection
        data['version'] = klipper.version
        data['type'] = 'klipper'


        if klipper.status.unrecoverable:
            data['status'] = 'ERROR'
            data['error'] = True
            data['error_message'] = klipper.status.message
            klipper.clear_connection()
        elif not klipper.status.initialized:
            data['status'] = 'ERROR'
            data['error'] = True
            data['error_message'] = klipper.status.message
            self._initialize(klipper)
        elif not data['connection']['port']:
            data['status'] = 'D/C'
            data['error_message'] = 'disconnected'
            data['error'] = True
            self._initialize(klipper)
        else:
            data['status'] = 'Operational'
            pass

        return data

    def execute(self):
        """return data"""
        data = {}
        for name in self.printers:
            data[name] = self._get_data(self.printers[name])

        print(data)

        return data

