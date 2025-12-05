import requests
import json
import logging

logger = logging.getLogger(__name__)


class Apprise:
    def __init__(self, cfg):
        self.cfg = cfg
        self.headers = {
            'content-type': 'application/json',
        }

    def info(self, message, title="Info"):
        response = requests.post(
            self.cfg['url'],
            headers={
                'content-type': 'application/json',
            },
            data=json.dumps({
                'body': message,
                'title': title,
                "tag": self.cfg['tag']
            })
        )
        if response.status_code > 299:
            logging.error(response.status_code)
            logging.error(response.content)


class ErrorHandler(logging.Handler):
    def __init__(self, cfg):
        logging.Handler.__init__(self=self)
        self.cfg = cfg
        self.headers = {
            'content-type': 'application/json',
        }
        self.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s'))

    def emit(self, record):
        print(record)
        try:
            response = requests.post(
                self.cfg['url'],
                headers={
                    'content-type': 'application/json',
                },
                data=json.dumps({
                    'body': self.format(record),
                    'title': "❌ Error",
                    "tag": self.cfg['tag']
                })
            )
        except Exception as e:
            print(e)
