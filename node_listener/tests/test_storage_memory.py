#!/usr/bin/python3
#pylint: skip-file

__author__ = 'Bartosz Kościów'
from nose.tools import assert_equal, assert_true, assert_false
from nose.tools import assert_raises
from nose.tools import assert_not_in
from node_listener.storage.dictionary_engine import DictionaryEngine


class TestDictionaryEngine(object):
    def setUp(self):
        self.storage_engine = DictionaryEngine()

    def test_set_key(self):
        self.storage_engine.set('animal', {'name': 'cat'})
        assert_equal(self.storage_engine.data['animal'], {'name': 'cat'})

    def test_get_key(self):
        self.storage_engine.set('animal', {'name': 'cat'})
        assert_equal(self.storage_engine.get('animal'), {'name': 'cat'})

    def test_key_exists(self):
        self.storage_engine.set('animal', {'name': 'cat'})
        assert_equal(self.storage_engine.exists('animal'), True)

    def test_key_not_exists(self):
        assert_equal(self.storage_engine.exists('animal'), False)

    def test_set_2d_key(self):
        self.storage_engine.set("table", {'color': 'red'})
        assert_not_in("table,color", self.storage_engine.data)
        assert_equal(self.storage_engine.data['table'], {'color': 'red'})
        assert_equal(self.storage_engine.data['table']['color'], 'red')

    def test_get_2d_key(self):
        self.storage_engine.set("table", {'color': 'red'})
        assert_not_in("table,color", self.storage_engine.data)
        assert_equal(self.storage_engine.get('table'), {'color': 'red'})
        assert_equal(self.storage_engine.get('table.color'), 'red')

    def test_complex_key_exists(self):
        self.storage_engine.set("table", {'color': 'red'})
        assert_true(self.storage_engine.exists("table"))

    def test_key_2d_exists(self):
        self.storage_engine.set("table", {'color': 'red'})
        assert_true(self.storage_engine.exists("table.color"))

    def test_complex_key_not_exists(self):
        self.storage_engine.set("table", {'color': 'red'})
        assert_false(self.storage_engine.exists("elbat"))

    def test_key_2d_not_exists(self):
        self.storage_engine.set("table", {'color': 'red'})
        assert_false(self.storage_engine.exists("table.colors"))

    def test_key_2d_not_exists_first_key(self):
        self.storage_engine.set("table", {'color': 'red'})
        assert_false(self.storage_engine.exists("tables.color"))
