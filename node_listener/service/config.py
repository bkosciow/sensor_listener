from configparser import ConfigParser
from iot_message.message import Message
from iot_message.cryptor.base64 import Cryptor as B64
from iot_message.cryptor.plain import Cryptor as Plain
from iot_message.cryptor.aes_sha1 import Cryptor as AES
from node_listener.service.hd44780_40_4 import Dump
import json
import importlib


class Config(object):
    """Class Config"""
    def __init__(self, file="../config.ini"):
        self.file = file
        self.config = ConfigParser()
        self.config.read(file, encoding='utf-8')
        self._init_message()
        self._init_hd44780()

    def _init_message(self):
        Message.node_name = self.config.get('general', 'node_name')
        Message.chip_id = self.config.get('general', 'node_id')
        # Message.add_encoder(B64())
        # Message.add_encoder(Plain())
        encoder_aes = AES(
            self.config.get('aes', 'staticiv'),
            self.config.get('aes', 'ivkey'),
            self.config.get('aes', 'datakey'),
            self.config.get('aes', 'passphrase')
        )
        Message.add_encoder(encoder_aes)
        Message.add_decoder(B64())
        Message.add_decoder(encoder_aes)

    def sections(self):
        return self.config.sections()

    def get(self, name):
        if "." in name:
            section, name = name.split(".")
        else:
            section = "global"

        val = self.config.get(section, name)
        return val if val != "" else None

    def __getitem__(self, item):
        return self.config[item]

    def get_dict(self, name):
        value = self.get(name)
        return self._get_dict(value)

    def get_list(self, name):
        return json.loads(self.get(name))

    def _get_dict(self, value):
        """str to dict, replace '' with None"""
        if not value:
            return None
        values = json.loads(value)
        for key in values:
            if values[key] == "":
                values[key] = None

        return values

    def section_enabled(self, section):
        value = 0
        if self.config.has_option(section, "enabled"):
            value = self.get(section+".enabled")

        return True if value == "1" else False

    def get_handler(self, section):
        data = None
        if self.config.has_option(section, "handler"):
            paths = self.get(section + ".handler").rsplit(".", 1)
            params = self.get(section + ".handler_parameters")
            if params is not None:
                params = json.loads(params)
            else:
                params = []
            data = {
                'module': paths[0],
                'class': paths[1],
                'params': params,
                'name': self.get(section + ".handler_name"),
            }

        return data

    def get_worker(self, section):
        data = None
        if self.config.has_option(section, "worker"):
            paths = self.get(section + ".worker").rsplit(".", 1)
            params = self.get(section + ".worker_parameters")
            if params is not None:
                params = json.loads(params)
            else:
                params = []
            data = {
                'module': paths[0],
                'class': paths[1],
                'params': params,
                'name': self.get(section + ".worker_name"),
                'freq': self.get(section + ".worker_freq")
            }

        return data

    def get_storage_engine(self):
        engine_name = self.get('storage.engine')
        module_path, class_name = engine_name.rsplit('.', 1)
        module = importlib.import_module(module_path)
        class_obj = getattr(module, class_name)
        args = self.get('storage.engine_parameters')
        return class_obj(json.loads(args))

    def _init_hd44780(self):
        Dump(self.section_enabled('hd44780'))

