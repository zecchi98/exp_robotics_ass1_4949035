#!/usr/bin/env python3
## @package exp_robotics_ass1_4949035
#  \file hints_generator.py
#  \brief This file is used to generate random hint and communicate them to the state machine node
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
#    [Initialization_service]
# 
from genpy import message
from mylibrary.library import *
from std_srvs.srv import Trigger,TriggerResponse
from random import randint
from exp_robotics_ass1_4949035.msg import hypothesis_msg as hypothesis_msg

def initialization():
  ##
  #\brief This function will initialize the node and wait for the initilization of the armor server by another node
  global armor_library

  #Declaration of the library
  armor_library=Armor_Communication()

  #Initialization of the node
  rospy.init_node('hints_generator')

  #No hint is ready at the moment, so we communicate it
  rospy.set_param("Hint_ready",False)

  #We wait the initialization of armor parameters to be completed
  rospy.wait_for_service('Initialization_service')
  Initialization_complete=rospy.get_param("Initialization_complete")
  while not Initialization_complete:
    #print(str(Initialization_complete))
    time.sleep(1)
    Initialization_complete=rospy.get_param("Initialization_complete")
def body():
  ##
  # \brief This function will generate a random hypothesis which can be consistent or not. Then it will communicate it to the state machine 
  # thanks to the ros parameter server
  rate = rospy.Rate(0.5) # 10hz
  
  #Win bool to exit the node
  we_win=False

  while not rospy.is_shutdown() and not we_win:

    #We are allowed to start sending hint only if this variable is True
    publish_allowed=rospy.get_param("Send_hint")
    print("waiting to send hint")

    if publish_allowed:
      print("sending hint")

      #We set it to False, in order to not sending hint while the system is processing them
      rospy.set_param("Send_hint",False)
      publish_allowed=False
      
      #We declare a general hypo with its correct new id_code
      hypo=hypothesis_general()
      hypo.hypothesis_code="HP"+str(armor_library.number_of_hypotheses_made)

      #In the next lines for each of "what","where" and "who": we generate a number between 0 and 10, if it is grater than 1 then
      # we will have just one value of that class. Otherwise we will have two values and the hint will be inconsistent. 
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
        
      #Due to the result of the precedent algorithm we create the hypothesis
      for i in range(num_where):
        hypo.places.append(armor_library.generate_random_place())

      for i in range(num_what):
        hypo.weapons.append(armor_library.generate_random_weapon())

      for i in range(num_who):
        hypo.people.append(armor_library.generate_random_person())
      
      #In the next lines we check if there are two equel values, in that case we remove one of them
      if(len(hypo.places)>=2):
        if(hypo.places[0]==hypo.places[1]):
          hypo.places.pop(0)

      if(len(hypo.weapons)>=2):
        if(hypo.weapons[0]==hypo.weapons[1]):
          hypo.weapons.pop(0)

      if(len(hypo.people)>=2):
        if(hypo.people[0]==hypo.people[1]):
          hypo.people.pop(0)

      #We insert the hypo in the armor system
      armor_library.make_general_hypothesis(hypo)

      #We communicate the hint id we have already built
      rospy.set_param("Actual_hint",hypo.hypothesis_code)

      #We communicate that a new hint is ready
      rospy.set_param("Hint_ready",True)

    #Here we check if the have won
    we_win=rospy.get_param("WIN")
    rate.sleep()

def main():
  ##
  # \brief This Function will call the initialization and body functions
  initialization()
  body()
  
if __name__ == '__main__':
  main()
