from homeassistant.components.number import NumberEntity
from .const import DOMAIN
from .eta_api import EtaApi

async def async_setup_entry(hass, config_entry, async_add_entities):
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]
    entities = []
    for conf in hass.data[DOMAIN][config_entry.entry_id]["numbers"]:
        entities.append(EtaNumber(api, conf))
    async_add_entities(entities, True)

class EtaNumber(NumberEntity):
    def __init__(self, api: EtaApi, conf):
        self._api = api
        self._conf = conf
        self._name = conf["name"]
        self._uri = conf["uri"]
        self._min = conf.get("min", 0)
        self._max = conf.get("max", 100)
        self._value = None

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._value

    @property
    def native_min_value(self):
        return self._min

    @property
    def native_max_value(self):
        return self._max

    async def async_set_native_value(self, value):
        self._api.set_value(self._uri, str(int(value)))
        self._value = value

    async def async_update(self):
        value = self._api.get_value(self._uri)
        if value:
            try:
                self._value = float(value.get("#text"))
            except Exception:
                self._value = None