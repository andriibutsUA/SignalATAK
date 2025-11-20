import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

COT_VERSION = "2.0"
COT_HOW = "h-e"  # human entered
COT_CALLSIGN = "Pentagon"

DEFAULT_STALE_MINUTES = 5

COT_TYPES = {
    "tank": "a-h-G-E-V-A-T",
    "apc": "a-h-G-E-V-A-A",
    "vehicle": "a-h-G-E-V",
    "truck": "a-h-G-E-V-C",
    "artillery": "a-h-G-E-W-A",
    "sam": "a-h-G-E-W-M-A-L",
    "mortar": "a-h-G-E-W-O",
    "aircraft": "a-h-A-M",
    "helicopter": "a-h-A-M-H",
    "uav": "a-h-A-M-F-Q",
    "infantry": "a-h-G-U-C-I",
}


class CoTMessage:
    def __init__(self, latitude: str, longitude: str, description: str) -> None:
        self._latitude = latitude
        self._longitude = longitude
        self._description = description
        self._cot_type = COT_TYPES.get(self._description.lower())

    def build_message(self) -> str:
        xml = self._build_xml()
        return ET.tostring(xml, encoding="unicode")

    def _build_xml(self) -> ET.Element:
        if not self._cot_type:
            raise ValueError("CoT type must be set")

        if not self._latitude or not self._longitude:
            raise ValueError("Location (lat/lon) must be set")

        uid = f"SIGBOT-{uuid.uuid4()}"
        now = datetime.now(tz=timezone.utc)
        now_str = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        stale = now + timedelta(minutes=DEFAULT_STALE_MINUTES)
        stale_str = stale.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        event = ET.Element("event")
        event.set("version", COT_VERSION)
        event.set("uid", uid)
        event.set("type", self._cot_type)
        event.set("time", now_str)
        event.set("start", now_str)
        event.set("stale", stale_str)
        event.set("how", COT_HOW)

        point = ET.SubElement(event, "point")
        point.set("lat", self._latitude)
        point.set("lon", self._longitude)
        point.set("hae", "0")
        point.set("ce", "1")
        point.set("le", "1")

        detail = ET.SubElement(event, "detail")
        contact = ET.SubElement(detail, "contact")
        contact.set("callsign", COT_CALLSIGN)
        remarks = ET.SubElement(detail, "remarks")
        remarks.text = self._description

        return event

    @classmethod
    def from_text_message(cls, latitude: str, longitude: str, description: str) -> str:
        builder = cls(latitude, longitude, description)
        return builder.build_message()
