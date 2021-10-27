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
def check_the_new_hypothesis(general_hypo):
  global match_is_not_over
  try:
    request = rospy.ServiceProxy('Oracle_service',hypothesis_srv)
    
    resp1 = request(general_hypo.places[0],general_hypo.weapons[0],general_hypo.people[0])
    print(resp1)
    if resp1.success:
      match_is_not_over=False
      return True
  except rospy.ServiceException as e:
    print("Service call failed: %s"%e)


  return False
def wait_for_a_complete_and_consistent_hypothesis():
  inconsistent_found=True
  while inconsistent_found:
    #time.sleep(2)
    hypo_msg=rospy.wait_for_message('hint_topic',hypothesis_msg)
    h=hypothesis_general(hypo_msg.who_array,hypo_msg.where_array,hypo_msg.what_array)
    h.hypothesis_code="HP"+str(armor_library.number_of_hypotheses_made)
    #h.print_data()

    armor_library.make_general_hypothesis(h)
    inconsistent_found=armor_library.check_if_the_hypothesis_corresponding_to_an_ID_is_inconsistent(h.hypothesis_code)
    #consistent_found=armor_library.check_if_the_hypothesis_msg_is_consistent(hypo_msg)
    if(not inconsistent_found):
      print('The hint is complete and consistent')
      print("Hint: "+h.people[0]+" has killed with a " + h.weapons[0]+" in the "+h.places[0])
      return h
    else:
      print('The hint is inconsistent')
def state_machine():
  global match_is_not_over
  while match_is_not_over:
    move_to_a_place()
    hypothesis=wait_for_a_complete_and_consistent_hypothesis()
    check_the_new_hypothesis(hypothesis)
def main():
  
  initializaiton()
  state_machine()


if __name__ == '__main__':
  main()
