__author__ = 'Bartosz Kościów'
from nose.tools import assert_equal, assert_true, assert_false
from nose.tools import assert_raises
from nose.tools import assert_not_in
from node_listener.worker.gios_worker import GiosWorker
from unittest.mock import MagicMock
from unittest import mock


class TestGiosWorker(object):
    def setUp(self):
        self.station_id = 'ABC'
        self.user_agent = "tests"

    def test_init(self):
        w = GiosWorker({'station_id': self.station_id, 'user_agent': self.user_agent})
        assert_equal(self.station_id, w.station_id)
        assert_equal(self.user_agent, w.user_agent)

    def test_normalize(self):
        w = GiosWorker({'station_id': self.station_id, 'user_agent': self.user_agent})
        data ={'c6h6CalcDate': None,
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
             'stSourceDataDate': '2020-02-07 13:00:00'
        }

        normalized_data = w._normalize(data)

        correct_data = {
            "PM10": None,
            "PM25": {"index": 1, "date": '2020-02-07 11:00:00'},
            "CO": {"index": 0, "date": '2020-02-07 13:00:00'},
            "O3": None,
            "SO2": None,
            "NO2": {"index": 1, "date": '2020-02-07 13:00:00'},
            "BC": None
        }
        assert_equal(normalized_data, correct_data)

    @mock.patch.object(GiosWorker, '_fetch_data')
    @mock.patch.object(GiosWorker, '_normalize')
    def test_execute_should_call_fetch_and_normalize(self, mock1, mock2):
        w = GiosWorker({'station_id': self.station_id, 'user_agent': self.user_agent})
        w.execute()
        mock1.assert_called()
        mock2.assert_called()

