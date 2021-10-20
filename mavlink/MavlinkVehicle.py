from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
from .PrintObserver import observer
import time
import threading
import math
from typing import Callable

# Handles connection and messages logic
class MavlinkVehicle:
    def __init__(
        self, 
        connection_url: str, 
        handlers: dict,
        name: str,
        connection_timeout: float,
        heartbeat_delay: float,
    ) -> None:
        # Is connected
        self.connected = False
        # Params
        self.name = name
        self.handlers = handlers
        self.connection_url = connection_url
        self.connection_timeout = connection_timeout
        self.heartbeat_delay = heartbeat_delay
        # Connect
        self.mavconn = mavutil.mavlink_connection(self.connection_url, source_system=255)
        # Debug
        self.msg_write(f'Initialized on {self.connection_url}. Waiting for connection')
        # Start sending heartbeat
        thread_send = threading.Thread(target=self.send_heartbeats)
        thread_send.start()
        # Start listening mavlink messages
        thread_listen = threading.Thread(target=self.listen_messages)
        thread_listen.start()
        # Cooldown
        time.sleep(1)
    
    # Debug
    def msg_write(self, msg: str) -> None:
        observer.write(f'{self.name}: {msg}')
    
    # Listen for mavlink messages and apply message handlers
    def listen_messages(self):
        self.msg_write('Started watching messages')
        while True:
            msg = self.mavconn.recv_match(
                blocking=True, 
                timeout=self.connection_timeout,
            )
            # Check if msg is None
            if not msg:
                # Set state to disconnected
                if self.connected == True:
                    # Debug
                    self.msg_write('Disconnected')
                self.connected = False
                continue
            else:
                if self.connected == False:
                    # Debug
                    self.msg_write('Connected')
                # Set state to connected
                self.connected = True
            # Style messages
            msg_dict: dict = msg.to_dict()
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
    
    # Send random heartbeats to receive messages from Drone
    def send_heartbeats(self):
        while True:
            self.mavconn.mav.heartbeat_send(
                # 0,
                # 0,
                # 0,
                # 0,
                # 0,
                mavlink.MAV_TYPE_GCS,
                mavlink.MAV_AUTOPILOT_GENERIC,
                0,
                0,
                0,
            )
            time.sleep(self.heartbeat_delay)