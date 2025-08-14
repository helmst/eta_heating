"""Home Assistant ETA Heizung setup."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_HOST, CONF_PORT
from .eta_api import EtaApi

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    host = config_entry.data[CONF_HOST]
    port = config_entry.data.get(CONF_PORT, 8080)
    api = EtaApi(host, port)
    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        "api": api,
        "sensors": config_entry.options.get("sensors", []),
        "switches": config_entry.options.get("switches", []),
        "numbers": config_entry.options.get("numbers", []),
    }
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "switch")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "number")
    )
    return True