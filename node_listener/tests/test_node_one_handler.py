#!/usr/bin/python3
#pylint: skip-file

__author__ = 'Bartosz Kościów'
from nose.tools import assert_equal, assert_true, assert_false
from nose.tools import assert_raises
from iot_message.message import Message
from nose.tools import assert_not_in, assert_in
from node_listener.handler.node_one_handler import NodeOneHandler
from unittest.mock import MagicMock


class TestDictionaryEngine(object):
    def setUp(self):
        self.worker = MagicMock()
        self.handler = NodeOneHandler(self.worker)

    def test_init_handler(self):
        assert_in(self.worker, self.handler.workers)

    def test_event_dht_status_handle(self):
        m = Message()
        m.set({'node': 'rambo', 'event': 'dht.status', 'response': {'temp': '10', 'humi': '60'}})
        self.handler.handle(m)
        self.worker.set_params.assert_called_with(
            'rambo', {'temp': '10', 'humi': '60'}
        )

    def test_event_detect_light_handle(self):
        m = Message()
        m.set({'node': 'rambo', 'event': 'detect.light'})
        self.handler.handle(m)
        self.worker.set_params.assert_called_with(
            'rambo', {'light': True}
        )

    def test_event_detect_dark_handle(self):
        m = Message()
        m.set({'node': 'rambo', 'event': 'detect.dark'})
        self.handler.handle(m)
        self.worker.set_params.assert_called_with(
            'rambo', {'light': False}
        )

    def test_event_pir_movement_handle(self):
        m = Message()
        m.set({'node': 'rambo', 'event': 'pir.movement'})
        self.handler.handle(m)
        self.worker.set_params.assert_called_with(
            'rambo', {'pir': True}
        )

    def test_event_pir_nomovement_handle(self):
        m = Message()
        m.set({'node': 'rambo', 'event': 'pir.nomovement'})
        self.handler.handle(m)
        self.worker.set_params.assert_called_with(
            'rambo', {'pir': False}
        )

    def test_event_channels_response_handle(self):
        m = Message()
        m.set({'node': 'rambo', 'event': 'channels.response', 'response': [1, 0, 1]})
        self.handler.handle(m)
        self.worker.set_params.assert_called_with(
            'rambo', {'relay': [1, 0, 1]}
        )
