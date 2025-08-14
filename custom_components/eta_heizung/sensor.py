from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity
from .const import DOMAIN
from .eta_api import EtaApi

async def async_setup_entry(hass, config_entry, async_add_entities):
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]
    entities = []
    for conf in hass.data[DOMAIN][config_entry.entry_id]["sensors"]:
        entities.append(EtaSensor(api, conf))
    async_add_entities(entities, True)

class EtaSensor(SensorEntity):
    def __init__(self, api: EtaApi, conf):
        self._api = api
        self._conf = conf
        self._name = conf["name"]
        self._uri = conf["uri"]
        self._unit = conf.get("unit")
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._state

    @property
    def native_unit_of_measurement(self):
        return self._unit

    async def async_update(self):
        value = self._api.get_value(self._uri)
        if value:
            self._state = value.get("#text")