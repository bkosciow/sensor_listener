import json
from node_listener.worker import Worker
import datetime
import urllib
import urllib.error
import urllib.request
from pprint import pprint


class GiosWorker(Worker):
    url = "http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/%STATION_ID%"

    def __init__(self, station_id):
        self.station_id = station_id

    def _fetch_data(self, url):
        """fetch json data from server"""
        return {'c6h6CalcDate': None,
 'c6h6IndexLevel': None,
 'c6h6SourceDataDate': None,
 'coCalcDate': '2020-02-07 13:20:22',
 'coIndexLevel': {'id': 0, 'indexLevelName': 'Bardzo dobry'},
 'coSourceDataDate': '2020-02-07 13:00:00',
 'id': 10158,
 'no2CalcDate': 1581078022000,
 'no2IndexLevel': {'id': 1, 'indexLevelName': 'Dobry'},
 'no2SourceDataDate': '2020-02-07 13:00:00',
 'o3CalcDate': None,
 'o3IndexLevel': None,
 'o3SourceDataDate': None,
 'pm10CalcDate': None,
 'pm10IndexLevel': None,
 'pm10SourceDataDate': None,
 'pm25CalcDate': '2020-02-07 13:20:22',
 'pm25IndexLevel': {'id': 1, 'indexLevelName': 'Dobry'},
 'pm25SourceDataDate': '2020-02-07 11:00:00',
 'so2CalcDate': None,
 'so2IndexLevel': None,
 'so2SourceDataDate': None,
 'stCalcDate': '2020-02-07 13:20:22',
 'stIndexCrParam': 'PYL',
 'stIndexLevel': {'id': 1, 'indexLevelName': 'Dobry'},
 'stIndexStatus': True,
 'stSourceDataDate': '2020-02-07 13:00:00'}

        try:
            request = urllib.request.Request(
                url, None, {'User-Agent': 'SensorListener'}
            )
            response = urllib.request.urlopen(request)
            data = response.read()
            json_data = json.loads(data.decode())
        except ValueError as e:
            json_data = None

        return json_data

    def _normalize(self, data):
        values = {
            "PM10": None,
            "PM25": None,
            "CO": None,
        }
        if data["pm10IndexLevel"] is not None:
            values["PM10"] = {
                "index": data["pm10IndexLevel"]["id"],
                "date": data["pm10SourceDataDate"],
            }

        if data["pm25IndexLevel"] is not None:
            values["PM25"] = {
                "index": data["pm25IndexLevel"]["id"],
                "date": data["pm25SourceDataDate"],
            }

        if data["coIndexLevel"] is not None:
            values["CO"] = {
                "index": data["coIndexLevel"]["id"],
                "date": data["coSourceDataDate"],
            }

        return values

    def execute(self):
        data = self._fetch_data(self.url.replace("%STATION_ID%", self.station_id))
        return self._normalize(data)
