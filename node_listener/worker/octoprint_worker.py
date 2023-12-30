from node_listener.worker import Worker
import requests
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.octoprint import OctoprintApi
import node_listener.model.printer3d_model as model
from node_listener.service.debug_interface import DebugInterface
import logging
logger = logging.getLogger(__name__)


class OctoprintWorker(Worker, DebugInterface):
    def __init__(self, config):
        if type(config) is not dict:
            raise ValueError("config must be a dict")
        self.printer = None
        self._debug_name = config["debug_name"]
        self.printer = OctoprintApi(config["node_name"], config["url"], config["key"])
        Dump.module_status({'name': self.debug_name(), 'status': 2})
        self._initialize(self.printer)

    def _initialize(self, octoprint):
        try:
            response = octoprint.get('/version')
            if response.status_code == 403:
                octoprint.status.message = "Invalid credentials" # for " + octoprint.name
                octoprint.status.unrecoverable = True
                return
            response_json = response.json()
            octoprint.version = response_json['text']

            response = octoprint.get('/connection')
            response_json = response.json()

            octoprint.connection['port'] = response_json['current']['port']
            octoprint.connection['baudrate'] = response_json['current']['baudrate']

            octoprint.status.initialized = True
            octoprint.status.message = ''
        except requests.exceptions.ConnectionError as e:
            Dump.module_status({'name': self.debug_name(), 'status': 4})
            octoprint.status.message = "no connection"
        except Exception as e:
            Dump.module_status({'name': self.debug_name(), 'status': 5})
            octoprint.status.unrecoverable = True
            octoprint.status.message = str(e)

    def _get_data_model(self, octoprint):
        data = model.get_data()
        data['type'] = 'octoprint'
        data['connection'] = octoprint.connection
        data['version'] = octoprint.version

        return data

    def _get_data(self, octoprint):
        data = self._get_data_model(octoprint)

        if octoprint.status.unrecoverable:
            data['status'] = 'ERROR'
            data['error'] = True
            data['error_message'] = octoprint.status.message
            octoprint.clear_connection()
        elif not octoprint.status.initialized:
            data['status'] = 'ERROR'
            data['error'] = True
            data['error_message'] = octoprint.status.message
            self._initialize(octoprint)
        elif not data['connection']['port']:
            data['status'] = 'D/C'
            data['error_message'] = 'disconnected'
            data['error'] = True
            self._initialize(octoprint)
        else:
            try:
                response = octoprint.get('/printer')
                if response.status_code == 409:
                    response_json = response.json()
                    data['status'] = response_json['error']
                    octoprint.clear_connection()
                    data['error'] = True
                elif response.status_code == 200:
                    response_json = response.json()
                    data['status'] = response_json['state']['text']
                    data['flags'] = response_json['state']['flags']
                    data['bed'] = {
                        'actual': response_json['temperature']['bed']['actual'] if 'bed' in response_json['temperature'] else '',
                        'target': response_json['temperature']['bed']['target'] if 'bed' in response_json['temperature'] else '',
                    }

                    for i in range(0, 2):
                        key = "tool"+str(i)
                        if key in response_json['temperature']:
                            noozle = {
                                'actual': response_json['temperature'][key]['actual'],
                                'target': response_json['temperature'][key]['target'],
                            }
                            data['nozzle'].append(noozle)

                    if data['status'] == "Printing":
                        response = octoprint.get('/job')
                        response_json = response.json()
                        job = {
                            'name': response_json['job']['file']['display'],
                            'completion': (response_json['progress']['completion']) if response_json['progress']['completion'] else 0,
                            'printTime': round(response_json['progress']['printTime']) if response_json['progress']['printTime'] else 0,
                            'printTimeLeft': round(response_json['progress']['printTimeLeft']) if response_json['progress']['printTimeLeft'] else 0,

                        }
                        data['print'] = job

                else:
                    data['status'] = 'unknown'
                    data['error'] = True

            except requests.exceptions.ConnectionError as e:
                Dump.module_status({'name': self.debug_name(), 'status': 4})
                octoprint.status.message = str(e)
                octoprint.status.error = True
                octoprint.status.initialized = False
                octoprint.version = None
                octoprint.clear_connection()
                data['status'] = 'ERROR'
                data['error'] = True
                data['error_message'] = octoprint.status.message
            except Exception as e:
                Dump.module_status({'name': self.debug_name(), 'status': 4})
                octoprint.status.message = str(e)
                octoprint.status.error = True
                octoprint.status.initialized = False
                octoprint.version = None
                octoprint.clear_connection()
                data['status'] = 'ERROR'
                data['error'] = True
                data['error_message'] = octoprint.status.message

        data['connection'] = octoprint.connection

        return data

    def execute(self):
        """return data"""
        return self._get_data(self.printer)

    def debug_name(self):
        return self._debug_name
