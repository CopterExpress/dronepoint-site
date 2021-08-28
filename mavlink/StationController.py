import os
import logging
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from .config import DronepointConfig as config
from .PrintObserver import observer


class StationController:
    def __init__(self):
        # Dronepoint connection url
        url = config.STATION_CONNECTION
        # Is connected
        self.connected = False
        # Dronepoint current custom mode
        self.custom_mode = config.STATE_STANDBY
        # Mavlink message handlers
        self.handlers = {
            0: self.HEARTBEAT_HANDLER
        }
        self.mavconn = mavutil.mavlink_connection(url, source_system=255)
        # Debug
        observer.write(f'Station initialized {url}. Waiting for connection')
        # Start sending heartbeat
        thread_send = threading.Thread(target=self.send_heartbeats)
        thread_send.start()
        # Start listening mavlink messages
        thread_listen = threading.Thread(target=self.listen_messages)
        thread_listen.start()
        # Cooldown
        time.sleep(1)
        # self.main()
    
    # Test code
    def main(self):
        # Debug
        observer.write('Started Station commands')
        self.execute_command(config.STATE_OPEN)

        # Delay
        time.sleep(config.STATION_DELAY)
        self.execute_command(config.STATE_CLOSED)
        # self.execute_command(
        #     config.STATE_UNLOADING_TO_USER,
        #     0, 3, 0,
        # )
        # # Delay
        # time.sleep(config.DRONEPOINT_DELAY)
        # self.execute_command(
        #     config.STATE_GETTING_FROM_USER,
        #     0, 3, 0,
        # )
        # # Delay
        # time.sleep(config.DRONEPOINT_DELAY)
        # self.execute_command(
        #     config.STATE_LOADING_DRONE,
        #     0, 3, 0, 3
        # )
    
    # Send random heartbeats to receive messages from Dronepoint
    def send_heartbeats(self):
        while True:
            self.mavconn.mav.heartbeat_send(
                0,
                0,
                0,
                0,
                0,
            )
            time.sleep(0.5)

    # Listen for mavlink messages and apply message handlers
    def listen_messages(self):
        observer.write('Started watching messages')
        while True:
            msg = self.mavconn.recv_match(blocking=True, timeout=config.STATION_CONNECTION_TIMEOUT)
            # Check if msg is None
            if not msg:
                if self.connected == True:
                    # Debug
                    observer.write('Station disconnected')
                    pass
                # Set state to disconnected
                self.connected = False
                continue
            else:
                if self.connected == False:
                    # Debug
                    observer.write('Station connected')
                # Set state to connected
                self.connected = True
            # Style messages
            msg_dict = msg.to_dict()
            msg_dict['msgid'] = msg.get_msgId()
            msg_dict['sysid'] = msg.get_srcSystem()
            msg_dict['compid'] = msg.get_srcComponent()
            del msg_dict['mavpackettype']
            # Convert NaN to None
            for key in msg_dict:
                if isinstance(msg_dict[key], float) and math.isnan(msg_dict[key]):
                    msg_dict[key] = None
            # Check if handler exists
            if msg_dict['msgid'] in self.handlers.keys():
                # Execute handlers
                self.handlers[msg_dict['msgid']](msg_dict)
    
    def send_command(self, mode, param1=0, param2=0, param3=0, param4=0, param5=0):
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

    # Execute Dronepoint command via command long
    def execute_command(self, mode, param1=0, param2=0, param3=0, param4=0, param5=0):
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
        
        # Wait until dronepoint custom_mode is in STANDBY mode (12)
        time.sleep(3)
        # Time counter
        start_time = time.time()
        while True:
            i = 1
            if self.custom_mode == config.STATE_STANDBY:
                break
            # Debug
            if i % 10 == 0:
                observer.write('Executing command')
            # Cooldown
            time.sleep(1)
        # Debug
        observer.write(f'Command {mode} finished in time {time.time() - start_time} s')
        return time.time() - start_time
    
    # Heartbeat listener (0): update dronepoint's custom mode
    def HEARTBEAT_HANDLER(self, msg):
        if msg['type'] == 31:
            state = msg['custom_mode']
            if self.custom_mode != state:
                self.custom_mode = state
                # Debug
                observer.write(f'Changed to custom mode {state}')