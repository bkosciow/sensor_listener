#!/usr/bin/python3
#pylint: skip-file

__author__ = 'Bartosz Kościów'
from unittest.mock import MagicMock
from nose.tools import assert_is_instance, assert_equal
from node_listener.storage.storage import Storage
from node_listener.service.sensor_listener import SensorListener
from node_listener.handler.node_one_handler import NodeOneHandler
from unittest import mock


class TestDictionaryEngine(object):
    def setUp(self):
        Storage.set_engine(MagicMock())
        self.storage = Storage()
        self.config = MagicMock()
        self.config.get_dict.return_value = {'1': 'BB'}

    @mock.patch.object(SensorListener, '_add_handlers')
    @mock.patch.object(SensorListener, '_add_workers')
    def test_start_should_start_server(self, mock1, mock2):
        server = SensorListener(self.storage, self.config)
        server.svr = MagicMock()
        server.executor = MagicMock()
        server.start()
        server.svr.start.should_be_called()
        server.executor.start.should_be_called()
        mock1.assert_called()
        mock2.assert_called()

    @mock.patch.object(SensorListener, '_add_handlers')
    @mock.patch.object(SensorListener, '_add_workers')
    def test_freq_parser(self, mock1, mock2):
        server = SensorListener(self.storage, self.config)
        r = server._parse_freq('3s')
        assert_equal(r, {'unit': 'seconds', 'value': 3})

    @mock.patch.object(SensorListener, '_add_handlers')
    @mock.patch.object(SensorListener, '_add_workers')
    @mock.patch.object(SensorListener, '_get_task')
    def test_start_task(self, mock1, mock2, mock3):
        mock1.return_value = "Task"
        server = SensorListener(self.storage, self.config)
        server.executor = MagicMock()
        server._start_task(MagicMock(), 'test', {'unit': 'seconds', 'value': 3})
        server.executor.every_seconds.assert_called_with(3, "Task")

    @mock.patch.object(SensorListener, '_add_handlers')
    @mock.patch.object(SensorListener, '_add_workers')
    @mock.patch.object(SensorListener, '_get_task')
    def test_start_task(self, mock1, mock2, mock3):
        mock1.return_value = "Task"
        server = SensorListener(self.storage, self.config)
        server.executor = MagicMock()
        server._start_task(MagicMock(), 'test', {'unit': 'minutes', 'value': 30})
        server.executor.every_minutes.assert_called_with(30, "Task")

    @mock.patch.object(SensorListener, '_add_handlers')
    @mock.patch.object(SensorListener, '_add_workers')
    @mock.patch.object(SensorListener, '_get_task')
    def test_start_task(self, mock1, mock2, mock3):
        mock1.return_value = "Task"
        server = SensorListener(self.storage, self.config)
        server.executor = MagicMock()
        server._start_task(MagicMock(), 'test', {'unit': 'hours', 'value': 1})
        server.executor.every_hours.assert_called_with(1, "Task")
