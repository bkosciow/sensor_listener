#!/usr/bin/python3
#pylint: skip-file

__author__ = 'Bartosz Kościów'
from unittest.mock import MagicMock
from nose.tools import assert_is_instance
from node_listener.storage.storage import Storage
from node_listener.service.sensor_listener import SensorListener
from node_listener.handler.node_one_handler import NodeOneHandler


class TestDictionaryEngine(object):
    def setUp(self):
        Storage.set_engine(MagicMock())
        self.storage = Storage()
        self.config = MagicMock()
        self.config.get_dict.return_value = {'1': 'BB'}
        self.server = SensorListener(self.storage, self.config)

    def test_node_one_should_be_added(self):
        assert_is_instance(self.server.svr.handlers['NodeOne'][0], NodeOneHandler)

    def test_start_should_start_server(self):

        self.server.svr = MagicMock()
        self.server.executor = MagicMock()
        self.server.start()
        self.server.svr.start.should_be_called()
        self.server.executor.start.should_be_called()