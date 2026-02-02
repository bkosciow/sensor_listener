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
        self.user_agent = params['user_agent']
        self.places = {}
        self.sensors = {}
        self.initialize_locations(params['places'])

    def initialize_locations(self, places):
        for place in places:
            self.sensors[place["name"]] = {}
            url = self.url + "locations?coordinates=" + place["coordinates"] + "&radius=" + place["radius"]
            items = self._fetch_data(url)
            if items is not None:
                for item in items['results']:
                    self.sensors[place["name"]][item['id']] = {}
                    for sensor in item['sensors']:
                        self.sensors[place["name"]][item['id']][sensor['id']] = sensor['parameter']['name']

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
            # print(dir(response))
            # print(response.request.url)
            if response.status_code != 200:
                logger.error(response.status_code)
                logger.error(response.content)

            json_data = json.loads(response.content) # data.decode())
            if json_data is None:
                print(response.is_redirect, response.headers)
                print("pusto", response.content)
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
    def _get_readings(self):
        response = {}
        for place in self.sensors:
            # print("Place: ", place)
            values = {
                "PM10": None,
                "PM25": None,
                "CO": None,
                "O3": None,
                "SO2": None,
                "NO2": None,
                "BC": None
            }
            for sensor_id in self.sensors[place]:
                url = self.url + "locations/" + str(sensor_id) + "/latest"
                # print("URL: ",url)
                items = self._fetch_data(url)
                # print(items)
                if items is None or 'results' not in items:
                    continue

                for item in items['results']:
                    name = self.sensors[place][sensor_id][item['sensorsId']]
                    if name == "co":
                        idx = air.air_index_co(item["value"])
                        if values["CO"] is None or values["CO"]["index"] < idx:
                            values['CO'] = {
                                'index': idx,
                                'date': item['datetime']['utc']
                            }
                    if name == "no2":
                        pass
                    if name == "pm25":
                        idx = air.air_index_pm25(item["value"])
                        if values["PM25"] is None or values["PM25"]["index"] < idx:
                            values['PM25'] = {
                                'index': idx,
                                'date': item['datetime']['utc']
                            }
                    if name == "no2":
                        idx = air.air_index_no2(item["value"])
                        if values["NO2"] is None or values["NO2"]["index"] < idx:
                            values['NO2'] = {
                                'index': idx,
                                'date': item['datetime']['utc']
                            }
                    if name == "o3":
                        idx = air.air_index_o3(item["value"])
                        if values["O3"] is None or values["O3"]["index"] < idx:
                            values['O3'] = {
                                'index': idx,
                                'date': item['datetime']['utc']
                            }
                    if name == "pm10":
                        idx = air.air_index_pm10(item["value"])
                        if values["PM10"] is None or values["PM10"]["index"] < idx:
                            values['PM10'] = {
                                'index': idx,
                                'date': item['datetime']['utc']
                            }
                    if name == "so2":
                        idx = air.air_index_so2(item["value"])
                        if values["SO2"] is None or values["SO2"]["index"] < idx:
                            values['SO2'] = {
                                'index': idx,
                                'date': item['datetime']['utc']
                            }
                response[place] = values

        return response

    def execute(self):
        data = self._get_readings()
        logger.info(data)
        if data:
            return data

        logger.error('OpenAQ no data')
        return {}

