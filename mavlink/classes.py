from enum import Enum, IntEnum
from config import DRONE_CONNECTION, STATION_CONNECTION

class StationState(IntEnum):
    UNKNOWN = 0
    OPEN = 1
    OPENING = 2
    CLOSED = 3
    CLOSING = 4
    LOCK_LOCK = 5
    LOCK_RELEASE = 6
    SERVICE = 10
    RESET = 11
    STANDBY = 12
    ERROR = 13


class StationCustomMode(IntEnum):
    LOCK_ON = 0
    LOCK_OFF = 1
    STOP = 12


class DroneConfig:
    CONNECTION_TIMEOUT = 6
    HEARTBEAT_DELAY = 0.5
    
    # Flight
    FLIGHT_DISTANCE = 0.00018 # 20 meters
    FLIGHT_ALT = 15
    
    # Minimum difference of position to update history
    MIN_POS_DIFFERENCE = 100


class StationConfig:
    CONNECTION_TIMEOUT = 3
    HEARTBEAT_DELAY = 0.5

    state = StationState
    custom_mode = StationCustomMode


class SystemState(Enum):
    IDLE = 'idle'
    OPENING = 'opening'
    RELEASING = 'releasing'
    FLYING = 'flying'
    LOCKING = 'locking'
    CLOSING = 'closing'
    ERROR = 'error'


class Config:
    # Connection
    DRONE_CONNECTION = DRONE_CONNECTION
    STATION_CONNECTION = STATION_CONNECTION
    DRONE_CONNECTION_TIMEOUT = 6
    STATION_CONNECTION_TIMEOUT = 3

    DRONE_HEARTBEAT_DELAY = 0.5

    # Flight
    FLIGHT_DISTANCE = 0.00018 # 20 meters
    FLIGHT_ALT = 15
    
    # Minimum difference of position to update history
    MIN_POS_DIFFERENCE = 100

    # Delay (seconds)
    TEST_DELAY = 1

    # Pos
    STATION_LAT = 55.7040408
    STATION_LON = 37.7244345
    STATION_ALT = 150
