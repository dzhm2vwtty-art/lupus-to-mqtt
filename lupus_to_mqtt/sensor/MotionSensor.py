import json

from lupus_to_mqtt.MQTT import MQTT

from . import AlarmSensor


class MotionSensor(AlarmSensor.AlarmSensor):
    """Class representing a motion detector."""

    def registerDevice(self):
        mqtt = MQTT.getInstance()

        msg_config = json.dumps({
            "name": self.name,
            "unique_id": self._id,
            "device_class": "motion",
            "availability_topic": self._panel.device_name + "/availability",
            "state_topic": f"{self._panel.device_name}/{self._id}/state",
            "payload_on": "ON",
            "payload_off": "OFF",
            "device": {
                "identifiers": self._sid,
                "manufacturer": self._panel.manufacturer,
                "name": self.name,
            }
        })

        mqtt.publish_message(
            f"homeassistant/binary_sensor/{self._id}/config",
            msg_config
        )

        self.sendUpdate()

    def sendUpdate(self):
        mqtt = MQTT.getInstance()
        mqtt.publish_message(
            f"{self._panel.device_name}/{self._id}/state",
            "ON" if self.isBurglarAlarm() else "OFF"
        )
