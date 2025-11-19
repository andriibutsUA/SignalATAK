import logging

from app.config import ATAKConfig, SignalConfig
from app.infrastructure.atak_sender import provide_atak_sender
from app.infrastructure.signal_atak_bot import provide_signal_atak_bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    atak_config = ATAKConfig()
    signal_config = SignalConfig()

    atak_sender = provide_atak_sender(atak_config)

    bot = provide_signal_atak_bot(signal_config, atak_sender)
    bot.start()
