"""
Conventions: docstrings and typing
"""

import os;
import time;

def find_filepath(name: str) -> str:
    """
    Finds the file in the project and returns the path. 
    If corresponding file does not exist, returns null.

    Parameters:
        name (str): name of file
    """
    ## make sure name is a string and not empty. 
    ## 

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
    
    Class Attributes: 
        targets (str:*Target): set of all targets in the buildsystem
    
    Public Methods:
        get_dependents(): returns __dependents
        get_prereqs(): returns __prereqs
        dependsOn(*args): adds self's dependencies to __prereqs and adds self to every arguments __dependents_t
    """
    targets: dict[str, "Target"] = {}

    def __init__(self, name):
        """Initializes instance of target class."""
        self.name: str = name # Temporary
        self.__dependents: set["Target"] = set()
        self.__prereqs: set["Target"] = set()
        Target.targets[self.name] = self
        

    def get_dependents(self) -> set["Target"]:
        """returns set of this target's dependencies"""
        return self.__dependents
    
    def get_prereqs(self) -> set["Target"]:
        """returns set of the target's that depend on this one."""
        return self.__prereqs

    def dependsOn(self, dependencies: set[str]):
        """
        Adds dependencies to self's __prereqs
        Adds self to every dependencies's __dependents set.

        Parameters:
            dependencies (set): set of strings 
        """
        for x in dependencies:
            if (x not in Target.targets): ## If target doesn't already exist, create instance.
                Target.targets[x] = Target(x)
            
            self.__prereqs.add(Target.targets[x])
            Target.targets[x].__dependents.add(self)
        

def create_target(file_name: str, dependencies: set[str]) -> Target:
    """
    Creates a target instance and initializes its prerequisistes 
    and dependents. If target instance corresponding to the same
    name exists already, update the target's prereqs and dependents 
    according to input. 
    
    Parameters: 
        file_name (str): name of the file
        dependencies (set): set of strings. 
    """
    if file_name not in Target.targets:
        Target.targets[file_name] = Target(file_name)
    else:
        print(f"File target \"{file_name}\" already exists.")

    Target.targets[file_name].dependsOn(dependencies)

    return Target.targets[file_name]   

def build(file_name: str, visiting=None, built=None):
    
    if visiting is None:
        visiting = set()
    if built is None:
        built = set()
    
    build_ready: bool = True ## temp
    
    target: Target = Target.targets[file_name]
    
    if target.name in visiting:
        raise RecursionError("There is a forbidden cycle in your buildsystem.") ## Not entirely sure how to deal with cycles yet and if this is the most efficient way or not.
    if target.name in built:
        return

    visiting.add(target.name)
    
    for x in target.get_prereqs():
        build(x.name, visiting, built)
        
        "If any of x have timestamp that is newer than current, current is flagged as not build_ready"


    print(f"building {target.name}") ## if current is not build_ready, then build"
    visiting.remove(target.name)
    built.add(target.name)
    

    


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
    t2 = create_target("main.c", {"app.h"})
    # t3 = create_target("app.h", {"main.o"})

    # for x in t1.get_prereqs():
    #     print(x.name)
    # for x in t2.get_prereqs():
    #     print(x.name)

    
    build("main.o")
    


if (__name__ == "__main__"):
    main()


