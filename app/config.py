import os
from dataclasses import dataclass


@dataclass
class SignalConfig:
    signal_service_host: str = os.environ.get("SIGNAL_SERVICE_HOST")
    signal_service_port: int = os.environ.get("SIGNAL_SERVICE_PORT")
    signal_bot_phone_number: str = os.getenv("SIGNAL_BOT_PHONE", "+380971111111")

    @property
    def signal_service_url(self) -> str:
        return self.signal_service_host + ":" + str(self.signal_service_port)


@dataclass
class ATAKConfig:
    atak_host: str = os.getenv("ATAK_HOST", "192.168.0.157")
    atak_port: int = int(os.getenv("ATAK_PORT", 4242))
    timeout: int = int(os.getenv("ATAK_TIMEOUT", 5))
