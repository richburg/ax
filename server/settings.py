from typing import Final, Union

HOST: Final[str] = "0.0.0.0"
PORT: Final[int] = 5000

MAX_REQUESTS_PER_SECOND: Final[int] = 4
MAX_REQUEST_SIZE_IN_BYTES: Final[int] = 1024
MAX_CLIENT_COUNT: Final[int] = 50

HEARTBEAT_INTERVAL_IN_SECONDS: Union[int, float] = 20
HEARTBEAT_TIMEOUT_IN_SECONDS: Union[int, float] = HEARTBEAT_INTERVAL_IN_SECONDS * 1.5
