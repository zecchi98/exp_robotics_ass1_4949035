#!/usr/bin/env python3
## @package exp_robotics_ass1_4949035
#  \file oracle.py
#  \brief This file is used to create a server; Its call will check if the hypothesis in consideration is the winner one; The first time will also create the winner
#  hypothesis
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
#    [Oracle_service] [Initialization_service]
# 
from genpy import message
from mylibrary.library import *
from std_srvs.srv import Trigger,TriggerResponse
from random import randint


def create_the_winner_hypothesis():
  ##
  # \brief This Function will create the winner hypothesis
  global winner_hypothesis,winner_hypo_created_bool

  #We change the winner_bool value
  winner_hypo_created_bool=True
  
  #We generate a random hypothesis and we save it as the winner one
  winner_hypothesis=armor_library.generate_random_correct_hypo()
  
  return winner_hypothesis
def handle_request(req):
  ##
  # \brief This Function will handle the request of the server. It will create the winner hypothesis if it hasn't been done yet and will check if the 
  # hypothesis inside the req message is the same as the winner one.
  # @param req Request to the server (hypothesis_srv srv)
  # @return hypothesis_srvResponse It will communicate if the game has been completed
  #If the winner hypothesis has not been created, we create it
  if not winner_hypo_created_bool: 
    create_the_winner_hypothesis()

  #We save into the struct the request message
  hypo=hypothesis()
  hypo.person=req.who
  hypo.place=req.where
  hypo.weapon=req.what
  hypo.hypothesis_code=""

  #We check if the hypothesis "hypo" is the same as "winner_hypothesis" a part for the id_code. In case "True" we return success=True
  if hypo.are_person_place_and_weapon_the_same_as_in_another_hypothesis(winner_hypothesis):
    success=True
  else:
    success=False
    message='YOU DO NOT WIN'
  return hypothesis_srvResponse(success)
def initialization_oracle():
  ##
  # \brief This Function will initialize the node, and will wait the armor server to be initilized by the "Initialization" server
  global armor_library,winner_hypo_created_bool

  #Declaration of the node
  rospy.init_node('Oracle_service')

  #We monitorized if the winner hypo has been already created
  winner_hypo_created_bool=False

  #Declaration of the library
  armor_library=Armor_Communication()

  #Service Oracle initialized
  s = rospy.Service('Oracle_service', hypothesis_srv, handle_request)
  
  #Let's wait fo the initialization of the variables to be completed
  rospy.wait_for_service('Initialization_service')
  Initialization_complete=rospy.get_param("Initialization_complete")
  while not Initialization_complete:
    time.sleep(1)
    Initialization_complete=rospy.get_param("Initialization_complete")
def main():
  ##
  # \brief This Function will call "initilization oracle" and then will wait for a service call
  initialization_oracle()
  rospy.spin()
if __name__ == '__main__':
  main()
