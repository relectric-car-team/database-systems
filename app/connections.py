from __future__ import annotations

import zmq
from loguru import logger


class DBNet:
    def __init__(self, core_frontend_address: str):
        """Client endpoint for database communication.

        Args:
            core_frontend_address (str)
        """
        context = zmq.Context.instance()

        self.core_frontend_address = core_frontend_address
        self.identity = "database"

        self.socket = context.socket(zmq.DEALER)
        self.socket.identity = self.identity.encode("ascii")

    def run(self):
        """Loop for user interface to server connection, primarily through __call__."""
        if not self.connect_to_server():
            logger.info(f"{self.identity} quitting")
            return

        while True:
            incoming_message = self.socket.recv_json()
            logger.debug(f"{self.identity} received: {incoming_message}")
            # Add message processing

    def connect_to_server(self) -> bool:
        self.socket.connect(self.core_frontend_address)
        logger.info(f"{self.identity} started, connecting to {self.core_frontend_address}")

        if self.register_to_server():
            logger.success(f"{self.identity}: Connection established")
            return True
        else:
            logger.error(f"{self.identity}: Connection failure")
            return False

    def register_to_server(self, ready_message: bytes = b"ready") -> bool:
        self.socket.send(bytes(self.identity, "utf-8"))
        ready_ping = self.socket.recv()
        return ready_message in ready_ping

    def __call__(self) -> None:
        try:
            self.run()
        except KeyboardInterrupt:
            self.socket.close()
