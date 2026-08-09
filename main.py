"""
Conventions: docstrings and typing
"""

import os;
import time;

def get_file_timestamp(filepath: str) -> float: 
    """
    Retrieves last-modified timestamp of a file

    Parameters:
        filepath (str): a file's path name.

    Returns:
        float: timestamp formatted in seconds since the Unix Epoch
    """
    mdata: float = os.stat(filepath).st_mtime
    return mdata # Use strftime() method to convert to date and time instead of seconds since the Unix epoch

class Target:
    """
    The target class is the node in the user's buildsystem tree. 

    Instance Attributes:
        name (str): name of the target instance
        __dependents (set[Target]): set containing target objects that depend on self.
        __prereqs (set[Target]): set containing target objects that self depends on.
        __buildable (bool): boolean value that indicates whether self can be built. Initally set to true. 
    
    Class Attributes: (not sure if I need this variable yet)
        buildReady (set[Target]): set containing targets objects that are buildable.
        targets (str:*Target): set of all targets in the buildsystem
    
    Public Methods:
        get_dependents(): returns __dependents
        get_prereqs(): returns __prereqs
        get_buildable(): returns __buildable
        dependsOn(*args): adds self's dependencies to __prereqs and adds self to every arguments __dependents_t
    """

    targets = {}
    buildReady = set()

    def __init__(self, name):
        """Initializes instance of target class."""
        self.name: str = name # Temporary
        self.__dependents: set["Target"] = set()
        self.__prereqs: set["Target"] = set()
        self.__buildable: bool = True
        Target.buildReady.add(self)
        Target.targets[self.name] = self
        
        # Add two set class attributes (Static) First set stores the targets that are ready to be built.  


    def get_dependents(self) -> set["Target"]:
        """returns set of this target's dependencies"""
        return self.__dependents
    
    def get_prereqs(self) -> set["Target"]:
        """returns set of the target's that depend on this one."""
        return self.__prereqs
    
    def get_buildable(self) -> bool:
        """returns true if this target is buildable, false otherwise."""
        return self.__buildable
    
    def set_buildable(self, value):
        """Sets __buildable to value (true:false) if value is a boolean."""
        if (isinstance(value, bool)):
            self.__buildable = value

    def dependsOn(self, dependencies: set):
        """
        Adds this target's dependencies to __prereqs set and 
        adds this target to every dependencies's __dependents set.

        Parameters:
            dependencies (set): set with no duplicate elements 
        """
        for x in dependencies:
            if (x not in Target.targets):
                Target.targets[x] = Target(x)
            self.__prereqs.add(Target.targets[x])

            Target.targets[x].__dependents.add(self)
                

        # self.__prereqs.update(dependencies)
        # for x in dependencies:
        #     target_x = create_target(x, {})
        #     target_x.__dependents.add(self)

        #     if (target_x.__buildable == False):
        #         self.__buildable = False
        
        # if (self.__buildable == False):
        #     Target.buildReady.remove(self)
        

def create_target(file_name: str, dependencies: [str]) -> Target:
    ## Check if there exists a key in the dictionary that matches the str inputed. 
    if file_name in Target.targets:
        print(f"File target \"{file_name}\" already exists.")
        Target.targets[file_name].dependsOn(dependencies)    
    else:
        Target.targets[file_name] = Target(file_name)
    Target.targets[file_name].dependsOn(dependencies)
    return Target.targets[file_name]   

def build(file_name: str):
    

def main():
    """
    Create demo presentation of a buildsystem with multiple targets.
    """

    # Create targets 
    # Populate their dependents and prereqs sets.
    # Output the targets into a json file. (Directed Acyclic Graph is the three buildsystem)
    # t1 = Target("t1")
    # t2 = Target("t2")
    # t3 = Target("t3")
    # t4 = Target("t4")

    # t1.dependsOn(t2, t3)
    # t2.dependsOn(t4)

    # for x in t1.get_prereqs():
    #     print(x.name)
    # for x in t2.get_prereqs():
    #     print(x.name)
    t1 = create_target("main.o", {"main.c", "defs.h"})
    t2 = create_target("main.c", {"app.h", "main.c"})

    for x in t1.get_prereqs():
        print(x.name)
    for x in t2.get_prereqs():
        print(x.name)

if (__name__ == "__main__"):
    main()


