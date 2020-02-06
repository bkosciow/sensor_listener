#!/usr/bin/python3
#pylint: skip-file

__author__ = 'Bartosz Kościów'
from unittest.mock import MagicMock
from nose.tools import assert_equal, assert_true, assert_false, assert_is_not_none
from node_listener.scheduler.task import Task


class TestStorage(object):
    def setUp(self):
        pass

    def test_storage_schould_be_set(self):
        storage = MagicMock()
        Task.set_storage(storage)
        assert_equal(Task.storage, storage)

    def test_task_schould_be_created(self):
        callback = 'ooo'
        storage_key = 'store_key'
        task = Task(callback, storage_key)
        assert_equal(task.func, callback)
        assert_equal(task.storage_key, storage_key)

    def test_execute_schould_call_callback_and_save_result(self):
        callback = MagicMock()
        callback.return_value = "value"
        storage = MagicMock()
        storage_key = "meow"
        Task.set_storage(storage)
        task = Task(callback, storage_key)
        task.execute()
        callback.assert_called()
        storage.set.assert_called_with(storage_key, "value")
