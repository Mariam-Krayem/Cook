"""
Conventions: docstrings and typing
"""

import os
import time
from pathlib import Path

def find_filepath(name: str, root=None) -> Path | None:
    """
    Traverses the files in the project directory and subdirectories. 
    Returns the filepath of the file whose name matches the argument. 
    If corresponding file does not exist, or if the extension is .py then 
    return null. 

    Parameters:
        name (str): name of file (case sensitive)
        root (str): project directory
    """
    if root is None:
        root = Path.cwd()
    else:
        root = Path(root)

    for file in root.rglob("*"):
        if file.is_file() and file.name == name:
            if file.suffix == ".py":
                continue
            return file

    return None
   

def get_file_timestamp(file: Path) -> float: 
    """
    Retrieves last-modified timestamp of a file

    Parameters:
        file (PAth): the file's Path object

    Returns:
        float: timestamp (last modified) formatted in seconds since the Unix Epoch
    """
    return file.stat().st_mtime # Use strftime() method to convert to date and time instead of seconds since the Unix epoch

class Target:
    """
    The target class is the node in the user's buildsystem tree. 

    Instance Attributes:
        name (str): name of the target instance
        __dependents (set[Target]): set containing target objects that depend on self.
        __prereqs (set[Target]): set containing target objects that self depends on.
        __recipe (str): a str that will be injected into cmd line to complete target/task
    
    Class Attributes: 
        targets (str:*Target): set of all targets in the buildsystem
    
    Public Methods:
        get_dependents(): returns __dependents
        get_prereqs(): returns __prereqs
        dependsOn(*args): adds self's dependencies to __prereqs and adds self to every arguments __dependents_t
    """
    targets: dict[str, "Target"] = {}

    def __init__(self, name, recipe):
        """Initializes instance of target class."""
        self.name: str = name # Temporary
        self.__dependents: set["Target"] = set()
        self.__prereqs: set["Target"] = set()
        self.__recipe: str = recipe
        Target.targets[self.name] = self
        

    def get_dependents(self) -> set["Target"]:
        """returns set of this target's dependencies"""
        return self.__dependents
    
    def get_prereqs(self) -> set["Target"]:
        """returns set of the target's that depend on this one."""
        return self.__prereqs

    def get_

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
    
    up_to_date: bool = True ## temp
    
    target: Target = Target.targets.get(file_name)

    if target is None:
        print("Error: Target has not been added to dependency system.")
        return ## since recursive in pre-reqs, we can assume that build will only run once in this case and a return statement will suffice. 
    
    if target.name in visiting:
        raise RecursionError("There is a forbidden cycle in your buildsystem.") ## Not entirely sure how to deal with cycles yet and if this is the most efficient way or not.
    if target.name in built:
        return

    visiting.add(target.name)
    
    target_Path = find_filepath(target.name)
    if target_Path is None:
        up_to_date = False

    for x in target.get_prereqs():
        build(x.name, visiting, built)
        
        x_Path = find_filepath(x.name)

        if up_to_date and x_Path:
            if get_file_timestamp(target_Path) < get_file_timestamp(x_Path):
                up_to_date = False 
        
        "If any of x have timestamp that is newer than current, current is flagged as not up_to_date"

    if not up_to_date:
        print(f"execute recipe for {target.name}") ## if current is not build_ready, then build"

    visiting.remove(target.name)
    built.add(target.name)
    

    


def main():
    """
    Create demo presentation of a buildsystem with multiple targets.
    """
    t1 = create_target("main.o", {"main.c", "defs.h"})
    t2 = create_target("main.c", {"app.h"})
    
    build("main.o")
    

if (__name__ == "__main__"):
    main()


