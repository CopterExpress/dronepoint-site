from .MavlinkVehicle import MavlinkVehicle
import os
import logging
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from .classes import StationConfig

class Station(MavlinkVehicle):
    def __init__(self, connection_url: str) -> None:
        # Dronepoint current custom mode
        self.custom_mode = StationConfig.state.STANDBY
        # Mavlink message handlers
        handlers = {
            mavlink.MAVLINK_MSG_ID_HEARTBEAT: self.HEARTBEAT_HANDLER
        }
        # Init connection
        super().__init__(
            connection_url, 
            handlers, 
            name="Station", 
            connection_timeout=StationConfig.CONNECTION_TIMEOUT, 
            heartbeat_delay=StationConfig.HEARTBEAT_DELAY
        )
    
    def _send_command(
        self, 
        mode: StationConfig.state, 
        param1: StationConfig.custom_mode=0, 
        param2=0, param3=0, param4=0, param5=0
    ):
        # Send command
        self.mavconn.mav.command_long_send(
            self.mavconn.target_system,
            self.mavconn.target_component,
            mavlink.MAV_CMD_DO_SET_MODE,
            1,
            mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode,
            param1, param2, param3,
            param4, param5,
        )
    
    def open_irlock(self):
        self._send_command(StationConfig.state.SERVICE, StationConfig.custom_mode.LOCK_ON)
    
    def close_irlock(self):
        self._send_command(StationConfig.state.SERVICE, StationConfig.custom_mode.LOCK_OFF)

    def execute_command(
        self, 
        mode: StationConfig.state, 
        param1: StationConfig.custom_mode=0, 
        param2=0, param3=0, param4=0, param5=0
    ) -> float:
        self._send_command(self, mode, param1, param2, param3, param4, param5)
        # Wait until custom_mode is in STANDBY mode (12)
        time.sleep(3)
        # Time counter
        start_time = time.time()
        while True:
            i = 1
            if self.custom_mode == StationConfig.state.STANDBY:
                break
            # Debug
            if i % 10 == 0:
                self.msg_write('Executing command')
            # Cooldown
            time.sleep(1)
        # Debug
        self.msg_write(f'Command {mode} finished in time {time.time() - start_time} s')
        return time.time() - start_time
    
    # Heartbeat listener (0): update dronepoint's custom mode
    def HEARTBEAT_HANDLER(self, msg: dict):
        if msg['type'] == 31:
            state = msg['custom_mode']
            if self.custom_mode != state:
                self.custom_mode = state
                # Debug
                self.msg_write(f'Changed to custom mode {state}')