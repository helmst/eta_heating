import logging
from .const import DOMAIN, CONF_HOST, CONF_PORT
from .eta_api import EtaApi

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, 8080)
    api = EtaApi(host, port)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "api": api,
        "sensors": entry.options.get("sensors", []),
        "switches": entry.options.get("switches", []),
        "numbers": entry.options.get("numbers", []),
    }
    await hass.config_entries.async_forward_entry_setups(
        entry, ["sensor", "switch", "number"]
    )
    return True

async def async_setup(hass, config):
    hass.data.setdefault(DOMAIN, {})
    return True