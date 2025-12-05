import json
from node_listener.worker import Worker
import urllib
import urllib.error
import urllib.request
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.debug_interface import DebugInterface
from pprint import pprint
import http
import logging
logger = logging.getLogger(__name__)


class GiosWorker(Worker, DebugInterface):
    url = "https://api.gios.gov.pl/pjp-api/v1/rest/aqindex/getIndex/%STATION_ID%"

    def __init__(self, params):
        self.station_id = params['station_id']
        self.user_agent = params['user_agent']

    def debug_name(self):
        return 'gios'

    def _fetch_data(self, url):
        """fetch json data from server"""
        try:
            request = urllib.request.Request(
                url, None, {'User-Agent': self.user_agent}
            )
            response = urllib.request.urlopen(request)
            data = response.read()
            json_data = json.loads(data.decode())
            if json_data is not None:
                json_data = json_data['AqIndex']
                Dump.module_status({'name': self.debug_name(), 'status': 2})
        except ValueError as e:
            logger.error(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except urllib.error.HTTPError as e:
            logger.error(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except urllib.error.URLError as e:
            logger.error(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except http.client.RemoteDisconnected as e:
            logger.error(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except ConnectionResetError as e:
            logger.error(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except Exception as e:
            logger.critical(str(e))
            Dump.module_status({'name': self.debug_name(), 'status': 5})
            raise

        return json_data

    def _normalize(self, data):
        values = {
            "PM10": None,
            "PM25": None,
            "CO": None,
            "O3": None,
            "SO2": None,
            "NO2": None,
            "BC": None
        }
        if "Wartość indeksu dla wskaźnika PM10" in data and data["Wartość indeksu dla wskaźnika PM10"] is not None:
            values["PM10"] = {
                "index": data["Wartość indeksu dla wskaźnika PM10"],
                "date": data["Data wykonania obliczeń indeksu dla wskaźnika PM10"],
            }

        if "Wartość indeksu dla wskaźnika PM2.5" in data and data["Wartość indeksu dla wskaźnika PM2.5"] is not None:
            values["PM25"] = {
                "index": data["Wartość indeksu dla wskaźnika PM2.5"],
                "date": data["Data wykonania obliczeń indeksu dla wskaźnika PM2.5"],
            }

        # if "coIndexLevel" in data and data["coIndexLevel"] is not None:
        #     values["CO"] = {
        #         "index": data["coIndexLevel"]["id"],
        #         "date": data["coSourceDataDate"],
        #     }

        if "Wartość indeksu dla wskaźnika SO2" in data and data["Wartość indeksu dla wskaźnika SO2"] is not None:
            values["SO2"] = {
                "index": data["Wartość indeksu dla wskaźnika SO2"],
                "date": data["Data wykonania obliczeń indeksu dla wskaźnika SO2"],
            }

        if "Wartość indeksu dla wskaźnika NO2" in data and data["Wartość indeksu dla wskaźnika NO2"] is not None:
            values["NO2"] = {
                "index": data["Wartość indeksu dla wskaźnika NO2"],
                "date": data["Data wykonania obliczeń indeksu dla wskaźnika NO2"],
            }

        if "Wartość indeksu dla wskaźnika O3" in data and data["Wartość indeksu dla wskaźnika O3"] is not None:
            values["O3"] = {
                "index": data["Wartość indeksu dla wskaźnika O3"],
                "date": data["Data wykonania obliczeń indeksu dla wskaźnika O3"],
            }
        #
        # if "c6h6IndexLevel" in data and data["c6h6IndexLevel"] is not None:
        #     values["BC"] = {
        #         "index": data["c6h6IndexLevel"]["id"],
        #         "date": data["c6h6SourceDataDate"],
        #     }

        return values

    def execute(self):
        data = self._fetch_data(self.url.replace("%STATION_ID%", str(self.station_id)))

        return self._normalize(data) if data is not None else {}
