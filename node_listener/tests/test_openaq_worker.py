__author__ = 'Bartosz Kościów'
from nose.tools import assert_equal, assert_true, assert_false
from nose.tools import assert_raises
from nose.tools import assert_not_in
from node_listener.worker.openaq_worker import OpenaqWorker
from unittest.mock import MagicMock
from unittest import mock


class TestOpenaqWorker(object):
    def setUp(self):
        self.city = 'ABC'
        self.location = "DEF"
        self.user_agent = "tests"
        # self.worker = OpenaqWorker(self.city, self.location, self.user_agent)

    def test_init_with_city(self):
        w = OpenaqWorker(self.city, None, self.user_agent)
        assert_equal(self.user_agent, w.user_agent)
        assert_equal(self.city, w.city)
        assert_equal(None, w.location)

    def test_init_with_location(self):
        w = OpenaqWorker(None, self.location, self.user_agent)
        assert_equal(self.user_agent, w.user_agent)
        assert_equal(w.city, None)
        assert_equal(self.location, w.location)

    def test_init_with_location_and_city(self):
        w = OpenaqWorker(self.city, self.location, self.user_agent)
        assert_equal(self.user_agent, w.user_agent)
        assert_equal(self.city, w.city)
        assert_equal(self.location, w.location)

    def test_not_init_without_city_and_location(self):
        assert_raises(AttributeError, OpenaqWorker, None, None, self.user_agent)

    def test_get_url_with_city(self):
        w = OpenaqWorker(self.city, None, self.user_agent)
        assert_equal(w._get_url(), "https://api.openaq.org/v1/latest?city="+self.city)

    def test_get_url_with_location(self):
        w = OpenaqWorker(None, self.location, self.user_agent)
        assert_equal(w._get_url(), "https://api.openaq.org/v1/latest?location="+self.location)

    def test_get_url_with_city_and_location(self):
        w = OpenaqWorker(self.city, self.location, self.user_agent)
        assert_equal(w._get_url(), "https://api.openaq.org/v1/latest?city="+self.city+"&location="+self.location)

    def test_normalize_data(self):
        w = OpenaqWorker(self.city, self.location, self.user_agent)
        data = {"meta":{"name":"openaq-api","license":"CC BY 4.0","website":"https://docs.openaq.org/","page":1,"limit":100,"found":2},"results":[{"location":"Bielsko-Biała, ul. Kossak-Szczuckiej 19","city":"Bielsko-Biała","country":"PL","distance":1484187.8159062166,"measurements":[{"parameter":"o3","value":66.155,"lastUpdated":"2020-02-08T15:00:00.000Z","unit":"µg/m³","sourceName":"GIOS"},{"parameter":"pm10","value":24.1643,"lastUpdated":"2020-02-08T14:00:00.000Z","unit":"µg/m³","sourceName":"GIOS"},{"parameter":"so2","value":8.38712,"lastUpdated":"2020-02-08T15:00:00.000Z","unit":"µg/m³","sourceName":"GIOS"},{"parameter":"bc","value":1.29114,"lastUpdated":"2020-02-08T15:00:00.000Z","unit":"µg/m³","sourceName":"GIOS"}],"coordinates":{"latitude":49.813465,"longitude":19.027317}},{"location":"Bielsko-Biała, ul.Partyzantów","city":"Bielsko-Biała","country":"PL","distance":1486127.442044661,"measurements":[{"parameter":"co","value":507.42,"lastUpdated":"2020-02-08T15:00:00.000Z","unit":"µg/m³","sourceName":"GIOS"},{"parameter":"no2","value":40.507,"lastUpdated":"2020-02-08T15:00:00.000Z","unit":"µg/m³","sourceName":"GIOS"},{"parameter":"pm25","value":30.9064,"lastUpdated":"2020-02-08T14:00:00.000Z","unit":"µg/m³","sourceName":"GIOS"}],"coordinates":{"latitude":49.802074,"longitude":19.04861}}]}

        normalized_data = w._normalize(data)

        correct_data = {
            "Bielsko-Biała, ul. Kossak-Szczuckiej 19": {
                "PM10": {"index": 1, "date": '2020-02-08T14:00:00.000Z'},
                "PM25": None,
                "CO": None,
            },
            "Bielsko-Biała, ul.Partyzantów": {
                "PM10": None,
                "PM25": {"index": 1, "date": '2020-02-08T14:00:00.000Z'},
                "CO": {"index": 0, "date": '2020-02-08T15:00:00.000Z'},
            }
        }
