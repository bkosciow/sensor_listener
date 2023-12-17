import json
from node_listener.worker import Worker
import datetime
import urllib
import urllib.error
import urllib.request
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.debug_interface import DebugInterface
import logging
logger = logging.getLogger(__name__)


class OpenweatherWorker(Worker, DebugInterface):
    forecast_days = 4

    """Openweather worker"""
    def __init__(self, params):
        if type(params['cities']) is not dict:
            raise ValueError("cities must be a dict")

        self.cities = params['cities']
        self.apikey = params['apikey']
        self.user_agent = params['user_agent']
        self.url_current = (
            "http://api.openweathermap.org/data/2.5/weather?"
            "id=%CITY_ID%&units=metric&mode=json&APPID=" + self.apikey
        )
        self.url_forecast = (
            "http://api.openweathermap.org/data/2.5/forecast/"
            "daily?id=%CITY_ID%&mode=json&units=metric&cnt="+str(self.forecast_days)+"&APPID=" + self.apikey
        )

    def debug_name(self):
        return 'OpenW'

    def _current_weather(self):
        """return curent weather"""
        for city_id in self.cities:
            """current weather"""
            url = self.url_current.replace("%CITY_ID%", str(city_id))
            json_data = self._fetch_data(url)
            if json_data:
                return self._decode_weather(json_data)

            return None

    def _forecast(self):
        """return forecast"""
        forecast_weather = {}
        for city_id in self.cities:
            """ forecast """
            url = self.url_forecast.replace("%CITY_ID%", str(city_id))
            json_data = self._fetch_data(url)
            forecast_weather[city_id] = {}

            if json_data:
                for row in json_data['list']:
                    date = (datetime.datetime.fromtimestamp(int(row['dt']))).strftime("%Y-%m-%d")
                    forecast_weather[city_id][date] = self._decode_forecast(row)

                return forecast_weather[city_id]

            return None

    def execute(self):
        """return data"""
        return {
            'current': self._current_weather(),
            'forecast': self._forecast(),
        }

    def _fetch_data(self, url):
        """fetch json data from server"""
        try:
            request = urllib.request.Request(
                url, None, {'User-Agent': self.user_agent}
            )
            response = urllib.request.urlopen(request)
            data = response.read()
            json_data = json.loads(data.decode())
            Dump.module_status({'name': 'OpenW', 'status': 2})
        except ValueError as e:
            logger.warning(str(e))
            json_data = None
            Dump.module_status({'name': 'OpenW', 'status': 4})
        except ConnectionResetError as e:
            logger.warning(str(e))
            json_data = None
            Dump.module_status({'name': 'OpenW', 'status': 4})
        except urllib.error.URLError as e:
            logger.warning(str(e))
            json_data = None
            Dump.module_status({'name': 'OpenW', 'status': 4})
        except Exception as e:
            logger.critical(str(e))
            Dump.module_status({'name': 'OpenW', 'status': 5})
            raise

        return json_data

    def _decode_weather(self, raw_data):
        """decode raw readings"""
        return {
            'temperature_current': raw_data['main']['temp'],
            'humidity': raw_data['main']['humidity'],
            'pressure': raw_data['main']['pressure'],
            'wind_speed': raw_data['wind']['speed'],
            'wind_deg': raw_data['wind']['deg'] if 'deg' in raw_data['wind'] else 0,
            'weather_id': raw_data['weather'][0]['id'],
            'weather': CODES[raw_data['weather'][0]['id']],
            'clouds': raw_data['clouds']['all'],
            'update': raw_data['dt']
        }

    def _decode_forecast(self, row):
        """decode raw readings"""
        return {
            'temperature_min': row['temp']['min'],
            'temperature_max': row['temp']['max'],
            'humidity': row['humidity'],
            'pressure': row['pressure'],
            'wind_speed': row['speed'],
            'wind_deg': row['deg'],
            'weather_id': row['weather'][0]['id'],
            'weather': CODES[row['weather'][0]['id']],
            'clouds': row['clouds']
        }


CODES = {
    200: 'thunderstorm with light rain',
    201: 'thunderstorm with rain',
    202: 'thunderstorm with heavy rain',
    210: 'light thunderstorm',
    211: 'thunderstorm',
    212: 'heavy thunderstorm',
    221: 'ragged thunderstorm',
    230: 'thunderstorm with light drizzle',
    231: 'thunderstorm with drizzle',
    232: 'thunderstorm with heavy drizzle',

    300: 'light intensity drizzle',
    301: 'drizzle',
    302: 'heavy intensity drizzle',
    310: 'light intensity drizzle rain',
    311: 'drizzle rain',
    312: 'heavy intensity drizzle rain',
    313: 'shower rain and drizzle',
    314: 'heavy shower rain and drizzle',
    321: 'shower drizzle',

    500: 'light rain',
    501: 'moderate rain',
    502: 'heavy intensity rain',
    503: 'very heavy rain',
    504: 'extreme rain',
    511: 'freezing rain',
    520: 'light intensity shower rain',
    521: 'shower rain',
    522: 'heavy intensity shower rain',
    531: 'ragged shower rain',

    600: 'light snow',
    601: 'snow',
    602: 'heavy snow',
    611: 'sleet',
    612: 'shower sleet',
    615: 'light rain and snow ',
    616: 'rain and snow ',
    620: 'light shower snow',
    621: 'shower snow',
    622: 'heavy shower snow',

    701: 'mist',
    711: 'smoke',
    721: 'haze',
    731: 'Sand/Dust Whirls',
    741: 'Fog',
    751: 'sand',
    761: 'dust',
    762: 'VOLCANIC ASH',
    771: 'SQUALLS',
    781: 'TORNADO',

    800: 'sky is clear',
    801: 'few clouds',
    802: 'scattered clouds',
    803: 'broken clouds',
    804: 'overcast clouds',
}
