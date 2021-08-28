#!/usr/bin/python2
# -*- coding: utf-8 -*-
import time, os, sys


from pymavlink import mavutil
import threading
import json


#CUSTOM_MODE
CUSTOM_MODE_UNKNOWN=0
KUPOL_OPEN=1
KUPOL_CLOSE=3
LOCK_LOCK = 5
LOCK_RELEASE = 6
SERVICE = 10
RESET = 11
STANDBY = 12
ERROR = 13

#CUSTOM_SUBMODE
IRLOCK_ON = 0
IRLOCK_OFF = 1
STOP = 12

CCSM=12
NUMO=0


master = mavutil.mavlink_connection('udpout:192.168.194.183:14542')

def telemet():
    #show incoming mavlink messages
    global CCSM
    while True:
        msg =  master.recv_match(type = 'HEARTBEAT', blocking = False)
        if not msg:
            continue
        else:
            #print(msg)
            try:
              state = msg.to_dict()
              #print(state)
              if state.get("type")==31:
                #print(state)
                CCSM = state.get("custom_mode")
                print("CUSTOM_MODE =", CCSM)
            except ValueError as e:  # Incorrect message                  
              print(e)

def sendheard():
      '''heartbeat bistro'''
      while True:
            try:
              master.mav.heartbeat_send(0,0,0,0,0)
              time.sleep(1)
            except ValueError as e:  # nemogu message send                 
              print(e)


task1 = threading.Thread(target=telemet)
task2 = threading.Thread(target=sendheard)
task1.start()
task2.start()


while True:
   try:  
         print("otkryt kupol") #2
         master.mav.command_long_send(master.target_system, master.target_component,
                                  mavutil.mavlink.MAV_CMD_DO_SET_MODE, 1,
                                  mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                  KUPOL_OPEN, 0, 0, 0, 0, 0)
         time.sleep(5)
         while CCSM!=12:
           pass
         print("zakryt kupol") #4
         master.mav.command_long_send(master.target_system, master.target_component,
                                  mavutil.mavlink.MAV_CMD_DO_SET_MODE, 1,
                                  mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                  KUPOL_CLOSE, 0, 0, 0, 0, 0)
         time.sleep(5)
         while CCSM!=12:
           pass
         print("otkryt kupol i razdvinut mehanizm") #2
         master.mav.command_long_send(master.target_system, master.target_component,
                                  mavutil.mavlink.MAV_CMD_DO_SET_MODE, 1,
                                  mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                  KUPOL_OPEN, 1, 0, 0, 0, 0)
         time.sleep(5)
         while CCSM!=12:
           pass
         print("razdvinut mehanizm") #6
         master.mav.command_long_send(master.target_system, master.target_component,
                                  mavutil.mavlink.MAV_CMD_DO_SET_MODE, 1,
                                  mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                  LOCK_RELEASE, 0, 0, 0, 0, 0)
         time.sleep(5)
         while CCSM!=12:
           pass
         print("sdvinut mehanizm") #5
         master.mav.command_long_send(master.target_system, master.target_component,
                                  mavutil.mavlink.MAV_CMD_DO_SET_MODE, 1,
                                  mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                  LOCK_LOCK, 0, 0, 0, 0, 0)
         time.sleep(5)
         while CCSM!=12:
           pass
         print("razdvinut mehanizm") #6
         master.mav.command_long_send(master.target_system, master.target_component,
                                  mavutil.mavlink.MAV_CMD_DO_SET_MODE, 1,
                                  mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                  LOCK_RELEASE, 0, 0, 0, 0, 0)
         time.sleep(5)
         while CCSM!=12:
           pass
         print("vkluchit ir-lock") #10 0
         master.mav.command_long_send(master.target_system, master.target_component,
                              mavutil.mavlink.MAV_CMD_DO_SET_MODE, 1,
                              mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                              SERVICE,
                              IRLOCK_ON,
                              0, 0, 0, 0) 
         time.sleep(10)
         print("vykluchit ir-lock") #10 1
         master.mav.command_long_send(master.target_system, master.target_component,
                              mavutil.mavlink.MAV_CMD_DO_SET_MODE, 1,
                              mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                              SERVICE,
                              IRLOCK_OFF,
                              0, 0, 0, 0) 
         time.sleep(10)
         print("sdvinut mehanizm") #5
         master.mav.command_long_send(master.target_system, master.target_component,
                                  mavutil.mavlink.MAV_CMD_DO_SET_MODE, 1,
                                  mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                                  LOCK_LOCK, 0, 0, 0, 0, 0)
         time.sleep(5)
         while CCSM!=12:
           pass
         print("ostanovyt vse") #10 12
         master.mav.command_long_send(master.target_system, master.target_component,
                              mavutil.mavlink.MAV_CMD_DO_SET_MODE, 1,
                              mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                              SERVICE,
                              STOP,
                              0, 0, 0, 0) 
         time.sleep(5)
         while CCSM!=12:
           pass
 
   
   except BaseException as e:
     print(e)

time.sleep(3)
print('OK')
