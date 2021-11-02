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

# How is the all project structured?
This project is composed of one library(mylibrary) and four nodes. All the nodes use similar codes and this is the reason I decided to create a personal library. 

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

# Oracle node

# State_machine node

# Hints_generator node
