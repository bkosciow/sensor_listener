#!/usr/bin/python3
#pylint: skip-file

__author__ = 'Bartosz Kościów'
from unittest.mock import MagicMock
from nose.tools import assert_equal, assert_true, assert_false, assert_is_not_none
from nose.tools import assert_raises
from nose.tools import assert_not_in
from node_listener.grpc.provider import Provider


class TestProvider(object):

    def test_get_whole_storage(self):
        storage = MagicMock()
        storage.get_all.return_value = {"test": "yes", "bum": "no"}
        queue = MagicMock()

        p = Provider(storage, queue)
        request = MagicMock()
        request.key = ''
        r = p.get_storage(request, MagicMock())

        storage.get_all.assert_called()
        assert_equal(r.data, '{"test": "yes", "bum": "no"}' )

    def test_get_one_key_from_storage(self):
        storage = MagicMock()
        storage.get.return_value = {"test": "yes"}
        queue = MagicMock()

        p = Provider(storage, queue)
        request = MagicMock()
        request.key = 'test'
        r = p.get_storage(request, MagicMock())

        storage.get.assert_called()
        assert_equal(r.data, '{"test": "yes"}' )