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
  
  while not armor_library.check_if_armor_has_been_initialized():
    #print("Waiting the initialization")
    time.sleep(3)
    nul=0
  
def body():
  pub = rospy.Publisher('hint_topic', hypothesis_msg, queue_size=1)
  rate = rospy.Rate(1) # 10hz
  
  while not rospy.is_shutdown():
    publish_allowed=rospy.get_param("Send_hint")
    time.sleep(0.5)
    if publish_allowed:
      msg=hypothesis_msg()
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
        msg.where_array.append(armor_library.generate_random_place())

      for i in range(num_what):
        msg.what_array.append(armor_library.generate_random_weapon())

      for i in range(num_who):
        msg.who_array.append(armor_library.generate_random_person())
      
      if(len(msg.where_array)>=2):
        if(msg.where_array[0]==msg.where_array[1]):
          msg.where_array.pop(0)

      if(len(msg.what_array)>=2):
        if(msg.what_array[0]==msg.what_array[1]):
          msg.what_array.pop(0)

      if(len(msg.who_array)>=2):
        if(msg.who_array[0]==msg.who_array[1]):
          msg.who_array.pop(0)

      
      pub.publish(msg)
      rate.sleep()

def main():
  initialization()
  body()
  
if __name__ == '__main__':
  main()
