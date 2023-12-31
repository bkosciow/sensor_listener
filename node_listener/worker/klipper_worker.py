from node_listener.worker import Worker
import requests
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.klipper import KlipperApi
import node_listener.model.printer3d_model as model
from node_listener.service.debug_interface import DebugInterface
import logging
logger = logging.getLogger(__name__)


class KlipperWorker(Worker, DebugInterface):
    def __init__(self, config):
        if type(config) is not dict:
            raise ValueError("config must be a dict")
        self.printer = None
        self._debug_name = config["debug_name"]
        self.printer = KlipperApi(config["node_name"], config["url"])
        self._initialize(self.printer)
        Dump.module_status({'name': self.debug_name(), 'status': 2})

    def debug_name(self):
        return self._debug_name

    def _initialize(self, klipper):
        try:
            response = klipper.get('/machine/update/status?refresh=false')
            response_json = response.json()
            klipper.version = response_json['result']['version_info']['klipper']['version']

            response = klipper.get('/printer/info')
            if response.status_code == 503:
                Dump.module_status({'name': self.debug_name(), 'status': 4})
                klipper.status.message = "booting"

            if response.status_code == 200:
                response_json = response.json()
                if response_json['result']['state'] == "ready":
                    klipper.connection['port'] = "default"
                    klipper.connection['baudrate'] = "default"

                klipper.status.initialized = True
                klipper.status.message = ''
        except requests.exceptions.ConnectionError as e:
            Dump.module_status({'name': self.debug_name(), 'status': 4})
            klipper.status.message = "no connection"
        except Exception as e:
            Dump.module_status({'name': self.debug_name(), 'status': 5})
            klipper.status.unrecoverable = True
            klipper.status.message = str(e)

    def _get_data_model(self, klipper):
        data = model.get_data()
        data['connection'] = klipper.connection
        data['version'] = klipper.version
        data['type'] = 'klipper'
        data['config']['connect_panel'] = False
        data['flags'] = {
            'paused': False,
            'pausing': False,
            'printing': False,
        }

        return data

    def _get_data(self, klipper):
        data = self._get_data_model(klipper)

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
            try:
                response = klipper.get('/printer/objects/query?print_stats&display_status&heater_bed&extruder&toolhead')
                if response.status_code == 200:
                    response_json = response.json()
                    data['status'] = response_json['result']['status']['print_stats']['state']
                    if data['status'] == "printing":
                        data['flags']['printing'] = True
                        data['print'] = {
                            'name': response_json['result']['status']['print_stats']['filename'],
                            'completion': round(response_json['result']['status']['display_status']['progress'], 2) * 100,
                            'printTime': round(response_json['result']['status']['print_stats']['total_duration'], 2),
                            'printTimeLeft': 0,
                        }
                        response = klipper.get('/server/files/metadata?filename='+response_json['result']['status']['print_stats']['filename'])
                        response_json_meta = response.json()
                        data['print']['printTimeLeft'] = round(response_json_meta['result']['estimated_time'] - response_json['result']['status']['display_status']['progress'], 2)
                    if data['status'] == "paused":
                        data['flags']['paused'] = True
                    data['bed'] = {
                        'actual': response_json['result']['status']['heater_bed']['temperature'],
                        'target': response_json['result']['status']['heater_bed']['target']
                    }
                    data['nozzle'].append(
                        {
                            'actual': response_json['result']['status']['extruder']['temperature'],
                            'target': response_json['result']['status']['extruder']['target']
                        }
                    )

                else:
                    response_json = response.json()
                    data['status'] = response_json['status']['message']
                    klipper.clear_connection()
                    data['error'] = True

            except requests.exceptions.ConnectionError as e:
                Dump.module_status({'name': self.debug_name(), 'status': 4})
                klipper.status.message = str(e)
                klipper.status.error = True
                klipper.status.initialized = False
                klipper.version = None
                klipper.clear_connection()
                data['status'] = 'ERROR'
                data['error'] = True
                data['error_message'] = klipper.status.message
            except Exception as e:
                Dump.module_status({'name': self.debug_name(), 'status': 4})
                klipper.status.message = str(e)
                klipper.status.error = True
                klipper.status.initialized = False
                klipper.version = None
                klipper.clear_connection()
                data['status'] = 'ERROR'
                data['error'] = True
                data['error_message'] = klipper.status.message

        data['connection'] = klipper.connection

        return data

    def execute(self):
        """return data"""
        return self._get_data(self.printer)
        # data = {}
        # for name in self.printers:
        #     data[name] = self._get_data(self.printers[name])
        #
        # return data

