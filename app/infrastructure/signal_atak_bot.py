import logging
import re

from signalbot import (
    Command,
    Context,
    SignalBot,
    enable_console_logging,
    regex_triggered,
    triggered,
)

from app.config import SignalConfig
from app.exceptions import ATAKException
from app.infrastructure.atak_sender import ATAKSender
from app.infrastructure.cot import COT_TYPES, CoTMessage

logger = logging.getLogger(__name__)

MESSAGE_REGEX_PATTERN = (
    r"^(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(.+)$"  # 48.567123 39.87897 tank
)


class HelpCommand(Command):
    @triggered("help", case_sensitive=False)
    async def handle(self, c: Context) -> None:
        text = (
            "Signal to ATAK Bot \n"
            "Send coordinates in this format: \n"
            "LAT LON DESCRIPTION \n"
            "Examples:\n"
            "* 48.567123 39.87897 tank\n"
            "* 50.450001 30.523333 apc\n"
            "Test commands:\n"
            "* types - Show target types\n"
            "* help - Show this message\n"
        )

        await c.send(text)


class TypesCommand(Command):
    @triggered("types", case_sensitive=False)
    async def handle(self, c: Context) -> None:
        await c.send(", ".join(COT_TYPES.keys()))


class ATAKCommand(Command):
    @regex_triggered(MESSAGE_REGEX_PATTERN)
    async def handle(self, c: Context) -> None:
        bot = c.bot
        lat, lon, desc = bot.parse_message(c.message.text)

        try:
            await bot.send_to_atak(lat, lon, desc)
            await c.send("Data sent to ATAK")
        except ATAKException:
            await c.send("Could not send message to ATAK, contact administrator")


class SignalATAKBot(SignalBot):
    def __init__(
        self,
        signal_service_connection: str,
        signal_phone_number: str,
        atak_sender: ATAKSender,
    ) -> None:
        super().__init__(
            {
                "signal_service": signal_service_connection,
                "phone_number": signal_phone_number,
            }
        )
        self._atak_sender = atak_sender

    def parse_message(self, message: str) -> tuple[str, str, str]:
        match = re.match(MESSAGE_REGEX_PATTERN, message)
        lat, lon, desc = match.groups()

        return str(lat), str(lon), str(desc.strip())

    async def send_to_atak(self, lat: str, lon: str, desc: str) -> None:
        cot_message = CoTMessage.from_text_message(
            latitude=lat, longitude=lon, description=desc
        )
        logger.info(f"Sending cot message: {cot_message}")
        await self._atak_sender.send(cot_message)


def provide_signal_atak_bot(
    signal_config: SignalConfig, atak_sender: ATAKSender
) -> SignalBot:
    enable_console_logging(logging.INFO)

    bot = SignalATAKBot(
        signal_config.signal_service_url,
        signal_config.signal_bot_phone_number,
        atak_sender,
    )

    bot.register(HelpCommand())
    bot.register(ATAKCommand())
    bot.register(TypesCommand())

    return bot
