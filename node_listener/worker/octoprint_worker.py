from node_listener.worker import Worker
import requests
from node_listener.service.hd44780_40_4 import Dump


class Status:
    def __init__(self):
        self.message = None
        self.error = False
        self.initialized = False
        self.unrecoverable = False


class OctoprintApi:
    def __init__(self, name, url, token):
        self.name = name
        self.url = url
        self.token = token
        self.status = Status()
        self.version = None
        self.connection = {
            'port': None,
            'baudrate': None
        }

    def clear_connection(self):
        self.connection = {
            'port': None,
            'baudrate': None
        }

    def get(self, uri):
        headers = {'X-Api-Key': self.token}
        return requests.get(self.url+uri, headers=headers)

    def post(self, uri, data):
        headers = {
            'X-Api-Key': self.token,
            'Content-Type': 'application/json',
        }
        return requests.post(self.url+uri, json=data, headers=headers)


class OctoprintWorker(Worker):
    def __init__(self, octoprints):
        if type(octoprints) is not dict:
            raise ValueError("octoprints must be a dict")
        self.octoprints = {}
        Dump.module_status({'name': 'Octo', 'status': 2})
        for name in octoprints:
            octoprint = OctoprintApi(name, octoprints[name][1], octoprints[name][0])
            self._initialize(octoprint)
            self.octoprints[name] = octoprint

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
            Dump.module_status({'name': 'Octo', 'status': 4})
            octoprint.status.message = "no connection"
        except Exception as e:
            Dump.module_status({'name': 'Octo', 'status': 5})
            octoprint.status.unrecoverable = True
            octoprint.status.message = str(e)

    def _get_data(self, octoprint):
        data = {
            'connection': octoprint.connection,
            'octoprint': octoprint.version,
            'status': '',
            'flags': [],
            'nozzle': [],
            'bed': {
                'actual': '',
                'target': '',
            },
            'error': False,
            'error_message': '',
            'print': ''
        }

        if octoprint.status.unrecoverable:
            data['status'] = 'ERROR'
            data['error'] = True
            data['error_message'] = octoprint.status.message
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
                    data['print'] = {}
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
                Dump.module_status({'name': 'Octo', 'status': 4})
                octoprint.status.message = str(e)
                octoprint.status.error = True
                octoprint.status.initialized = False
                octoprint.version = None
                octoprint.connection = {
                    'port': None,
                    'baudrate': None
                }
                data['status'] = 'ERROR'
                data['error'] = True
                data['error_message'] = octoprint.status.message
            except Exception as e:
                Dump.module_status({'name': 'Octo', 'status': 4})
                octoprint.status.message = str(e)
                octoprint.status.error = True
                octoprint.status.initialized = False
                octoprint.version = None
                octoprint.connection = {
                    'port': None,
                    'baudrate': None
                }
                data['status'] = 'ERROR'
                data['error'] = True
                data['error_message'] = octoprint.status.message

        return data

    def execute(self):
        """return data"""
        data = {}
        for name in self.octoprints:
            data[name] = self._get_data(self.octoprints[name])
            # print(data[name])

        return data

