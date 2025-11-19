import asyncio
import logging
import socket

from app.config import ATAKConfig
from app.exceptions import ATAKException

logger = logging.getLogger(__name__)


class ATAKSender:
    def __init__(self, host: str = "127.0.0.1", port: int = 4242, timeout: int = 10):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._sock: socket.socket | None = None

    @property
    def is_connected(self) -> bool:
        return self._sock is not None

    async def connect(self) -> None:
        if self.is_connected:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)
        self._sock = sock
        logger.info(f"Initialized ATAK UDP socket for {self._host}:{self._port}")

    async def send(self, cot_message: str) -> None:
        if not self.is_connected:
            await self.connect()

        assert self._sock is not None

        data = cot_message.encode("utf-8")
        loop = asyncio.get_running_loop()

        try:
            await asyncio.wait_for(
                loop.sock_sendto(self._sock, data, (self._host, self._port)),
                timeout=self._timeout,
            )
            logger.debug(
                "Sent CoT message via UDP to %s:%d",
                len(data),
                self._host,
                self._port,
            )
        except (OSError, asyncio.TimeoutError) as e:
            logger.error(
                f"Failed to send CoT message to {self._host}:{self._port}: {e}"
            )
            raise ATAKException(f"Send failed: {e}") from e

    async def close(self) -> None:
        if self._sock is not None:
            try:
                self._sock.close()
                logger.info("ATAK UDP socket closed")
            finally:
                self._sock = None


def provide_atak_sender(atak_config: ATAKConfig) -> ATAKSender:
    return ATAKSender(
        host=atak_config.atak_host,
        port=atak_config.atak_port,
        timeout=atak_config.timeout,
    )
