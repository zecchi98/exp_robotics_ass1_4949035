## @package exp_robotics_ass1_4949035
#  \file library.py
#  \brief This library is used to handle armor communication
#  \author Federico Zecchi
#  \version 0.1
#  \date 31/10/2021
#
#  \details
#  Service : <BR>
#    [armor_interface_srv]
# 
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
    ##
    #\class hypothesis
    #\brief struct to handle hypothesis made of person,place,weapon and hypothesis_code
    def __init__(self):
        ##
        #\brief init function to initialize the class
        super(hypothesis, self).__init__()
        self.person=""
        self.place=""
        self.weapon=""
        self.hypothesis_code="HP-1"
    def are_person_place_and_weapon_the_same_as_in_another_hypothesis(self,hypothesis):
        ##
        #\brief control if this hypothesis is equal to another one, by comparing person,place,weapon values.
        #@param hypothesis the variable that will be compared to the one saved in the class
        #@return True if they are equals
        if(hypothesis.person==self.person and hypothesis.place==self.place and hypothesis.weapon==self.weapon):
            return True
        else:
            return False
    def print_data(self):
        ##
        #\brief print data
        print(self.place)
        print(self.weapon)
        print(self.person)
        print(self.hypothesis_code)
class hypothesis_general():
    ##
    #\class hypothesis_general
    #\brief struct to handle hypothesis made of people,places,weapons and hypothesis_code. All this values are arrays, which not happen in the "hypothesis" class
    def __init__(self,people,places,weapons):
        ##
        #\brief init function to assign values directly
        super(hypothesis_general, self).__init__()
        self.people=people
        self.places=places
        self.weapons=weapons
        self.hypothesis_code="HP-1"
    def __init__(self):
        ##
        #\brief init value to initialize arrays 
        super(hypothesis_general, self).__init__()
        self.people=[]
        self.places=[]
        self.weapons=[]
        self.hypothesis_code="HP-1"
    def print_data(self):
        ##
        #\brief print data function
        print(self.hypothesis_code)
        print(self.people)
        print(self.places)
        print(self.weapons)

class Armor_Communication():
    ##
    #\class Armor_Communication
    def __init__(self):
        ##
        #\brief Initilize the class by declaring the client to "armor_interface_srv" service
        super(Armor_Communication, self).__init__()
        rospy.wait_for_service('armor_interface_srv')
        self.armor_service = rospy.ServiceProxy('armor_interface_srv', ArmorDirective)
        self.number_of_hypotheses_made=0
    def load_file(self):
        ##
        #\brief load the owl file
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
        ##
        #\brief Add a person to the server
        #@param person A string
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
        ##
        #\brief Obtain the list of all the people inside the system
        #@return The array requested
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
        ##
        #\brief Make the armor system reason
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
        ##
        #\brief Add a weapon to the armor server
        #@param weapon A string
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
        ##
        #\brief Obtain the list of all the weapons inside the system
        #@return The array requested
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
        ##
        #\brief Add a place to the armor server
        #@param place A string
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
        ##
        #\brief Obtain the list of all the places inside the system
        #@return The array requested
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
        ##
        #\brief Insert an hypothesis in the system
        #@param hypothesis the hypothesis that will be inserted in the system, which is of type hypothesis.
        

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
        ##
        #\brief private function to handle comunication
        
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
        ##
        #\brief Take as input the code of an hypothesis that is already been inserted in the system, and it returns its information.
        #@param hypothesis_code The code of the hypothesis you are interested in
        #@return The hypothesis details expressed as hypothesis
        x=hypothesis()
        x.weapon=self.__struct_query_hypothesis(hypothesis_code,'what')
        x.place=self.__struct_query_hypothesis(hypothesis_code,'where')
        x.person=self.__struct_query_hypothesis(hypothesis_code,'who')
        x.hypothesis_code=hypothesis_code
        return x
    def check_if_this_hypothesis_already_exist(self,hypothesis):
        ##
        #\brief check if the hypothesis you have inserted as input is already in the system
        #@param hypothesis the hypothesis you want to check
        #@return True or False
        
        for i in range(self.number_of_hypotheses_made):
            hypo_code='HP'+str(i)
            hypo=self.details_of_an_hold_hypothesis(hypo_code)
            if hypo.are_person_place_and_weapon_the_same_as_in_another_hypothesis(hypothesis):
                return True
        
        return False
    def generate_random_correct_hypo(self):
        ##
        #\brief generate a random correct hypothesis
        #@return the hypothesis you have generated
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
        ##
        #\brief generate a random place
        #@return the place
        places=self.obtain_places()
        return places[randint(0,len(places)-1)]
    def generate_random_person(self):
        ##
        #\brief generate a random person
        #@return the person you have generated
        people=self.obtain_people()
        return people[randint(0,len(people)-1)] 
    def generate_random_weapon(self):
        ##
        #\brief generate a random weapon
        #@return the weapon you have generated
        weapons=self.obtain_weapons()
        return weapons[randint(0,len(weapons)-1)]                
    def __check_if_the_hypothesis_msg_is_consistent(self,hypo_msg):
        ##
        #\brief Check if the hypothesis_MSG you have inserted as input is consistent by checking the lenght of its arrays
        #@return True or False
        if len(hypo_msg.what_array)>1 :
            return False
        if len(hypo_msg.where_array)>1 :
            return False
        if len(hypo_msg.who_array)>1 :
            return False
        return True
    def check_if_armor_has_been_initialized(self):
        ##
        #\brief Check if armor has been initialized by counting how many place have been inserted inside.
        #@return True or False
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
        ##
        #\brief it will make person place and weapon as disjoint
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
        ##
        #\brief Query obtains and returns all the inconsistent hypothesis in the system
        #@return The array of inconsistent hypothesis 
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
        ##
        #\brief Check if the hypothesis corresponding to the input ID is inconsistent
        #@param ID_hypo The ID of the hypothesis you want to check
        #@return True or False
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
        ##
        #\brief Add in the system a general hypothesis
        #@param hypothesis_general A variable of type hypothesis_general
        
        
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
        ##
        #\brief A private function to handle armor comunication
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
        ##
        #\brief From the id of an hypothesis it will look and return the hypothesis details
        #@param hypothesis_code the ID of the hypothesis you want to check
        #@return a variable of type hypothesis
        h=hypothesis()
        h.person=self.from_hypothesis_code_to_who(hypothesis_code)
        
        h.place=self.from_hypothesis_code_to_where(hypothesis_code)
        
        h.weapon=self.from_hypothesis_code_to_what(hypothesis_code)
        
        h.hypothesis_code=hypothesis_code
        return h        
    def from_hypothesis_code_to_who(self,hypothesis_code):
        ##
        #\brief From the id of an hypothesis it will look and return the corresponding person
        #@param hypothesis_code the ID of the hypothesis you want to check
        #@return a variable of type String
        return self.__struct_query_hypothesis(hypothesis_code,'who')
    def from_hypothesis_code_to_what(self,hypothesis_code):
        ##
        #\brief From the id of an hypothesis it will look and return the corresponding weapon
        #@param hypothesis_code the ID of the hypothesis you want to check
        #@return a variable of type String
        return self.__struct_query_hypothesis(hypothesis_code,'what')
    def from_hypothesis_code_to_where(self,hypothesis_code):
        ##
        #\brief From the id of an hypothesis it will look and return the corresponding place
        #@param hypothesis_code the ID of the hypothesis you want to check
        #@return a variable of type String
        return self.__struct_query_hypothesis(hypothesis_code,'where')
    