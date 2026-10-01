import json
import re

from lupus_to_mqtt.MQTT import MQTT
from . import Sensor


class LightSensor(Sensor):
    """Class representing a Lupusec light sensor."""

    def __init__(self, data, panel):
        self._lux = self._parse_lux(data.get('status'))
        super().__init__(data, panel)

    def _parse_lux(self, status):
        if not status:
            return 0

        match = re.search(r'(-?\d+(?:\.\d+)?)\s*$', status)
        return float(match.group(1)) if match else 0

    def registerDevice(self):
        mqtt = MQTT.getInstance()

        msg_config = json.dumps({
            "name": self.name,
            "unique_id": self._id,
            "device_class": "illuminance",
            "unit_of_measurement": "lx",
            "state_class": "measurement",
            "availability_topic": self._panel.device_name + "/availability",
            "state_topic": f"{self._panel.device_name}/{self._id}/state",
            "device": {
                "identifiers": self._sid,
                "manufacturer": self._panel.manufacturer,
                "name": self.name,
            }
        })

        mqtt.publish_message(
            f"homeassistant/sensor/{self._id}/config",
            msg_config
        )

        self.sendUpdate()

    def updateFromData(self, data):
        new_lux = self._parse_lux(data.get('status'))

        updated = self._lux != new_lux
        self._lux = new_lux

        return updated

    def sendUpdate(self):
        mqtt = MQTT.getInstance()

        mqtt.publish_message(
            f"{self._panel.device_name}/{self._id}/state",
            str(self._lux)
        )
