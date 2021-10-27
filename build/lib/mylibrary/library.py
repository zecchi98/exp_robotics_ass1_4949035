
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
from random import randint
from exp_robotics_ass1_4949035.msg import hypothesis_msg as hypothesis_msg
class hypothesis():
    person:str
    place:str
    weapon:str
    hypothesis_code:str
    def are_person_place_and_weapon_the_same_as_in_another_hypothesis(self,hypothesis):
        if(hypothesis.person==self.person and hypothesis.place==self.place and hypothesis.weapon==self.weapon):
            return True
        else:
            return False
    def print_data(self):
        print(self.place)
        print(self.weapon)
        print(self.person)
        print(self.hypothesis_code)

class Armor_Communication():
    def __init__(self):
        super(Armor_Communication, self).__init__()
        rospy.wait_for_service('armor_interface_srv')
        self.armor_service = rospy.ServiceProxy('armor_interface_srv', ArmorDirective)
        self.number_of_hypotheses_made=0
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
    def initialize_person(self,person):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'ADD'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= [person,'PERSON']
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
            A=[0]*len(queries)
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
            A=[0]*len(queries)
            for query in queries:
                results=query[40:]
                results=results[:len(results)-1]
                #print(results)
                A[cont]=results
                cont=cont+1
            return A
        except rospy.ServiceException as e:
            print(e)
    def initialize_place(self,place):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'ADD'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= [place,'PLACE']
            msg = self.armor_service(req)
            self.reason()
        except rospy.ServiceException as e:
            print(e)   
    def obtain_places(self):
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
            A=[0]*len(queries)
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
        

        person=hypothesis.person
        place=hypothesis.place
        weapon=hypothesis.weapon
        hypothesis_code=hypothesis.hypothesis_code
        integer_hypo_code=int(hypothesis_code[2:])+1

        if(self.check_if_this_hypothesis_already_exist(hypothesis)):
            print('The hypothesis already exist')
            return False

        if(integer_hypo_code<=self.number_of_hypotheses_made):
            print('Your hypo code has been already used')
            return False
        self.number_of_hypotheses_made=self.number_of_hypotheses_made+1
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'ADD'
            req.primary_command_spec= 'OBJECTPROP'
            req.secondary_command_spec= 'IND'
            req.args= ['who',hypothesis_code,person]
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
            req.args= ['where',hypothesis_code,place]
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
            results=query[40:]
            results=results[:len(results)-1]
            return results
        except rospy.ServiceException as e:
            print(e)
    def details_of_an_hold_hypothesis(self,hypothesis_code):
        x=hypothesis()
        x.weapon=self.__struct_query_hypothesis(hypothesis_code,'what')
        x.place=self.__struct_query_hypothesis(hypothesis_code,'where')
        x.person=self.__struct_query_hypothesis(hypothesis_code,'who')
        x.hypothesis_code=hypothesis_code
        return x
    def check_if_this_hypothesis_already_exist(self,hypothesis):
        
        for i in range(self.number_of_hypotheses_made):
            hypo_code='HP'+str(i)
            hypo=self.details_of_an_hold_hypothesis(hypo_code)
            if hypo.are_person_place_and_weapon_the_same_as_in_another_hypothesis(hypothesis):
                return True
        
        return False
    def generate_random_correct_hypo(self):

        people=self.obtain_people()
        weapons=self.obtain_weapons()
        places=self.obtain_places()
        print(places)
        print(len(places))
        hypo=hypothesis()
        hypo.person=people[randint(0,len(people)-1)]
        hypo.weapon=weapons[randint(0,len(weapons)-1)]
        hypo.place=places[randint(0,len(places)-1)]
        hypo.hypothesis_code='HP'+str(self.number_of_hypotheses_made)
        
        return hypo
    def generate_random_place(self):
        places=self.obtain_places()
        return places[randint(0,len(places)-1)]
    def generate_random_person(self):
        people=self.obtain_people()
        return people[randint(0,len(people)-1)] 
    def generate_random_weapon(self):
        weapons=self.obtain_weapons()
        return weapons[randint(0,len(weapons)-1)]                
    def check_if_the_hypothesis_msg_is_consistent(self,hypo_msg):
        if len(hypo_msg.what_array)>1 :
            return False
        if len(hypo_msg.where_array)>1 :
            return False
        if len(hypo_msg.who_array)>1 :
            return False
        return True
    def check_if_armor_has_been_initialized(self):
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
            if(len(queries))>0:
                return True
            else:
                return False
        except rospy.ServiceException as e:
            print(e)
            return False






