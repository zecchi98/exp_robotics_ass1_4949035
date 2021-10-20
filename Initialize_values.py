#!/usr/bin/env python
#fold all: ctrl + k + 0
#unfold all: ctrl + k + j
import copy
import math
import sys
import time
from logging import setLoggerClass
from math import cos, pi, sin
from os import access
from re import X

import geometry_msgs.msg
import numpy as np
import rospy
from std_msgs.msg import String
from armor_msgs.msg import * 
from armor_msgs.srv import * 


class Armor_Communication():
    def __init__(self):
        super(Armor_Communication, self).__init__()
        rospy.wait_for_service('armor_interface_srv')
        self.armor_service = rospy.ServiceProxy('armor_interface_srv', ArmorDirective)
    def load_file(self):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'LOAD'
            req.primary_command_spec= 'FILE'
            req.secondary_command_spec= ''
            req.args= ['/root/ros_ws/src/exp_robotics_ass1_4949035/cluedo_ontology.owl', 'http://www.emarolab.it/cluedo-ontology', 'true', 'PELLET', 'true']
            msg = self.armor_service(req)
        except rospy.ServiceException as e:
            print(e)
    def add_person(self,name):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'ADD'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= [name,'PERSON']
            msg = self.armor_service(req)
            self.reason()
        except rospy.ServiceException as e:
            print(e)
    def print_people(self):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'QUERY'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= ['PERSON']
            msg = self.armor_service(req)
            queries=msg.armor_response.queried_objects
            for query in queries:
                results=query[40:]
                results=results[:len(results)-1]
                print(results)
        except rospy.ServiceException as e:
            print(e)
    def reason(self):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'REASON'
            req.primary_command_spec= ''
            req.secondary_command_spec= ''
            req.args= []
            msg = self.armor_service(req)
        except rospy.ServiceException as e:
            print(e)



def define_all_initial_functions():
    global armor_library
    armor_library=Armor_Communication()
    armor_library.load_file()
    armor_library.add_person('JIM')
    armor_library.add_person('FILO')
    armor_library.print_people()
   


def prova():
  nul=0
def main():
  define_all_initial_functions()
  prova()    
#   try:
#     while (not rospy.core.is_shutdown()):
#         rospy.rostime.wallsleep(0.5)
#   except rospy.ROSInterruptException:
#     return
#   except KeyboardInterrupt:
#     return
if __name__ == '__main__':
  main()
