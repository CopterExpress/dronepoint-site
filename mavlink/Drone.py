from .MavlinkVehicle import MavlinkVehicle
import os
import logging
from socket import timeout
import time
import threading
from typing import Callable

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from .classes import DroneConfig

# Initialize waypoint
wp = mavwp.MAVWPLoader()

class Drone(MavlinkVehicle):
    def __init__(self, connection_url: str) -> None:
        # Drone parameters
        self.pos = [0, 0]
        self.alt = 0
        self.angle = 0
        self.armed = False
        self.landed_state = 0
        # Current mission item
        self.mission_item = 0
        # History of position
        self.history = []
        # Mavlink message handlers
        handlers = {
            mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT: self.GLOBAL_POSITION_INT_HANDLER,
            mavlink.MAVLINK_MSG_ID_EXTENDED_SYS_STATE: self.EXTENDED_SYS_STATE_HANDLER,
            mavlink.MAVLINK_MSG_ID_HEARTBEAT: self.HEARTBEAT_HANDLER,
            mavlink.MAVLINK_MSG_ID_MISSION_CURRENT: self.MISSION_ITEM_HANDLER,
            # mavlink.MAVLINK_MSG_ID_GPS_RAW_INT: self.GLOBAL_POSITION_INT_HANDLER,
        }
        # Init connection
        super().__init__(
            connection_url, 
            handlers, 
            name="Drone", 
            connection_timeout=DroneConfig.CONNECTION_TIMEOUT, 
            heartbeat_delay=DroneConfig.HEARTBEAT_DELAY
        )
    
    # Global position int listener: update drone's position
    def GLOBAL_POSITION_INT_HANDLER(self, msg_dict: dict):
        # Get GPS Position
        pos = [msg_dict['lat'] / 10000000, msg_dict['lon'] / 10000000]

        # Check if Difference is big enough
        last_pos = self.history[-1] if len(self.history) > 0 else self.pos[:]
        pos_difference = [abs(pos[i] - last_pos[i]) * 10000000 for i in range(len(pos))]
        alt = msg_dict['alt'] / 1000
        self.pos = pos[:]
        self.alt = alt
        self.angle = msg_dict['hdg'] / 100
        # If difference is big enough, update history
        if (
            pos_difference[0] > DroneConfig.MIN_POS_DIFFERENCE or 
            pos_difference[1] > DroneConfig.MIN_POS_DIFFERENCE
        ):
            self.history.append(pos[:])
    
    # Current mission item listener: update drone's current mission item
    def MISSION_ITEM_HANDLER(self, msg_dict: dict):
        item = msg_dict['seq']
        if self.mission_item != item:
            self.msg_write(f'Reached mission item {item}')
        self.mission_item = item
    
    # Heartbeat listener: update drone's state (armed)
    def HEARTBEAT_HANDLER(self, msg_dict: dict):
        self.armed = (msg_dict['base_mode'] & mavlink.MAV_MODE_FLAG_SAFETY_ARMED) != 0
    
    # Extended sys state listener: update drone's landed_state
    def EXTENDED_SYS_STATE_HANDLER(self, msg_dict: dict):
        # Get landed state
        landed_state = msg_dict['landed_state']
        # Check if different from previous
        if landed_state != self.landed_state:
            self.landed_state = landed_state
            self.msg_write(f"Updated Landed State to {landed_state}")

    # Set home
    def set_home(self, homelocation, altitude):
        self.msg_write('Setting Home')
        self.mavconn.mav.command_long_send(
            self.mavconn.target_system, self.mavconn.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_HOME,
            1, # set position
            0, # param1
            0, # param2
            0, # param3
            0, # param4
            homelocation[0], # lat
            homelocation[1], # lon
            altitude)
    
    def create_waypoints(self):
        wp.clear()
        # Frame
        frame = mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        # Takeoff
        p = mavlink.MAVLink_mission_item_message(
            self.mavconn.target_system,
            self.mavconn.target_component,
            0,
            frame,
            mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            1,
            15, 0, 0, math.nan,
            self.pos[0],
            self.pos[1],
            DroneConfig.FLIGHT_ALT,
        )
        wp.add(p)
        # Flight
        point = [self.pos[0] + DroneConfig.FLIGHT_DISTANCE, self.pos[1]]
        p = mavlink.MAVLink_mission_item_message(
            self.mavconn.target_system,
            self.mavconn.target_component,
            1,
            frame,
            mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            1,
            0, 10, 0, math.nan,
            point[0],
            point[1],
            DroneConfig.FLIGHT_ALT,
        )
        wp.add(p)
        point = [self.pos[0] + DroneConfig.FLIGHT_DISTANCE, self.pos[1] + DroneConfig.FLIGHT_DISTANCE]
        p = mavlink.MAVLink_mission_item_message(
            self.mavconn.target_system,
            self.mavconn.target_component,
            1,
            frame,
            mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            1,
            0, 10, 0, math.nan,
            point[0],
            point[1],
            DroneConfig.FLIGHT_ALT,
        )
        wp.add(p)
        point = [self.pos[0], self.pos[1] + DroneConfig.FLIGHT_DISTANCE]
        p = mavlink.MAVLink_mission_item_message(
            self.mavconn.target_system,
            self.mavconn.target_component,
            1,
            frame,
            mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            1,
            0, 10, 0, math.nan,
            point[0],
            point[1],
            DroneConfig.FLIGHT_ALT,
        )
        wp.add(p)
        point = [self.pos[0], self.pos[1]]
        p = mavlink.MAVLink_mission_item_message(
            self.mavconn.target_system,
            self.mavconn.target_component,
            1,
            frame,
            mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            1,
            0, 10, 0, self.angle,
            point[0],
            point[1],
            DroneConfig.FLIGHT_ALT,
        )
        wp.add(p)
        # Land
        p = mavlink.MAVLink_mission_item_message(
            self.mavconn.target_system,
            self.mavconn.target_component,
            2,
            frame,
            mavlink.MAV_CMD_NAV_LAND,
            0,
            1,
            0, 
            2, # Precision land mode 
            0, 
            self.angle, # Angle
            self.pos[0], # Lat 
            self.pos[1], # Lon
            0, # Alt
        )
        wp.add(p)
    
    def execute_flight(self, last_item_handler=None, custom_mission=False):
        # Clear old history
        self.history = [self.pos[:]]
        # Start mission
        mission_count = self.start_mission(custom_mission)
        # Cooldown
        time.sleep(15)
        # Time Counter
        start_time = time.time()

        called = False
        while self.armed:
            # Debug
            time.sleep(2)
            # Check if last mission item is reached
            if self.mission_item == mission_count - 1 and not called:
                called = True
                if last_item_handler:
                    last_item_handler()
        # Debug
        self.msg_write(f'Finished Flight in {time.time() - start_time} s')
        return time.time() - start_time

    def start_mission(self, custom_mission: bool):
        custom_msg = 'WITH' if custom_mission else 'WITHOUT'
        self.msg_write(f'Initiating Flight Mission {custom_msg} Custom Mission')

        if custom_mission:
            self.create_waypoints()
            # Send waypoints
            while True:
                self.msg_write('Clearing waypoints')
                self.mavconn.waypoint_clear_all_send()
                mission_ack = self.mavconn.recv_match(type=['MISSION_ACK'], blocking=True, timeout=2)
                if mission_ack:
                    break
            self.msg_write(str(mission_ack))
            time.sleep(2)
            self.msg_write('Sending waypoint count')
            self.mavconn.waypoint_count_send(wp.count())

            for i in range(wp.count()):
                msg = self.mavconn.recv_match(
                    type=['MISSION_REQUEST', 'MISSION_REQUEST_INT'], 
                    blocking=True
                )
                self.msg_write(str(msg))
                self.mavconn.mav.send(wp.wp(msg.seq))
                self.msg_write(f'Sending waypoint {msg.seq}')
        
        time.sleep(3)
        # Start Mission (Arm Drone)
        while True:
            self.mavconn.set_mode_auto()
            command_ack = self.mavconn.recv_match(
                type=['COMMAND_ACK'],
                blocking=True,
                timeout=2
            )
            self.msg_write('Resending mission start')
            if command_ack:
                break
        # while True:
        #     self.mavconn.mav.command_long_send(
        #             self.mavconn.target_system,
        #             self.mavconn.target_component,
        #             mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        #             0,
        #             1, 0, 0, 0, 0, 0, 0
        #         )
        #     command_ack = self.mavconn.recv_match(
        #         type=['COMMAND_ACK'],
        #         blocking=True,
        #         timeout=2
        #     )
        #     if command_ack:
        #         break
        self.msg_write('Command ack')
        self.msg_write(f'Started Mission with {wp.count()} waypoints')
        return wp.count() if custom_mission else 5