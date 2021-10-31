#!/usr/bin/env python3
#fold all: ctrl + k + 0
#unfold all: ctrl + k + j
from mylibrary.library import *
#!/usr/bin/env python3
#fold all: ctrl + k + 0
#unfold all: ctrl + k + j

from mylibrary.library import *
from std_srvs.srv import Trigger
import time
## @package exp_robotics_ass1_4949035
#  \file state_machine.py
#  \brief This file is used as the mind of the project. It will call all the services it needs to complete the cluedo game
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
#    [Initialization_service][Oracle_service]
# 
def initializaiton():
  ##
  #\brief Initialization of the node state_machine, and of some servers parameters. It will call the Initialization service to initialize
  #all the armor parameters
  global match_is_not_over,armor_library
  rospy.init_node('State_machine')

  #Armor library initialization
  armor_library=Armor_Communication()
  
  match_is_not_over=True
  
  rospy.set_param("Send_hint",False)
  rospy.set_param("WIN",False)

  #Waiting for servers activation
  rospy.wait_for_service('Initialization_service')
  rospy.wait_for_service('Oracle_service')

  #try to call the Initialization_service to request: Initialize the armor server with standard parameters
  try:
    request = rospy.ServiceProxy('Initialization_service',Trigger)
    resp1 = request()
    
  except rospy.ServiceException as e:
    print("Service call failed: %s"%e)
def move_to_a_place(place):
  ##
  #\brief this function will simulate the robot movement to the room "place" by sleeping 1 second
  #@param place It's the name of the place you want to move to 
  #it is just a sleep 
  print('I am moving to '+place)
  time.sleep(1) 
def check_the_new_hypothesis(hypo):
  ##
  #\brief Check if the input hypothesis is a winner one by calling the oracle. Then it will modify consequently the "match_is_over" global variable
  #@param hypo is the hypothesis you need to evaluate 
  global match_is_not_over

  #Let's ask to the oracle if the hypothesis was correct
  try:
    request = rospy.ServiceProxy('Oracle_service',hypothesis_srv)
    
    resp1 = request(hypo.place,hypo.weapon,hypo.person)
    
    #if the answer is yes, then the match is over
    if resp1.success:

      match_is_not_over=False
      return True
      
    else:
      print("The hint you just received was not correct")
  except rospy.ServiceException as e:
    print("Service call failed: %s"%e)
    


  return False
def wait_for_a_complete_and_consistent_hypothesis():
  ##
  #\brief this function will wait to receive an hypothesis, then it will check if it is consistent. This function will return only if a consistent hypothesis
  #has been received. Otherwise it will continue to loop
  #@return It will return the consistent hypothesis received from the hints generator
  rate = rospy.Rate(1) # 1hz
  
  print("\nI am ready to wait for new hints\n")
  
  #Let's loop until we found a consistent hypothesis
  inconsistent_found=True
  while inconsistent_found:

    #I ask to send me an hint
    rospy.set_param("Send_hint",True)

    #Let's check if an hint has been received
    Hint_ready=rospy.get_param("Hint_ready")
    print("Waiting hint_ready")
    
    #If the hint has been received, let's check if it is consistent
    if(Hint_ready):
      print("hint ready")
      
      #Let's put Hint_ready a false, in order to be ready for the next hint
      rospy.set_param("Hint_ready",False)

      #Let's read the hint code we have received
      hypothesis_code=rospy.get_param("Actual_hint")

      #here we check if the code correspond to an inconsistent value
      inconsistent_found=armor_library.check_if_the_hypothesis_corresponding_to_an_ID_is_inconsistent(hypothesis_code)

      #In case it is not inconsistent we ask the server what is the hypothesis and we print it. Otherwise we will loop
      if(not inconsistent_found):
        hypothesis=armor_library.from_hypo_code_to_hypothesis(hypothesis_code)
        
        print("\nYou received the hint "+ hypothesis.hypothesis_code + ": "+hypothesis.person+" has killed with a " + hypothesis.weapon+" in the "+hypothesis.place+"\n")
        
        return hypothesis
      else:
        print('\nThe hint you received is inconsistent\n')
    rate.sleep()
def state_machine():
  ##
  #\brief until the match is not over, it will move to the home, wait for a consistent hypothesis, move to that localization, and then check if it is the winner
  #hypothesis.
  global match_is_not_over,armor_library

  
  #Wait the end of the game
  while match_is_not_over:
  
    #We first move to home to stark making hypotheses
    move_to_a_place("HOME")

    #wait for a complete and consistent hypothesis and return its value
    hypothesis=wait_for_a_complete_and_consistent_hypothesis()

    #move to the localization suggested in the hypothesis to check if it is correct
    move_to_a_place(hypothesis.place)

    #check if the hypothesis is the winner one
    check_the_new_hypothesis(hypothesis)

  #Kove to home and conclude the game
  move_to_a_place("HOME")
  print("The last hint was correct, you win")

  rospy.set_param("WIN",True)
def main():
  ##
  #\brief This function will call the initialization and state machine functions
  initializaiton()
  state_machine()


if __name__ == '__main__':
  main()
