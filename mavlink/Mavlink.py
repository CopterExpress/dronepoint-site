from mavlink.DroneController import DroneController
import os
import logging
import time
import threading

from pymavlink import mavutil, mavwp
from pymavlink.mavutil import mavlink
import math
from .StationController import StationController
from .config import DronepointConfig as config
from .PrintObserver import observer

class Mavlink:
    def __init__(self):
        # Mission Execution param (bool)
        self.executing = False
        # Station Controller
        self.station_controller = StationController()
        # Drone Controller
        self.drone_controller = DroneController()
        # Custom mission
        self.custom_mission = True
    
    # Set custom mission parameter
    def set_custom_mission(self, custom_mission):
        if custom_mission is not None:
            self.custom_mission = bool(custom_mission)
    
    # Validate if it's possible to start test
    def validate_test(self, test_type):
        if test_type == 'drone':
            return self.drone_controller.connected
        elif test_type == 'station':
            return self.station_controller.connected
        elif test_type == 'full':
            return self.connected
    
    def test(self, test_type):
        # Debug
        observer.write('Start Executing Test')
        # Start async thread for test execution
        thread_test = threading.Thread(target=self.execute_test, args=(test_type,))
        thread_test.start()
    
    # Main Test
    def execute_test(self, test_type):
        # Validate Test Type
        if not self.validate_test(test_type):
            return observer.write(f"Can't start {test_type} Test. Drone or Station not connected")
        
        observer.write(f'Test Station type "{test_type}"')
        self.executing = True

        # Start Iteration depending on test type
        if test_type == 'drone':
            self.execute_flight()
        elif test_type == 'station':
            self.execute_iteration(flight=False)
            # self.execute_something()
        elif test_type == 'full':
            self.execute_iteration(flight=True)
        else:
            observer.write('Error. Invalid Test Type')

        self.executing = False

    def execute_flight(self):
        observer.write('Flight started')
        observer.write(f'start angle: {self.drone_controller.angle}')
        time_flight = self.drone_controller.execute_flight(custom_mission=self.custom_mission)
        observer.write(f'end angle: {self.drone_controller.angle}')
        observer.write(f'Flight ended in {time_flight}')

    def execute_iteration(self, flight=False):
        def open_irlock():
            observer.write('Opening Irlock')
            self.station_controller.send_command(config.STATE_SERVICE, config.CUSTOM_MODE_LOCK_ON)
        def close_irlock():
            observer.write('Closing Irlock')
            self.station_controller.send_command(config.STATE_SERVICE, config.CUSTOM_MODE_LOCK_OFF)

        # Debug
        observer.write(f'Iteration for station started')

        self.executing = True

        # Time Counter
        start_time = time.time()

        # Delay
        time.sleep(config.STATION_DELAY)

        # Open
        time_open = self.station_controller.execute_command(config.STATE_OPEN, 1)
        # Delay
        time.sleep(config.STATION_DELAY)
        
        open_irlock()
        # Delay
        time.sleep(config.STATION_DELAY)

        # Execute drone flight
        if flight:
            observer.write('Start flight function')
            time_flight = self.drone_controller.execute_flight(custom_mission=self.custom_mission)
        else:
            time_flight = 0.0
            observer.write('No flight')
        # Delay
        time.sleep(config.STATION_DELAY)

        # Lock
        time_lock = self.station_controller.execute_command(config.STATE_LOCK_LOCK)
        # Delay
        time.sleep(config.STATION_DELAY)

        time_close = self.station_controller.execute_command(config.STATE_CLOSED)
        # Delay
        time.sleep(config.STATION_DELAY)

        # Irlock off
        if flight:
            close_irlock()

        time_total = time_open + time_flight + time_lock + time_close
        
        # Debug
        observer.write(f'Iteration for station ended in {time.time() - start_time} s')

        self.executing = False
        
        # Final Message
        observer.write(f'Open: {round(time_open, 2)} s')
        observer.write(f'Flight: {round(time_flight, 2)} s')
        observer.write(f'Close: {round(time_close, 2)} s')
        observer.write(f'Total (no delay): {round(time_total, 2)} s')
        observer.write(f'Total: {round(time.time() - start_time, 2)} s')

    @property
    def connected(self):
        return self.station_controller.connected
    
    # Retrieve drone & dronepoint data
    def get_data(self):
        return {
            "pos": self.drone_controller.pos,
            "alt": self.drone_controller.alt,
            "armed": self.drone_controller.armed,
            "landing_state": self.drone_controller.landed_state,
            "executing": self.executing,
            "state": self.get_state(),
            "station_pos": [config.STATION_LAT, config.STATION_LON],
            "drone_history": self.drone_controller.history,
            "connection": {
                "drone": self.drone_controller.connected,
                "station": self.station_controller.connected,
            },
            "custom_mission": self.custom_mission,
        }
    
    # Dynamically get state of test
    def get_state(self):
        # Check flight
        if self.drone_controller.connected and self.drone_controller.armed:
            return config.FLYING
        # Check dronepoint states
        state_to_test = {
            config.STATE_STANDBY: config.IDLE,
            config.STATE_CLOSING: config.CLOSING,
            config.STATE_OPENING: config.OPENING,
            config.STATE_LOCK_RELEASE: config.RELEASING,
            config.STATE_LOCK_LOCK: config.LOCKING,
            config.STATE_ERROR: config.ERROR,
        }
        if not self.station_controller.connected:
            return config.IDLE
        if self.station_controller.custom_mode in state_to_test.keys():
            return state_to_test[self.station_controller.custom_mode]
        return config.IDLE

if __name__ == '__main__':
    mavlink = Mavlink()