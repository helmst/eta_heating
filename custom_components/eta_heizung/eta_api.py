import requests
import xmltodict
import logging

_LOGGER = logging.getLogger(__name__)

class EtaApi:
    def __init__(self, host, port=8080):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"

    def _get(self, path):
        url = f"{self.base_url}{path}"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.text
        except Exception as ex:
            _LOGGER.error(f"GET {url} failed: {ex}")
            return None

    def _post(self, path, data):
        url = f"{self.base_url}{path}"
        try:
            resp = requests.post(url, data=data, timeout=10)
            resp.raise_for_status()
            return resp.text
        except Exception as ex:
            _LOGGER.error(f"POST {url} failed: {ex}")
            return None

    def get_menu(self):
        xml = self._get("/user/menu")
        if not xml:
            return None
        try:
            menu = xmltodict.parse(xml)
            return menu
        except Exception as ex:
            _LOGGER.error(f"Menu XML parsing failed: {ex}")
            return None

    def get_value(self, can_uri):
        xml = self._get(f"/user/var{can_uri}")
        if not xml:
            return None
        try:
            d = xmltodict.parse(xml)
            return d["eta"]["value"]
        except Exception as ex:
            _LOGGER.error(f"Value XML parsing failed: {ex}")
            return None

    def set_value(self, can_uri, value):
        xml = self._post(f"/user/var{can_uri}", {"value": value})
        if not xml:
            return None
        try:
            d = xmltodict.parse(xml)
            return d["eta"].get("success")
        except Exception as ex:
            _LOGGER.error(f"Set value XML parsing failed: {ex}")
            return None

    def get_errors(self):
        xml = self._get("/user/errors")
        if not xml:
            return None
        try:
            d = xmltodict.parse(xml)
            return d["eta"]["errors"]
        except Exception as ex:
            _LOGGER.error(f"Error XML parsing failed: {ex}")
            return None