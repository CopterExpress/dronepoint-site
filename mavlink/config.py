from config import DRONE_CONNECTION, STATION_CONNECTION

class DronepointConfig:
    # Modes
    CUSTOM_MODE_LOCK_ON = 0
    CUSTOM_MODE_LOCK_OFF = 1
    CUSTOM_MODE_STOP = 12

    # Connection
    DRONE_CONNECTION = DRONE_CONNECTION
    STATION_CONNECTION = STATION_CONNECTION
    DRONE_CONNECTION_TIMEOUT = 6
    STATION_CONNECTION_TIMEOUT = 3

    # Flight
    FLIGHT_DISTANCE = 0.00018 # 20 meters
    FLIGHT_ALT = 20
    
    # Minimum difference of position to update history
    MIN_POS_DIFFERENCE = 100

    # State
    IDLE = 'idle'
    OPENING = 'opening'
    RELEASING = 'releasing'
    FLYING = 'flying'
    LOCKING = 'locking'
    CLOSING = 'closing'
    ERROR = 'error'

    # DP State
    STATE_UNKNOWN = 0
    STATE_OPEN = 1
    STATE_OPENING = 2
    STATE_CLOSED = 3
    STATE_CLOSING = 4
    STATE_LOCK_LOCK = 5
    STATE_LOCK_RELEASE = 6
    STATE_SERVICE = 10
    STATE_RESET = 11
    STATE_STANDBY = 12
    STATE_ERROR = 13

    # DP Delay (seconds)
    STATION_DELAY = 1

    # DP Pos
    STATION_LAT = 55.7040408
    STATION_LON = 37.7244345
    STATION_ALT = 150