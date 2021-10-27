#!/usr/bin/env python3
#fold all: ctrl + k + 0
#unfold all: ctrl + k + j
from genpy import message
from mylibrary.library import *
from std_srvs.srv import Trigger,TriggerResponse
from random import randint

def create_and_check_the_hypothesis():
  
  hypo=armor_library.generate_random_correct_hypo()
  
  if not armor_library.check_if_this_hypothesis_already_exist(hypo):
    armor_library.make_hypothesis(hypo)
  
  return hypo
def create_the_winner_hypothesis():
  global winner_hypothesis,winner_hypo_created_bool
  winner_hypo_created_bool=True
  print("Winner Hypo:")
  winner_hypothesis=armor_library.generate_random_correct_hypo()
  winner_hypothesis.print_data()
  return winner_hypothesis
def handle_request(req):

  if not winner_hypo_created_bool: 
    create_the_winner_hypothesis()

  hypo=hypothesis()
  hypo.person=req.who
  hypo.place=req.where
  hypo.weapon=req.what
  hypo.hypothesis_code=""
  hypo.print_data()
  if hypo.are_person_place_and_weapon_the_same_as_in_another_hypothesis(winner_hypothesis):
    success=True
    message='YOU WIN'
    print(message)
  else:
    success=False
    message='YOU DO NOT WIN'
  return hypothesis_srvResponse(success)
def initialization_oracle():
  global armor_library,winner_hypo_created_bool

  winner_hypo_created_bool=False

  armor_library=Armor_Communication()

  rospy.init_node('Oracle_service')

  print('Waiting for initialization_service')
  rospy.wait_for_service('Initialization_service')
  s = rospy.Service('Oracle_service', hypothesis_srv, handle_request)

def main():
  initialization_oracle()
  
  rospy.spin()
if __name__ == '__main__':
  main()
