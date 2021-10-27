#!/usr/bin/env python3
#fold all: ctrl + k + 0
#unfold all: ctrl + k + j
from os import sched_setscheduler
from mylibrary.library import *
from std_srvs.srv import Trigger,TriggerResponse
def handle_request(req):
  print("Message received")
  initialize_people_weapons_places()
  print("The owl file has been initialized")
  return TriggerResponse(success=True,message="OK")
def initialize_people_weapons_places():
    global armor_library
    armor_library=Armor_Communication()
    armor_library.load_file()
    armor_library.initialize_person('JIM')
    armor_library.initialize_person('OLIVER')
    armor_library.initialize_person('JACK')
    #armor_library.initialize_person('JACOB')
    #armor_library.initialize_person('CHARLIE')
    #armor_library.initialize_person('THOMAS')
    
    armor_library.initialize_gun('ROPE')
    armor_library.initialize_gun('KNIFE')
    armor_library.initialize_gun('GUN')
    #armor_library.initialize_gun('WRENCH')
    #armor_library.initialize_gun('CANDLESTICK')
    #armor_library.initialize_gun('TUBE')

    armor_library.initialize_place('KITCHEN')
    armor_library.initialize_place('BATHROOM')
    armor_library.initialize_place('LIVINGROOM')
    #armor_library.initialize_place('BEDROOM')
    #armor_library.initialize_place('GARAGE')
    #armor_library.initialize_place('BASEMENT')

def main():
  armor_library=Armor_Communication()
  rospy.init_node('Initializition_service')
  s = rospy.Service('Initialization_service', Trigger, handle_request)
  rospy.spin() 

if __name__ == '__main__':
  main()
