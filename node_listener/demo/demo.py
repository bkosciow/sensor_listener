import time
import pprint
from iot_message.message import Message
from iot_message.cryptor.base64 import Cryptor as B64
from iot_message.cryptor.plain import Cryptor as Plain
from iot_message.cryptor.aes_sha1 import Cryptor as AES

from node_listener.storage.storage import Storage
from node_listener.storage.dictionary_engine import DictionaryEngine

from node_listener.server import SensorListener
from configparser import ConfigParser

config = ConfigParser()
config.read("../../config.ini")

Message.node_name = "db"
Message.add_encoder(B64())
Message.add_encoder(Plain())
encoder_aes = AES(
    config.get('aes', 'staticiv'),
    config.get('aes', 'ivkey'),
    config.get('aes', 'datakey'),
    config.get('aes', 'passphrase')
)
Message.add_encoder(encoder_aes)
Message.add_decoder(B64())
Message.add_decoder(encoder_aes)

Storage.set_engine(DictionaryEngine())

storage = Storage()
storage.set("test.script", '1')
serverSensor = SensorListener(storage)
serverSensor.start()
print(storage.get("test"))

while True:
    print("****************")
    pprint.pprint(storage.get_all())
    time.sleep(2)

