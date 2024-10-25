import json
from node_listener.worker import Worker
import urllib
import urllib.error
import urllib.request
import urllib.parse
import node_listener.service.air_pollution as air
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.debug_interface import DebugInterface
import logging
logger = logging.getLogger(__name__)


class OpenaqWorker(Worker, DebugInterface):
    url = "https://api.openaq.org/v1/latest?"

    def __init__(self, params):
        self.apikey = params['apikey'] if params['apikey'] != "" else None
        self.city = params['city'] if params['city'] != "" else None
        self.location = params['location'] if params['location'] != "" else None
        self.user_agent = params['user_agent']
        self._validate()

    def debug_name(self):
        return 'opnAQ'

    def _validate(self):
        if self.city is None and self.location is None:
            raise AttributeError("city or location must be set")
        if self.apikey is None:
            raise AttributeError("apikey must be set")

    def _fetch_data(self, url):
        try:
            request = urllib.request.Request(
                url, None, {
                    'User-Agent': self.user_agent,
                    'X-API-Key': self.apikey,
                }
            )
            response = urllib.request.urlopen(request)
            data = response.read()
            json_data = json.loads(data.decode())
            Dump.module_status({'name': self.debug_name(), 'status': 2})
        except ValueError as e:
            logger.warning(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except urllib.error.HTTPError as e:
            logger.warning(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except urllib.error.URLError as e:
            logger.warning(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except ConnectionResetError as e:
            logger.warning(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except Exception as e:
            logger.critical(str(e))
            Dump.module_status({'name': self.debug_name(), 'status': 5})
            raise

        return json_data

    def _get_url(self):
        url = self.url
        if self.city is not None:
            url = url + "city="+urllib.parse.quote(self.city)

        if self.location is not None:
            if self.city is not None:
                url = url+"&"
            url = url + "location="+urllib.parse.quote(self.location)

        return url

    def _normalize(self, data):
        values = {}
        for entry in data['results']:
            values[entry['location']] = {
                "PM10": None,
                "PM25": None,
                "CO": None,
                "O3": None,
                "SO2": None,
                "NO2": None,
                "BC": None
            }
            for measurement in entry['measurements']:
                if measurement['parameter'] == "pm10":
                    values[entry['location']]["PM10"] = {
                        'index': air.air_index_pm10(measurement["value"]),
                        'date': measurement['lastUpdated']
                    }

                if measurement['parameter'] == "pm25":
                    values[entry['location']]["PM25"] = {
                        'index': air.air_index_pm25(measurement["value"]),
                        'date': measurement['lastUpdated']
                    }

                if measurement['parameter'] == "co":
                    values[entry['location']]["CO"] = {
                        'index': air.air_index_co(measurement["value"]),
                        'date': measurement['lastUpdated']
                    }

                if measurement['parameter'] == "so2":
                    values[entry['location']]["SO2"] = {
                        'index': air.air_index_so2(measurement["value"]),
                        'date': measurement['lastUpdated']
                    }

                if measurement['parameter'] == "no2":
                    values[entry['location']]["NO2"] = {
                        'index': air.air_index_no2(measurement["value"]),
                        'date': measurement['lastUpdated']
                    }

                if measurement['parameter'] == "o3":
                    values[entry['location']]["O3"] = {
                        'index': air.air_index_o3(measurement["value"]),
                        'date': measurement['lastUpdated']
                    }

                if measurement['parameter'] == "bc":
                    values[entry['location']]["BC"] = {
                        'index': air.air_index_so2(measurement["value"]),
                        'date': measurement['lastUpdated']
                    }

        return values

    def execute(self):
        data = self._fetch_data(self._get_url())
        if data:
            return self._normalize(data)

        return {}
