# exp_robotics_ass1_4949035


# How to build the package?
- The package need to be inside a package with armor already installed and ready to be used.
- Clone this package into the src folder of your workspace
- catkin_make the workspace
- Go inside this package and execute the script "update_library.sh" by ./update_library.sh


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

[Component diagram.pdf](https://github.com/zecchi98/exp_robotics_ass1_4949035/files/7537091/Component.diagram.pdf)
![1008778](https://user-images.githubusercontent.com/78590047/141748541-09659ad5-2411-4518-82e7-1caee6723365.jpg)

# Where to read the all documentation of the project?
I have created a documentation in doxygen, which is stored in the "html" folder
https://zecchi98.github.io/exp_robotics_ass1_4949035/html/files.html
