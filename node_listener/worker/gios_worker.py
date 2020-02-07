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
