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
  rospy.set_param("Send_hint",False)
  rospy.set_param("WIN",False)
  rospy.init_node('State_machine')
  rospy.wait_for_service('Initialization_service')
  rospy.wait_for_service('Oracle_service')
  try:
    request = rospy.ServiceProxy('Initialization_service',Trigger)
    resp1 = request()
    
  except rospy.ServiceException as e:
    print("Service call failed: %s"%e)
def move_to_a_place(place):
  print('I am moving to '+place)
  #time.sleep(1)
def check_the_new_hypothesis(general_hypo):
  global match_is_not_over
  try:
    request = rospy.ServiceProxy('Oracle_service',hypothesis_srv)
    
    resp1 = request(general_hypo.place,general_hypo.weapon,general_hypo.person)
    #print(resp1)
    if resp1.success:
      match_is_not_over=False
      return True
    else:
      print("The hint you just received was not correct")
  except rospy.ServiceException as e:
    print("Service call failed: %s"%e)
    


  return False
def wait_for_a_complete_and_consistent_hypothesis():
  rate = rospy.Rate(1) # 10hz
  print("\nI am ready to wait for new hints\n")
  inconsistent_found=True
  while inconsistent_found:
    rospy.set_param("Send_hint",True)
    #hypo_msg=rospy.wait_for_message('hint_topic',hypothesis_msg)
    #h=hypothesis_general(hypo_msg.who_array,hypo_msg.where_array,hypo_msg.what_array)
    #h.hypothesis_code="HP"+str(armor_library.number_of_hypotheses_made)
    Hint_ready=rospy.get_param("Hint_ready")
    print("Waiting hint_ready")
    if(Hint_ready):
      print("hint ready")
      rospy.set_param("Hint_ready",False)
      hypothesis_code=rospy.get_param("Actual_hint")

      inconsistent_found=armor_library.check_if_the_hypothesis_corresponding_to_an_ID_is_inconsistent(hypothesis_code)

      if(not inconsistent_found):
        hypothesis=armor_library.from_hypo_code_to_hypothesis(hypothesis_code)
        
        print("\nYou received the hint "+ hypothesis.hypothesis_code + ": "+hypothesis.person+" has killed with a " + hypothesis.weapon+" in the "+hypothesis.place+"\n")
        
        return hypothesis
      else:
        print('\nThe hint you received is inconsistent\n')
    rate.sleep()
def state_machine():
  global match_is_not_over,armor_library

  move_to_a_place("HOME")
  while match_is_not_over:
    hypothesis=wait_for_a_complete_and_consistent_hypothesis()
    move_to_a_place(hypothesis.place)
    check_the_new_hypothesis(hypothesis)
  move_to_a_place("HOME")
  print("The last hint was correct, you win")

  rospy.set_param("WIN",True)
def main():
  
  initializaiton()
  state_machine()


if __name__ == '__main__':
  main()
