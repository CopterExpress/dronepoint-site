from .Station import Station
from .Drone import Drone
import os
import logging
import time
import threading

import math
from .PrintObserver import observer
from config import DRONE_CONNECTION, STATION_CONNECTION
from .classes import StationConfig, SystemState, Config

class Mavlink:
    def __init__(self):
        # Mission Execution param (bool)
        self.executing = False
        # Station Controller
        self.station_controller = Station(STATION_CONNECTION)
        # Drone Controller
        self.drone_controller = Drone(DRONE_CONNECTION)
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

    def execute_iteration(self, flight: bool=False):
        def open_irlock():
            observer.write('Opening Irlock')
            self.station_controller.open_irlock()
        def close_irlock():
            observer.write('Closing Irlock')
            self.station_controller.close_irlock()

        # Debug
        observer.write(f'Iteration for station started')

        self.executing = True

        # Time Counter
        start_time = time.time()

        # Delay
        time.sleep(Config.TEST_DELAY)

        # Open
        time_open = self.station_controller.execute_command(StationConfig.state.OPEN, 1)
        # Delay
        time.sleep(Config.TEST_DELAY)
        
        open_irlock()
        # Delay
        time.sleep(Config.TEST_DELAY)

        # Execute drone flight
        if flight:
            observer.write('Start flight function')
            time_flight = self.drone_controller.execute_flight(custom_mission=self.custom_mission)
        else:
            time_flight = 0.0
            observer.write('No flight')
        # Delay
        time.sleep(Config.TEST_DELAY)

        # Lock
        time_lock = self.station_controller.execute_command(StationConfig.state.LOCK_LOCK)
        # Delay
        time.sleep(Config.TEST_DELAY)

        time_close = self.station_controller.execute_command(StationConfig.state.CLOSED)
        # Delay
        time.sleep(Config.TEST_DELAY)

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
            "state": self.get_state().value,
            "station_pos": [Config.STATION_LAT, Config.STATION_LON],
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
            return SystemState.FLYING
        # Check dronepoint states
        state_to_test = {
            StationConfig.state.STANDBY: SystemState.IDLE,
            StationConfig.state.CLOSING: SystemState.CLOSING,
            StationConfig.state.OPENING: SystemState.OPENING,
            StationConfig.state.LOCK_RELEASE: SystemState.RELEASING,
            StationConfig.state.LOCK_LOCK: SystemState.LOCKING,
            StationConfig.state.ERROR: SystemState.ERROR,
        }
        if not self.station_controller.connected:
            return SystemState.IDLE
        if self.station_controller.custom_mode in state_to_test.keys():
            return state_to_test[self.station_controller.custom_mode]
        return SystemState.IDLE

if __name__ == '__main__':
    mavlink = Mavlink()