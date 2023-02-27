from node_listener.worker import Worker
import requests
from node_listener.service.hd44780_40_4 import Dump


class OctoprintApi:
    def __init__(self, name, url, token):
        self.name = name
        self.url = url
        self.token = token


class OctoprintWorker(Worker):
    def __init__(self, octoprints):
        if type(octoprints) is not dict:
            raise ValueError("octoprints must be a dict")

        self.octoprints = {}
        Dump.module_status({'name': 'Octo', 'status': 2})
        for name in octoprints:
            octoprint = OctoprintApi(name, octoprints[name][1], octoprints[name][0])
            self._validate_credentials(octoprint)
            self.octoprints[name] = octoprint


    def _validate_credentials(self, octoprint):
        try:
            response = self._get(octoprint, '/printer')
            if response.status_code == 403:
                raise ValueError("Invalid credentials for " + octoprint.name)
        except requests.exceptions.ConnectionError as e:
            Dump.module_status({'name': 'Octo', 'status': 4})
        except:
            Dump.module_status({'name': 'Octo', 'status': 5})
            raise

    def _get(self, octoprint, uri):
        headers = {'X-Api-Key': octoprint.token}
        return requests.get(octoprint.url+uri, headers=headers)

    def _get_data(self, octoprint):
        data = {
            'status': '',
            'flags': [],
            'nozzle': [],
            'bed': {
                'actual': '',
                'target': '',
            },
            'error': False,
            'print': ''
        }
        try:
            response = self._get(octoprint, '/printer')
            if response.status_code == 409:
                response_json = response.json()
                data['status'] = response_json['error']
                data['error'] = True
            elif response.status_code == 200:
                response_json = response.json()
                data['status'] = response_json['state']['text']
                data['flags'] = response_json['state']['flags']
                data['bed'] = {
                    'actual': response_json['temperature']['bed']['actual'] if 'bed' in response_json['temperature'] else '',
                    'target': response_json['temperature']['bed']['target'] if 'bed' in response_json['temperature'] else '',
                }
                data['print'] = []
                for i in range(0, 2):
                    key = "tool"+str(i)
                    if key in response_json['temperature']:
                        noozle = {
                            'actual': response_json['temperature'][key]['actual'],
                            'target': response_json['temperature'][key]['target'],
                        }
                        data['nozzle'].append(noozle)

                if data['status'] == "Printing":
                    response = self._get(octoprint, '/job')
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
            data['status'] = 'exception'
            data['error'] = True
        except:
            Dump.module_status({'name': 'Octo', 'status': 5})
            data['status'] = 'exception'
            data['error'] = True

        return data

    def execute(self):
        """return data"""
        data = {}
        for name in self.octoprints:
            data[name] = self._get_data(self.octoprints[name])

        return data

