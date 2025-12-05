import json
from node_listener.worker import Worker
import requests
import node_listener.service.air_pollution as air
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.debug_interface import DebugInterface
import logging
logger = logging.getLogger(__name__)
from pprint import pprint


class OpenaqWorker(Worker, DebugInterface):
    url = "https://api.openaq.org/v3/"

    def __init__(self, params):
        self.apikey = params['apikey'] if params['apikey'] != "" else None
        self.coordinates = params['coordinates']
        self.radius = params['radius']
        self.user_agent = params['user_agent']
        self.sensors = {}
        self.initialize_locations()

    def initialize_locations(self):
        url = self.url + "locations?coordinates=" + self.coordinates + "&radius=" + self.radius
        items = self._fetch_data(url)
        if items is not None:
            for item in items['results']:
                self.sensors[item['id']] = {}
                for sensor in item['sensors']:
                    self.sensors[item['id']][sensor['id']] = sensor['parameter']['name']

        if self.sensors is None:
            logger.critical("AQ no localization detected")

    def debug_name(self):
        return 'opnAQ'

    def _fetch_data(self, url):
        try:
            response = requests.get(
                url,
                headers={
                    'User-Agent': self.user_agent,
                    'X-API-Key': self.apikey,
                }
            )
            if response.status_code > 299:
                logger.error(response.status_code)
                logger.error(response.content)

            json_data = json.loads(response.content) # data.decode())
            Dump.module_status({'name': self.debug_name(), 'status': 2})
        except ValueError as e:
            logger.error(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except requests.exceptions.ConnectionError as e:
            logger.error(str(e))
            json_data = None
            Dump.module_status({'name': self.debug_name(), 'status': 4})
        except Exception as e:
            logger.critical(str(e))
            Dump.module_status({'name': self.debug_name(), 'status': 5})
            raise

        return json_data
    # https://api.openaq.org/v3/locations/9635/latest
    # https://api.openaq.org/v3/locations/9635/latest
    def _get_readings(self):
        values = {}
        for sensor_id in self.sensors:
            url = self.url + "locations/" + str(sensor_id) + "/latest"
            # print(url)
            items = self._fetch_data(url)
            # print(items)
            if items is None or 'results' not in items:
                continue
            values[sensor_id] = {
                "PM10": None,
                "PM25": None,
                "CO": None,
                "O3": None,
                "SO2": None,
                "NO2": None,
                "BC": None
            }
            for item in items['results']:
                name = self.sensors[sensor_id][item['sensorsId']]
                if name == "co":
                    values[sensor_id]["CO"] = {
                        'index': air.air_index_co(item["value"]),
                        'date': item['datetime']['utc']
                    }
                if name == "no2":
                    pass
                if name == "pm25":
                    values[sensor_id]["PM25"] = {
                        'index': air.air_index_pm25(item["value"]),
                        'date': item['datetime']['utc']
                    }
                if name == "bc":
                    values[sensor_id]["BC"] = {
                        'index': air.air_index_so2(item["value"]),
                        'date': item['datetime']['utc']
                    }
                if name == "no2":
                    values[sensor_id]["NO2"] = {
                        'index': air.air_index_no2(item["value"]),
                        'date': item['datetime']['utc']
                    }
                if name == "o3":
                    values[sensor_id]["O3"] = {
                        'index': air.air_index_o3(item["value"]),
                        'date': item['datetime']['utc']
                    }
                if name == "pm10":
                    values[sensor_id]["PM10"] = {
                        'index': air.air_index_pm10(item["value"]),
                        'date': item['datetime']['utc']
                    }
                if name == "so2":
                    values[sensor_id]["SO2"] = {
                        'index': air.air_index_so2(item["value"]),
                        'date':item['datetime']['utc']
                    }

        return values

    def execute(self):
        data = self._get_readings()
        #print("DATA", data)
        logger.info(data)
        if data:
            return data

        logger.error('OpenAQ no data')
        return {}

