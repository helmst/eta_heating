"""ETA Heizung Home Assistant Integration."""
import logging
from .const import DOMAIN, CONF_HOST, CONF_PORT
from .eta_api import EtaApi

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry):
    host = config_entry.data[CONF_HOST]
    port = config_entry.data.get(CONF_PORT, 8080)
    api = EtaApi(host, port)
    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        "api": api,
        "sensors": config_entry.options.get("sensors", []),
        "switches": config_entry.options.get("switches", []),
        "numbers": config_entry.options.get("numbers", []),
    }
    await hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    await hass.config_entries.async_forward_entry_setup(config_entry, "switch")
    await hass.config_entries.async_forward_entry_setup(config_entry, "number")
    return True

async def async_setup(hass, config):
    """Support YAML setup (falls gewünscht)."""
    hass.data.setdefault(DOMAIN, {})
    return True