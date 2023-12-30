import json
from node_listener.worker import Worker
import urllib
import urllib.error
import urllib.request
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.debug_interface import DebugInterface
import http
import logging
logger = logging.getLogger(__name__)


class GiosWorker(Worker, DebugInterface):
    url = "http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/%STATION_ID%"

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
        except http.client.RemoteDisconnected as e:
            logger.warning(str(e))
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
        if "pm10IndexLevel" in data and data["pm10IndexLevel"] is not None:
            values["PM10"] = {
                "index": data["pm10IndexLevel"]["id"],
                "date": data["pm10SourceDataDate"],
            }

        if "pm25IndexLevel" in data and data["pm25IndexLevel"] is not None:
            values["PM25"] = {
                "index": data["pm25IndexLevel"]["id"],
                "date": data["pm25SourceDataDate"],
            }

        if "coIndexLevel" in data and data["coIndexLevel"] is not None:
            values["CO"] = {
                "index": data["coIndexLevel"]["id"],
                "date": data["coSourceDataDate"],
            }

        if "so2IndexLevel" in data and data["so2IndexLevel"] is not None:
            values["SO2"] = {
                "index": data["so2IndexLevel"]["id"],
                "date": data["so2SourceDataDate"],
            }

        if "no2IndexLevel" in data and data["no2IndexLevel"] is not None:
            values["NO2"] = {
                "index": data["no2IndexLevel"]["id"],
                "date": data["no2SourceDataDate"],
            }

        if "o3IndexLevel" in data and data["o3IndexLevel"] is not None:
            values["O3"] = {
                "index": data["o3IndexLevel"]["id"],
                "date": data["o3SourceDataDate"],
            }

        if "c6h6IndexLevel" in data and data["c6h6IndexLevel"] is not None:
            values["BC"] = {
                "index": data["c6h6IndexLevel"]["id"],
                "date": data["c6h6SourceDataDate"],
            }

        return values

    def execute(self):
        data = self._fetch_data(self.url.replace("%STATION_ID%", str(self.station_id)))

        return self._normalize(data) if data is not None else {}
