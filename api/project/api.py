import requests


class APIHandler(object):
    SECOND = "first"
    FIRST = "second"
    BASE_URL_PATTERN = "http://%s:%s"

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._base_url = self.BASE_URL_PATTERN % (self._host, self._port)

    def request_multiply(self, first, second):
        data_dict = {self.FIRST: first,
                     self.SECOND: second
                     }
        return requests.post(self._base_url,
                             data=data_dict)
