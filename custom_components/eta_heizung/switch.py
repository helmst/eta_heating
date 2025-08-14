from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
from .eta_api import EtaApi

async def async_setup_entry(hass, config_entry, async_add_entities):
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]
    entities = []
    for conf in hass.data[DOMAIN][config_entry.entry_id]["switches"]:
        entities.append(EtaSwitch(api, conf))
    async_add_entities(entities, True)

class EtaSwitch(SwitchEntity):
    def __init__(self, api: EtaApi, conf):
        self._api = api
        self._conf = conf
        self._name = conf["name"]
        self._uri = conf["uri"]
        self._is_on = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._api.set_value(self._uri, self._conf.get("on_value", "1"))
        self._is_on = True

    async def async_turn_off(self, **kwargs):
        self._api.set_value(self._uri, self._conf.get("off_value", "0"))
        self._is_on = False

    async def async_update(self):
        value = self._api.get_value(self._uri)
        if value:
            self._is_on = value.get("#text") == self._conf.get("on_value", "1")