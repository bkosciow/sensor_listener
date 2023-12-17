#!/usr/bin/python3
#pylint: skip-file

__author__ = 'Bartosz Kościów'
from unittest.mock import MagicMock
from nose.tools import assert_equal, assert_true, assert_false, assert_is_not_none
from nose.tools import assert_raises
from nose.tools import assert_not_in
from node_listener.service.queue_bus import QueueBus


class TestQueueBus(object):
    def setUp(self):
        self.queue = MagicMock()
        self.bus = QueueBus(self.queue)

    def test_add_to_queue(self):
        e = MagicMock()
        e.key = "test"
        e.value = {'data': "tset"}

        self.queue.full.return_value = False
        self.bus.add_to_queue(e)
        self.queue.put.assert_called()
        self.queue.get.assert_not_called()

    def test_add_to_full_queue(self):
        e = MagicMock()
        e.key = "test"
        e.value = {'data': "tset"}

        self.queue.full.return_value = True
        self.bus.add_to_queue(e)
        self.queue.get.assert_called()
        self.queue.put.assert_called()