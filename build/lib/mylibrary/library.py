
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
from exp_robotics_ass1_4949035.srv import *
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
class hypothesis_general():
    def __init__(self,people,places,weapons):
        super(hypothesis_general, self).__init__()
        self.people=people
        self.places=places
        self.weapons=weapons
        self.hypothesis_code="HP-1"
    def __init__(self):
        super(hypothesis_general, self).__init__()
        self.people=[]
        self.places=[]
        self.weapons=[]
        self.hypothesis_code="HP-1"
    def print_data(self):
        print(self.hypothesis_code)
        print(self.people)
        print(self.places)
        print(self.weapons)

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
        #print(places)
        #print(len(places))
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
    def make_PERSON_PLACE_WEAPON_as_DISJOINT(self):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'DISJOINT'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= ['WEAPON']
            msg = self.armor_service(req)
        except rospy.ServiceException as e:
            print(e)

        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'DISJOINT'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= ['PERSON']
            msg = self.armor_service(req)
        except rospy.ServiceException as e:
            print(e)
        
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'DISJOINT'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= ['PLACE']
            msg = self.armor_service(req)
        except rospy.ServiceException as e:
            print(e)
    def obtain_all_inconsistent_hypothesis(self):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'QUERY'
            req.primary_command_spec= 'IND'
            req.secondary_command_spec= 'CLASS'
            req.args= ['INCONSISTENT']
            msg = self.armor_service(req)
            queries=msg.armor_response.queried_objects
            cont=0
            if len(queries)<=0:
                return [],False
            A=[0]*len(queries)
            for query in queries:
                results=query[40:]
                results=results[:len(results)-1]
                A[cont]=results
                cont=cont+1
            return A,True
        except rospy.ServiceException as e:
            print(e)
            return [],False
    def check_if_the_hypothesis_corresponding_to_an_ID_is_inconsistent(self,ID_hypo):
        incons_hypo,bool=self.obtain_all_inconsistent_hypothesis()
        #print(ID_hypo)
        #print(incons_hypo)
        if(len(incons_hypo)<=0):
            return False
        else:
            for i in range(0,len(incons_hypo)):
                #print("control:"+incons_hypo[i]+" " + ID_hypo)
                if(incons_hypo[i]==ID_hypo):
                    return True
                
        return False
    def make_general_hypothesis(self,hypothesis_general):
   
        
        
        people=hypothesis_general.people
        places=hypothesis_general.places
        weapons=hypothesis_general.weapons
        hypothesis_code=hypothesis_general.hypothesis_code
        integer_hypo_code=int(hypothesis_code[2:])+1


        

        self.number_of_hypotheses_made=self.number_of_hypotheses_made+1
        if len(people)==1:
            self.__add_hypotheisis(hypothesis_code,'who',people[0])
        if len(people)==2:
            self.__add_hypotheisis(hypothesis_code,'who',people[0])
            self.__add_hypotheisis(hypothesis_code,'who',people[1])

        if len(places)==1:
            self.__add_hypotheisis(hypothesis_code,'where',places[0])
        if len(places)==2:
            self.__add_hypotheisis(hypothesis_code,'where',places[0])
            self.__add_hypotheisis(hypothesis_code,'where',places[1])
        
        if len(weapons)==1:
            self.__add_hypotheisis(hypothesis_code,'what',weapons[0])
        if len(weapons)==2:
            self.__add_hypotheisis(hypothesis_code,'what',weapons[0])
            self.__add_hypotheisis(hypothesis_code,'what',weapons[1])    
        return hypothesis_general
    def __add_hypotheisis(self,hypothesis_code,property,value):
        try:
            req=ArmorDirectiveReq()
            req.client_name= 'tutorial'
            req.reference_name= 'ontoTest'
            req.command= 'ADD'
            req.primary_command_spec= 'OBJECTPROP'
            req.secondary_command_spec= 'IND'
            req.args= [property,hypothesis_code,value]
            msg = self.armor_service(req)
            
        except rospy.ServiceException as e:
            print(e)
        self.reason()
    def from_hypo_code_to_hypothesis(self,hypothesis_code):
        h=hypothesis()
        h.person=self.from_hypothesis_code_to_who(hypothesis_code)
        
        h.place=self.from_hypothesis_code_to_where(hypothesis_code)
        
        h.weapon=self.from_hypothesis_code_to_what(hypothesis_code)
        
        h.hypothesis_code=hypothesis_code
        return h
        
    def from_hypothesis_code_to_who(self,hypothesis_code):
        return self.__struct_query_hypothesis(hypothesis_code,'who')
    def from_hypothesis_code_to_what(self,hypothesis_code):
        return self.__struct_query_hypothesis(hypothesis_code,'what')
    def from_hypothesis_code_to_where(self,hypothesis_code):
        return self.__struct_query_hypothesis(hypothesis_code,'where')
    