#!/usr/bin/env python3
#fold all: ctrl + k + 0
#unfold all: ctrl + k + j
from mylibrary.library import *
from std_srvs.srv import Trigger,TriggerResponse
def handle_request(req):
  initialize_people_weapons_places()
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
    print(armor_library.obtain_people())
    
    armor_library.initialize_gun('ROPE')
    armor_library.initialize_gun('KNIFE')
    armor_library.initialize_gun('GUN')
    #armor_library.initialize_gun('WRENCH')
    #armor_library.initialize_gun('CANDLESTICK')
    #armor_library.initialize_gun('TUBE')
    print(armor_library.obtain_weapons())

    armor_library.initialize_place('KITCHEN')
    armor_library.initialize_place('BATHROOM')
    armor_library.initialize_place('LIVINGROOM')
    #armor_library.initialize_place('BEDROOM')
    #armor_library.initialize_place('GARAGE')
    #armor_library.initialize_place('BASEMENT')
    print(armor_library.obtain_places())
def define_all_initial_functions():
    
    initialize_people_weapons_places()
    
   
    h0=hypothesis()
    h0.place='KITCHEN'
    h0.weapon='ROPE'
    h0.person='JIM'
    h0.hypothesis_code='HP0'

    armor_library.make_hypothesis(h0)


    h1=hypothesis()
    h1.place='KITCHEN'
    h1.weapon='KNIFE'
    h1.person='JIM'
    h1.hypothesis_code='HP1'
    
    armor_library.make_hypothesis(h1)

    print(armor_library.check_if_this_hypothesis_already_exist(h1))
def main():
  #define_all_initial_functions()
  
  rospy.init_node('Initializition_service')
  s = rospy.Service('Initialization_service', Trigger, handle_request)
  rospy.spin() 

if __name__ == '__main__':
  main()
