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
def initializaiton():
  global match_is_not_over,armor_library
  armor_library=Armor_Communication()
  match_is_not_over=True
  rospy.init_node('State_machine')
  rospy.wait_for_service('Initialization_service')
  rospy.wait_for_service('Oracle_service')
  
  try:
    request = rospy.ServiceProxy('Initialization_service',Trigger)
    resp1 = request()
    
  except rospy.ServiceException as e:
    print("Service call failed: %s"%e)
  

def move_to_a_place():
  print('I am moving to the next place')
  #time.sleep(2)
  print('I am ready to make hypotheses')
  #stampa il nome della stanza
def create_and_check_the_new_hypothesis():
  global match_is_not_over
  try:
    request = rospy.ServiceProxy('Oracle_service',Trigger)
    resp1 = request()
    print(resp1)
    if resp1.message=="YOU WIN":
      match_is_not_over=False
      return True
  except rospy.ServiceException as e:
    print("Service call failed: %s"%e)


  return False
def wait_for_a_complete_and_consistent_hypothesis():
  consistent_found=False
  while not consistent_found:
    hypo_msg=rospy.wait_for_message('hint_topic',hypothesis_msg)
    consistent_found=armor_library.check_if_the_hypothesis_msg_is_consistent(hypo_msg)
    if(consistent_found):
      print('The hint is complete and consistent')
    else:
      print('The hint is inconsistent')
def state_machine():
  global match_is_not_over
  while match_is_not_over:
    move_to_a_place()
    wait_for_a_complete_and_consistent_hypothesis()
def main():
  initializaiton()
  state_machine()


if __name__ == '__main__':
  main()
