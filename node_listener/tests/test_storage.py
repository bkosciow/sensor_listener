#!/usr/bin/python3
#pylint: skip-file

__author__ = 'Bartosz Kościów'
from unittest.mock import MagicMock
from nose.tools import assert_equal, assert_true, assert_false, assert_is_not_none
from nose.tools import assert_raises
from nose.tools import assert_not_in
from node_listener.storage.storage import Storage
from node_listener.storage.dictionary_engine import DictionaryEngine


class TestStorage(object):
    def setUp(self):
        Storage.set_engine(MagicMock())
        self.storage = Storage()

    def test_storage_has_an_engine(self):
        assert_is_not_none(Storage.engine)

    def test_get_on_engine(self):
        self.storage.get("r.a.m.b.o")
        Storage.engine.exists.assert_called_with('r.a.m.b.o')
        Storage.engine.get.assert_called_with('r.a.m.b.o')

    def test_set_on_engine(self):
        self.storage.set("r.a.m.b.o", True)
        Storage.engine.set.assert_called_with('r.a.m.b.o', True)

    def test_exists_on_engine(self):
        self.storage.exists("r.a.m.b.o")
        Storage.engine.exists.assert_called_with('r.a.m.b.o')

    def test_set_new_params(self):
        data = {
            'part1': "first blood",
            'part2': 'II',
        }
        self.storage.engine.get.return_value = {}
        self.storage.set_params("r.a.m.b.o", data)

        self.storage.engine.get.assert_called_with('r.a.m.b.o')
        self.storage.engine.set.assert_called_with('r.a.m.b.o', data)

    # def test_update_params(self):
    #     data = {
    #         'part1': "first blood",
    #         'part2': 'II',
    #     }
    #     self.storage.engine.get.return_value = {
    #         "part3": 'III',
    #         'part1': "I",
    #     }
    #     self.storage.set_params("r.a.m.b.o", data)
    #
    #     self.storage.engine.get.assert_called_with('r.a.m.b.o')
    #     self.storage.engine.set.assert_called_with('r.a.m.b.o', {
    #         "part3": 'III',
    #         'part2': 'II',
    #         'part1': "first blood",
    #     })

    def test_storage_with_dictionry_engine(self):
        Storage.set_engine(DictionaryEngine())
        data = {
            'part1': "first blood",
            'part2': 'II',
        }
        self.storage.set_params("r.a.m.b.o", data)
        assert_equal(self.storage.get('r.a.m.b.o'), data)
        self.storage.set_params("r.a.m.b.o", {
            "part3": 'III',
            'part1': 'I',
        })

        assert_equal(self.storage.get('r.a.m.b.o'), {
            "part3": 'III',
            'part2': 'II',
            'part1': 'I',
        })

    def test_set_hook(self):
        h = MagicMock()
        self.storage.on("set", h)
        self.storage.set("vroom", "car")
        h.assert_called()

    def test_get_hook(self):
        h = MagicMock()
        self.storage.on("get", h)
        self.storage.get("vroom")
        h.assert_called()