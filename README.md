# exp_robotics_ass1_4949035


# How to build the package?
- The package need to be inside a package with armor already installed and ready to be used.
- Clone this package into the src folder of the ros_ws
- catkin_make the workspace
- Go inside this package and execute the script "update_library.sh" by ./update_library.sh

# Is the owl file in the right position?
The package has been mainly built to work in the docker container workspace. This package need to be installed in the ros_ws workspace. Otherwise it will not work.
If you are running this package outside of that folder you will need to change manually the code. In particular, go to "my_library" folder and to the library.ph file.
Then go to the Armor_Communication class and to the load_file method.
Find the line: "req.args= ['/root/ros_ws/src/exp_robotics_ass1_4949035/cluedo_ontology.owl', 'http://www.emarolab.it/cluedo-ontology', 'true', 'PELLET', 'true']"
Modify the first argument of this square brackets, by inserting your path to the cluedo file.
After saving this modification you will have to buil the library.
In the main folder execute the script "update_library.sh" by ./update_library.sh

# How to run the code?
- First tab: roscore
- Second tab: rosrun armor execute it.emarolab.armor.ARMORMainService
- Third tab: roslaunch exp_robotics_ass1_4949035 launcher.launch


# In which language is the project written?
Python


# How is the Cluedo match structured?
A specific person has killed with a particular weapon in a particular place. The system will have to understand what has happened through the hints that it will receive.


# How is the all project structured?
This project is composed of one library(mylibrary) and four nodes. All the nodes use similar codes and this is the reason I decided to create a personal library. Thanks to many variables stored in the paramter server, the system is able to handle comunication and concurrency between nodes.


# What about the library
I mainly used the library to interact with armor, it contains three classes. Two classes are the C# equivalent for structure, they are used to store hypothesis. In particular the first one is used to save correct hypothesis, the second one instead is made of inconsistent hypothesis.
The third class instead is used to comunicate with armor, it contains the client to call it and all the methods to save lines of codes. 
Here below there are some example of this methods:
- Method to make hypothesis and insert them into the armor system
- Method to obtain all the person inserted in the system
- Method to obtain all the inconsistent hypotheses in the system
- Method to check if an hypothesis is inconsistent
- .....


# Initialize_values node
This node is used to initialize the armor server. In particular it will load the owl file and will insert in the system all the people places and weapons needed. In order to make it initialize everything, you will need to call its server which is called "Initialization service".


# Oracle node
This node is used to understand if the last hypothesis generated is the winner one. In particular it creates a server called "Oracle_service" and takes as input an hypothesis that will check with the winner one. The first time this server its called it also generate the winner hypothesis


# Hints_generator node
This node is used to create hypotheses, it will insert them in the armor system and then will comunicate the ID to the state machine thanks to the parameter server.


# State_machine node
This node is core part of the project, it will call the initialization service and will wait for new hypothesis.
It will check if the hypothesis received is consistent and in case of affertive response it will go to the particular location to check if it is also the winner one.
The move_to_location method for the moment it's just a busy wait.

# Component diagram
In the diagram below all the nodes already explained will be connected
![component diagram](https://user-images.githubusercontent.com/78590047/141748734-6a5c9d89-94f5-47c1-9927-444df0286691.PNG)

# State diagram
![state diagram](https://user-images.githubusercontent.com/78590047/141750068-393cd9a9-690a-4091-93df-04d33447b49c.png)

# Temporal diagram
As it is shown in the diagram, most of the nodes wait for the initialization of the "initializatioon_values" node. Then most of the code is directed and organized thanks to the "state_machine" node. 
![temporal diagram](https://user-images.githubusercontent.com/78590047/141755697-11457d88-75d0-43ee-bf96-9c8c8c59851f.png)

# Screenshot of the working algorithm!
[Screenshot from 2021-11-15 10-45-53](https://user-images.githubusercontent.com/78590047/141759875-264b3927-3e67-4c6f-a2be-1d3ac6e3674f.png)


# Where to read the all documentation of the project?
I have created a documentation in doxygen, which is stored in the "html" folder. The majority of the files documentation can be also seen in the link below. Not all the links works, so I suggest to check also the "html" folder
https://zecchi98.github.io/exp_robotics_ass1_4949035/html/files.html

# Author & Contacts
Author: Federico Zecchi
E-mail: zecchi.federico@hotmail.it  s4949035@studenti.unige.it
