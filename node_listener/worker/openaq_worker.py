import json
from node_listener.worker import Worker
import urllib
import urllib.error
import urllib.request


class OpenaqWorker(Worker):
    url = "https://api.openaq.org/v1/latest?"

    def __init__(self, city, location, user_agent):
        self.city = city
        self.location = location
        self.user_agent = user_agent
        self._validate()

    def _validate(self):
        if self.city is None and self.location is None:
            raise AttributeError("city or location must be set")

    def _fetch_data(self, url):
        try:
            request = urllib.request.Request(
                url, None, {'User-Agent': self.user_agent}
            )
            response = urllib.request.urlopen(request)
            data = response.read()
            json_data = json.loads(data.decode())
        except ValueError as e:
            json_data = None

        return json_data

    def _get_url(self):
        url = self.url
        if self.city is not None:
            url = url + "city="+self.city

        if self.location is not None:
            if self.city is not None:
                url = url+"&"
            url = url + "location="+self.location

        return url

    def _normalize(self, data):
        return None

    def execute(self):

        data = self._fetch_data(self._get_url())
        return self._normalize(data)