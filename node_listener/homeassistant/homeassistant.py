from paho.mqtt import client as mqtt_client
import json
import logging
logger = logging.getLogger(__name__)


class HomeAssistant:
    def __init__(self, cfg):
        self.cfg = cfg
        self.client = mqtt_client.Client(client_id="SensorListener", callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(cfg['mqtt_user'], cfg['mqtt_password'])
        self.client.connect(cfg['mqtt_server'], int(cfg['mqtt_port']))
        self.supported_nodes = {
            'node-kitchen': 'node-one',
            'node-toilet': 'node-one',
            'node-living': 'node-one',
            'node-lib': 'node-one',
            'node-printers': 'relay-box',
            'node-relaybox2': 'relay-box'
        }
        self.discovery()

    def discovery(self):
        for node in self.supported_nodes:
            if self.supported_nodes[node] == 'node-one':
                discovery_packet = self.get_node_discovery_packet(node)
                discovery_topic = f"homeassistant/device/{node}/config"
            elif self.supported_nodes[node] == 'relay-box':
                discovery_packet = self.get_relay_discovery_packet(node)
                discovery_topic = f"homeassistant/device/{node}/config"

            self.publish(discovery_topic, discovery_packet, True)
            logger.info(f'Initializing node: {node}, topic: {discovery_topic} ')

    def get_node_discovery_packet(self, _id):
        base_topic_state = f"home/{_id}"
        discovery_packet = {
            'dev': {  # device
                'ids': _id,
                'name': f'NodeOne: {_id}',
                'mf': 'me',
            },
            'o': {  # origin
                'name': 'NodeOne',
                'sw': '2.1'
            },
            'cmps': {  # components
                f'{_id}-temperature0': {
                    'p': 'sensor',  # platform
                    'device_class': 'temperature',
                    'unit_of_measurement': "°C",
                    'value_template': "{{ value_json.temp}}",
                    "unique_id": f"home-{_id}-temperature0",
                    "state_topic": base_topic_state + "/temperature0/state"
                },
                f'{_id}-humidity0': {
                    'p': 'sensor',  # platform
                    'device_class': 'humidity',
                    'unit_of_measurement': "%",
                    'value_template': "{{ value_json.humi}}",
                    "unique_id": f"home-{_id}-humidity0",
                    "state_topic": base_topic_state + "/temperature0/state"
                },
                f'{_id}-motion0': {
                    "p": "binary_sensor",
                    'device_class': 'motion',
                    'unique_id': f"home-{_id}-motion0",
                    'state_topic': base_topic_state + "/motion0/state",
                    'payload_on': True,
                    'payload_off': False,
                },
                f'{_id}-light0': {
                    'p': 'binary_sensor',
                    'device_class': 'light',
                    'unique_id': f"home-{_id}-light0",
                    'state_topic': base_topic_state + "/light0/state",
                    'payload_on': True,
                    'payload_off': False,
                },
                f'{_id}-power0': {
                    'p': 'switch',
                    'unique_id': f"home-{_id}-power0",
                    'state_topic': base_topic_state + "/power0/state",
                    'command_topic': base_topic_state + "/power0/command",
                    'payload_on': '1',
                    'payload_off': '0',
                    "value_template": "{{ value_json[0] }}"
                }
            },
            'qos': 2
        }

        return discovery_packet

    def get_relay_discovery_packet(self, _id):
        base_topic_state = f"home/{_id}"
        discovery_packet = {
            'dev': {  # device
                'ids': _id,
                'name': f'RelayBox: {_id}',
                'mf': 'me',
            },
            'o': {  # origin
                'name': 'RelayBox',
                'sw': '1.0'
            },
            'cmps': {
                f'{_id}-power0': {
                    'p': 'switch',
                    'unique_id': f"home-{_id}-power0",
                    'state_topic': base_topic_state + "/power0/state",
                    'command_topic': base_topic_state + "/power0/command",
                    'payload_on': '1',
                    'payload_off': '0',
                    "value_template": "{{ value_json[0] }}"
                },
                f'{_id}-power1': {
                    'p': 'switch',
                    'unique_id': f"home-{_id}-power1",
                    'state_topic': base_topic_state + "/power0/state",
                    'command_topic': base_topic_state + "/power1/command",
                    'payload_on': '1',
                    'payload_off': '0',
                    "value_template": "{{ value_json[1] }}"
                },
                f'{_id}-power2': {
                    'p': 'switch',
                    'unique_id': f"home-{_id}-power2",
                    'state_topic': base_topic_state + "/power0/state",
                    'command_topic': base_topic_state + "/power2/command",
                    'payload_on': '1',
                    'payload_off': '0',
                    "value_template": "{{ value_json[2] }}"
                },
                f'{_id}-power3': {
                    'p': 'switch',
                    'unique_id': f"home-{_id}-power3",
                    'state_topic': base_topic_state + "/power0/state",
                    'command_topic': base_topic_state + "/power3/command",
                    'payload_on': '1',
                    'payload_off': '0',
                    "value_template": "{{ value_json[3] }}"
                }
            },
            'qos': 2
        }

        return discovery_packet

    def publish(self, topic, packet, persist):
        if isinstance(packet, dict) or isinstance(packet, list):
            packet = json.dumps(packet)

        result = self.client.publish(topic, packet)
        status = result[0]
        if status != 0:
            logger.error(f"Failed to send message to topic {topic}")

    def set_params(self, key, params):
        if key in self.supported_nodes:
            # print(key, params)
            if 'temp' in params:
                topic = f"home/{key}/temperature0/state"
                self.publish(topic, params, True)
            if 'relay' in params:
                topic = f"home/{key}/power0/state"
                self.publish(topic, params['relay'], True)
            if 'light' in params:
                topic = f"home/{key}/light0/state"
                self.publish(topic, params['light'], True)
            if 'pir' in params:
                topic = f"home/{key}/motion0/state"
                self.publish(topic, params['pir'], True)
