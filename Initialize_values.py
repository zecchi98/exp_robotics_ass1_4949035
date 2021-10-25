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

class hypothesis():
    name:str
    room:str
    weapon:str
    hypothesis_code:str

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
    def initialize_person(self,name):
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
    def obtain_people(self):
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
            cont=0
            A=[0]*6
            for query in queries:
                results=query[40:]
                results=results[:len(results)-1]
                #print(results)
                A[cont]=results
                cont=cont+1
            return A
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
    def initialize_gun(self,weapon):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'ADD'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= [weapon,'WEAPON']
            msg = self.armor_service(req)
            self.reason()
        except rospy.ServiceException as e:
            print(e)   
    def obtain_weapons(self):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'QUERY'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= ['WEAPON']
            msg = self.armor_service(req)
            queries=msg.armor_response.queried_objects
            cont=0
            A=[0]*6
            for query in queries:
                results=query[40:]
                results=results[:len(results)-1]
                #print(results)
                A[cont]=results
                cont=cont+1
            return A
        except rospy.ServiceException as e:
            print(e)
    def initialize_room(self,room):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'ADD'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= [room,'PLACE']
            msg = self.armor_service(req)
            self.reason()
        except rospy.ServiceException as e:
            print(e)   
    def obtain_rooms(self):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'QUERY'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= ['PLACE']
            msg = self.armor_service(req)
            queries=msg.armor_response.queried_objects
            cont=0
            A=[0]*6
            for query in queries:
                results=query[40:]
                results=results[:len(results)-1]
                #print(results)
                A[cont]=results
                cont=cont+1
            return A
        except rospy.ServiceException as e:
            print(e)
    def make_hypothesis(self,hypothesis):
        name=hypothesis.name
        room=hypothesis.room
        weapon=hypothesis.weapon
        hypothesis_code=hypothesis.hypothesis_code
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'ADD'
            req.primary_command_spec= 'OBJECTPROP'
            req.secondary_command_spec= 'IND'
            req.args= ['who',hypothesis_code,name]
            msg = self.armor_service(req)
            
        except rospy.ServiceException as e:
            print(e)

        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'ADD'
            req.primary_command_spec= 'OBJECTPROP'
            req.secondary_command_spec= 'IND'
            req.args= ['what',hypothesis_code,weapon]
            msg = self.armor_service(req)
            
        except rospy.ServiceException as e:
            print(e)

        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'ADD'
            req.primary_command_spec= 'OBJECTPROP'
            req.secondary_command_spec= 'IND'
            req.args= ['where',hypothesis_code,room]
            msg = self.armor_service(req)
            
        except rospy.ServiceException as e:
            print(e)

        self.reason()
    def __struct_query_hypothesis(self,hypothesis_code,param):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'QUERY'
            req.primary_command_spec= 'OBJECTPROP'
            req.secondary_command_spec= 'IND'
            req.args= [param,hypothesis_code]
            msg = self.armor_service(req)
            query=msg.armor_response.queried_objects[0]
            cont=0
            A=[0]*6
            results=query[40:]
            results=results[:len(results)-1]
            return results
        except rospy.ServiceException as e:
            print(e)
    def details_of_an_hold_hypothesis(self,hypothesis_code):
        what=self.__struct_query_hypothesis(hypothesis_code,'what')
        where=self.__struct_query_hypothesis(hypothesis_code,'where')
        who=self.__struct_query_hypothesis(hypothesis_code,'who')
        return what,where,who
    def check_if_this_hypothesis_already_exits(self,hypothesis):
        nuòl=0
def define_all_initial_functions():
    global armor_library
    armor_library=Armor_Communication()
    armor_library.load_file()
    armor_library.initialize_person('JIM')
    armor_library.initialize_person('OLIVER')
    armor_library.initialize_person('JACK')
    armor_library.initialize_person('JACOB')
    armor_library.initialize_person('CHARLIE')
    armor_library.initialize_person('THOMAS')
    #print(armor_library.obtain_people())
    
    armor_library.initialize_gun('ROPE')
    armor_library.initialize_gun('KNIFE')
    armor_library.initialize_gun('GUN')
    armor_library.initialize_gun('WRENCH')
    armor_library.initialize_gun('CANDLESTICK')
    armor_library.initialize_gun('TUBE')
    #print(armor_library.obtain_weapons())

    armor_library.initialize_room('KITCHEN')
    armor_library.initialize_room('BATHROOM')
    armor_library.initialize_room('LIVINGROOM')
    armor_library.initialize_room('BEDROOM')
    armor_library.initialize_room('GARAGE')
    armor_library.initialize_room('BASEMENT')
    #print(armor_library.obtain_rooms())
   
    h0=hypothesis()
    h0.room='KITCHEN'
    h0.weapon='ROPE'
    h0.name='JIM'
    h0.hypothesis_code='HP0'
    armor_library.make_hypothesis(h0)
    print(armor_library.details_of_an_hold_hypothesis('HP0'))
    
def prova():
  nul=0
def main():
  define_all_initial_functions()
  prova()    

if __name__ == '__main__':
  main()
