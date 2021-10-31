#!/usr/bin/env python3
## @package exp_robotics_ass1_4949035
#  \file Initialize_values.py
#  \brief This file is used to create a server, which call will initialized the armor parameters
#  \author Federico Zecchi
#  \version 0.1
#  \date 31/10/2021
#
#  \details
#
#  Subscribes to: <BR>
#    [None]
#
#  Publishes to: <BR>
#    [None]
#
#  Service : <BR>
#    [Initialization_service]
# 
from os import sched_setscheduler
from mylibrary.library import *
from std_srvs.srv import Trigger,TriggerResponse
def handle_request(req):
  ##
  # \brief This Function handle the request of the server by adding into the armor server: people,places,weapons
  # @param req Request to the server (Trigger srv)
  # @return TriggerResponse It will communicate that the initialization has been completed
  #With the next line we will put into the server: people, weapons and places
  initialize_people_weapons_places()

  print("The owl file has been initialized")
  
  #The initialization is complete
  rospy.set_param("Initialization_complete",True)
  return TriggerResponse(success=True,message="OK")
def initialize_people_weapons_places():
  ##
  # \brief This Function will add to the server: people,places,weapons; And will make them disjoint
    #With the next line we will put into the server: people, weapons and places
    global armor_library

    #Initialization of armor library
    armor_library=Armor_Communication()

    #loading the owl file
    armor_library.load_file()

    #We add people
    armor_library.initialize_person('JIM')
    armor_library.initialize_person('OLIVER')
    armor_library.initialize_person('JACK')
    
    #We add weapons
    armor_library.initialize_gun('ROPE')
    armor_library.initialize_gun('KNIFE')
    armor_library.initialize_gun('GUN')
    
    #We add places 
    armor_library.initialize_place('KITCHEN')
    armor_library.initialize_place('BATHROOM')
    armor_library.initialize_place('LIVINGROOM')
    
    #We make everything disjoint
    armor_library.make_PERSON_PLACE_WEAPON_as_DISJOINT()
def main():
  ##
  # \brief This Function will initialize the node, the server and will wait for a service call
  #Let's declare the node 
  rospy.init_node('Initializition_service')

  #Let's put the Initialization param False, it will put True once the initialization is complete
  rospy.set_param("Initialization_complete",False)

  #We initialize the service
  s = rospy.Service('Initialization_service', Trigger, handle_request)
  
  #We wait for the call to initialize the server
  rospy.spin() 

if __name__ == '__main__':
  main()
