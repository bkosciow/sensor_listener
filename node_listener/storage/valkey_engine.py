from . import StorageEngineInterface
import valkey
import json
from mergedeep import merge

GLUE = "."


class DictionaryEngine(StorageEngineInterface):
    def __init__(self, cfg):
        self.client = valkey.Valkey(host=cfg['host'], port=cfg['port'], db=cfg['db'])
        self.namespace = "sl"

    def set(self, key, value):
        try:
            valkey_key = f"{self.namespace}:{key}"
            existing_value = self.client.get(valkey_key)
            
            if existing_value is not None:
                existing_data = json.loads(existing_value)
                merged_value = merge({}, existing_data, value)
            else:
                merged_value = value
            
            json_value = json.dumps(merged_value)
            self.client.set(valkey_key, json_value)
        except Exception as e:
            print(f"Error setting key '{key}': {e}")
            print(f"Value: {value}")

    def get(self, key):
        try:
            valkey_key = f"{self.namespace}:{key}"
            value = self.client.get(valkey_key)

            if value is None:
                return None

            return json.loads(value)

        except Exception as e:
            print(f"Error getting key '{key}': {e}")
            return None

    def exists(self, key):
        try:
            valkey_key = f"{self.namespace}:{key}"
            return self.client.exists(valkey_key) > 0
        except Exception as e:
            print(f"Error checking existence of key '{key}': {e}")
            return False

    def close(self):
        self.client.close()

    def get_all(self):
        try:
            all_data = {}
            pattern = f"{self.namespace}:*"

            cursor = 0
            while True:
                cursor, keys = self.client.scan(cursor, pattern, count=100)
                if keys:
                    # Get values in bulk
                    values = self.client.mget(keys)
                    for i, key in enumerate(keys):
                        if values[i] is not None:
                            key_str = key.decode('utf-8')
                            original_key = key_str[len(self.namespace) + 1:]
                            all_data[original_key] = json.loads(values[i])

                if cursor == 0:
                    break

            return all_data

        except Exception as e:
            print(f"Error getting all data: {e}")
            return {}
