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
    
    Class Attributes:
        buildReady (set[Target]): set containing targets objects that are buildable. 
    
    Public Methods:
        get_dependents(): returns __dependents_t
        get_prerequisites(): returns __prerequisites_t
        get_buildable(): returns __buildable
        dependsOn(*args): adds self's dependencies to __prereqs and adds self to every arguments __dependents_t
    """

    buildReady = set()

    def __init__(self, name):
        """Initializes instance of target class."""
        self.name: str = name # Temporary
        self.__dependents: set["Target"] = set()
        self.__prereqs: set["Target"] = set()
        self.__buildable: bool = True
        Target.buildReady.add(self)
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
        if (isinstance(value, bool)):
            self.__buildable = value

    def dependsOn(self, *args):
        """
        Adds this targets dependencies to __prereqs set and 
        adds this target to every arguments __dependents set.

        Parameters:
            *args (tuple): tuple of target instance of unknown size. 
        """
        self.__prereqs.update(args)
        for x in args:
            x.__dependents.add(self)

            if (x.__buildable == False):
                self.__buildable = False
        
        if (self.__buildable == False):
            Target.buildReady.remove(self)
        



def main():
    """
    Create demo presentation of a buildsystem with multiple targets.
    """

    # Create targets 
    # Populate their dependents and prereqs sets.
    # Output the targets into a json file. (Directed Acyclic Graph is the three buildsystem)
    t1 = Target("t1")
    t2 = Target("t2")
    t3 = Target("t3")

    t1.dependsOn(t2, t3)
    for x in t1.get_prereqs():
        print(x.name)
    

if (__name__ == "__main__"):
    main()


