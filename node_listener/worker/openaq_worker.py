import json
from node_listener.worker import Worker
import urllib
import urllib.error
import urllib.request
import urllib.parse
import node_listener.service.air_pollution as air


class OpenaqWorker(Worker):
    url = "https://api.openaq.org/v1/latest?"

    def __init__(self, city, location, user_agent):
        self.city = city
        self.location = location
        self.user_agent = user_agent
        self._validate()

    def _validate(self):
        if self.city is None and self.location is None:
            raise AttributeError("city or location must be set")

    def _fetch_data(self, url):
        try:
            request = urllib.request.Request(
                url, None, {'User-Agent': self.user_agent}
            )
            response = urllib.request.urlopen(request)
            data = response.read()
            json_data = json.loads(data.decode())
        except ValueError as e:
            json_data = None

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
        return self._normalize(data)
