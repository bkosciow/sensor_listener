import json
from node_listener.worker import Worker
import urllib
import urllib.error
import urllib.request
from node_listener.service.hd44780_40_4 import Dump


class GiosWorker(Worker):
    url = "http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/%STATION_ID%"

    def __init__(self, station_id, user_agent):
        self.station_id = station_id
        self.user_agent = user_agent

    def _fetch_data(self, url):
        """fetch json data from server"""
 #        return {'c6h6CalcDate': None,
 # 'c6h6IndexLevel': None,
 # 'c6h6SourceDataDate': None,
 # 'coCalcDate': '2020-02-07 13:20:22',
 # 'coIndexLevel': {'id': 0, 'indexLevelName': 'Bardzo dobry'},
 # 'coSourceDataDate': '2020-02-07 13:00:00',
 # 'id': 10158,
 # 'no2CalcDate': 1581078022000,
 # 'no2IndexLevel': {'id': 1, 'indexLevelName': 'Dobry'},
 # 'no2SourceDataDate': '2020-02-07 13:00:00',
 # 'o3CalcDate': None,
 # 'o3IndexLevel': None,
 # 'o3SourceDataDate': None,
 # 'pm10CalcDate': None,
 # 'pm10IndexLevel': None,
 # 'pm10SourceDataDate': None,
 # 'pm25CalcDate': '2020-02-07 13:20:22',
 # 'pm25IndexLevel': {'id': 1, 'indexLevelName': 'Dobry'},
 # 'pm25SourceDataDate': '2020-02-07 11:00:00',
 # 'so2CalcDate': None,
 # 'so2IndexLevel': None,
 # 'so2SourceDataDate': None,
 # 'stCalcDate': '2020-02-07 13:20:22',
 # 'stIndexCrParam': 'PYL',
 # 'stIndexLevel': {'id': 1, 'indexLevelName': 'Dobry'},
 # 'stIndexStatus': True,
 # 'stSourceDataDate': '2020-02-07 13:00:00'}

        try:
            request = urllib.request.Request(
                url, None, {'User-Agent': self.user_agent}
            )
            response = urllib.request.urlopen(request)
            data = response.read()
            json_data = json.loads(data.decode())
            Dump.module_status({'name': 'gios', 'status': 2})
        except ValueError as e:
            json_data = None
            Dump.module_status({'name': 'gios', 'status': 4})
        except urllib.error.HTTPError as e:
            print(e)
            json_data = None
            Dump.module_status({'name': 'gios', 'status': 4})
        except urllib.error.URLError as e:
            print(e)
            json_data = None
            Dump.module_status({'name': 'gios', 'status': 4})
        except:
            Dump.module_status({'name': 'gios', 'status': 5})
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
        data = self._fetch_data(self.url.replace("%STATION_ID%", self.station_id))

        return self._normalize(data) if data is not None else None
