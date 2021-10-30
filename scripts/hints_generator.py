#!/usr/bin/env python3
#fold all: ctrl + k + 0
#unfold all: ctrl + k + j
from genpy import message
from mylibrary.library import *
from std_srvs.srv import Trigger,TriggerResponse
from random import randint
from exp_robotics_ass1_4949035.msg import hypothesis_msg as hypothesis_msg

def initialization():
  global armor_library

  armor_library=Armor_Communication()

  rospy.init_node('hints_generator')
  rospy.wait_for_service('Initialization_service')
  rospy.set_param("Hint_ready",False)
  while not armor_library.check_if_armor_has_been_initialized():
    #print("Waiting the initialization")
    time.sleep(3)
    nul=0
  
def body():
  pub = rospy.Publisher('hint_topic', hypothesis_msg, queue_size=1)
  rate = rospy.Rate(1) # 10hz
  we_win=False
  while not rospy.is_shutdown() and not we_win:
    publish_allowed=rospy.get_param("Send_hint")
    print("waiting to send hint")
    if publish_allowed:
      print("sending hint")
      rospy.set_param("Send_hint",False)
      hypo=hypothesis_general()
      hypo.hypothesis_code="HP"+str(armor_library.number_of_hypotheses_made)

      prob_what=randint(0,10)
      if(prob_what>1):
        num_what=1
      else:
        num_what=2
      
      prob_where=randint(0,10)
      if(prob_where>1):
        num_where=1
      else:
        num_where=2
      
      prob_who=randint(0,10)
      if(prob_who>1):
        num_who=1
      else:
        num_who=2
        

      for i in range(num_where):
        hypo.places.append(armor_library.generate_random_place())

      for i in range(num_what):
        hypo.weapons.append(armor_library.generate_random_weapon())

      for i in range(num_who):
        hypo.people.append(armor_library.generate_random_person())
      
      if(len(hypo.places)>=2):
        if(hypo.places[0]==hypo.places[1]):
          hypo.places.pop(0)

      if(len(hypo.weapons)>=2):
        if(hypo.weapons[0]==hypo.weapons[1]):
          hypo.weapons.pop(0)

      if(len(hypo.people)>=2):
        if(hypo.people[0]==hypo.people[1]):
          hypo.people.pop(0)


      armor_library.make_general_hypothesis(hypo)

      rospy.set_param("Actual_hint",hypo.hypothesis_code)
      rospy.set_param("Hint_ready",True)
      #pub.publish(msg)

      we_win=rospy.get_param("WIN")
      rate.sleep()

def main():
  initialization()
  body()
  
if __name__ == '__main__':
  main()
