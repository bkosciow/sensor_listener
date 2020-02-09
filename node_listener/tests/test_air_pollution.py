__author__ = 'Bartosz Kościów'
from nose.tools import assert_equal, assert_true, assert_false
from nose.tools import assert_raises
from nose.tools import assert_not_in
from unittest.mock import MagicMock
from unittest import mock
import node_listener.service.air_pollution as air


class TestAirPollution(object):
    # def setUp(self):
    #     self.station_id = 'ABC'
    #     self.user_agent = "tests"
    def test_pm10_to_index_0(self):
        assert_equal(0, air.air_index_pm10(0))
        assert_equal(0, air.air_index_pm10(10))
        assert_equal(0, air.air_index_pm10(20))

    def test_pm10_to_index_1(self):
        assert_equal(1, air.air_index_pm10(20.1))
        assert_equal(1, air.air_index_pm10(30))
        assert_equal(1, air.air_index_pm10(50))

    def test_pm10_to_index_2(self):
        assert_equal(2, air.air_index_pm10(50.1))
        assert_equal(2, air.air_index_pm10(70))
        assert_equal(2, air.air_index_pm10(80))

    def test_pm10_to_index_3(self):
        assert_equal(3, air.air_index_pm10(80.1))
        assert_equal(3, air.air_index_pm10(90))
        assert_equal(3, air.air_index_pm10(110))

    def test_pm10_to_index_4(self):
        assert_equal(4, air.air_index_pm10(110.1))
        assert_equal(4, air.air_index_pm10(130))
        assert_equal(4, air.air_index_pm10(150))

    def test_pm10_to_index_5(self):
        assert_equal(5, air.air_index_pm10(150.1))
        assert_equal(5, air.air_index_pm10(300))
        assert_equal(5, air.air_index_pm10(5000))

    def test_pm25_to_index_0(self):
        assert_equal(0, air.air_index_pm25(0))
        assert_equal(0, air.air_index_pm25(10))
        assert_equal(0, air.air_index_pm25(13))

    def test_pm25_to_index_1(self):
        assert_equal(1, air.air_index_pm25(13.1))
        assert_equal(1, air.air_index_pm25(20))
        assert_equal(1, air.air_index_pm25(35))

    def test_pm25_to_index_2(self):
        assert_equal(2, air.air_index_pm25(35.1))
        assert_equal(2, air.air_index_pm25(45))
        assert_equal(2, air.air_index_pm25(55))

    def test_pm25_to_index_3(self):
        assert_equal(3, air.air_index_pm25(55.1))
        assert_equal(3, air.air_index_pm25(60))
        assert_equal(3, air.air_index_pm25(75))

    def test_pm25_to_index_4(self):
        assert_equal(4, air.air_index_pm25(75.1))
        assert_equal(4, air.air_index_pm25(100))
        assert_equal(4, air.air_index_pm25(110))

    def test_pm25_to_index_5(self):
        assert_equal(5, air.air_index_pm25(110.1))
        assert_equal(5, air.air_index_pm25(300))
        assert_equal(5, air.air_index_pm25(5000))
        
    def test_co_to_index_0(self):
        assert_equal(0, air.air_index_co(0))
        assert_equal(0, air.air_index_co(100))
        assert_equal(0, air.air_index_co(3000))

    def test_co_to_index_1(self):
        assert_equal(1, air.air_index_co(3000.1))
        assert_equal(1, air.air_index_co(4000))
        assert_equal(1, air.air_index_co(7000))

    def test_co_to_index_2(self):
        assert_equal(2, air.air_index_co(7000.1))
        assert_equal(2, air.air_index_co(10000))
        assert_equal(2, air.air_index_co(11000))

    def test_co_to_index_3(self):
        assert_equal(3, air.air_index_co(11000.1))
        assert_equal(3, air.air_index_co(14000))
        assert_equal(3, air.air_index_co(15000))

    def test_co_to_index_4(self):
        assert_equal(4, air.air_index_co(15000.1))
        assert_equal(4, air.air_index_co(16000))
        assert_equal(4, air.air_index_co(21000))

    def test_co_to_index_5(self):
        assert_equal(5, air.air_index_co(21000.1))
        assert_equal(5, air.air_index_co(300000))
        assert_equal(5, air.air_index_co(5000000))