# makefile_alt
Python program that manages projects like makefile.

Goal of this project is to create a file management system similar to makefile that can be integrated into large projects as a module and managed through a python script rather than a textfile. The main workings of this program are like make. 

Makefile is a text file that lists the different targets in a project and their dependencies as well as how to create these targets (targets + recipes) Make is a command that builds a specific target, or the first target if none is specified after "make"

There are 3 main steps to building a target:
1. Parse the makefile
2. Build an internal dependency graph (Directed Acyclic Graph)
3. Traverse the graph recursively and execute recipes if needed

### 1. Parse the makefile & Build Graph
The make parser reads the makefile text file and interprets variables and rules. The internal dependency graph is actually built incrementally as the makefile is parsed. So when the parser encounters a rule, it inputs the name of the target in the hash table to verify whether the node object for it exists already. If there does not exists a node object that corresponds to the target's string, we create a new node object and insert it into the hash table. Otherwise, we don't create a new node and we move on to said target's dependencies. Again, we verify if there corresponds nodes in the hashtable to the file's string. If no, we create new nodes and list them as dependencies of the target nodes (i.e. create directed edge from target to new node). Otherwise, we don't create a new node and we just create the directed edge between the target and the node. As the parser reads the rest of the makefile, the graph builds. 

There are a few cases where additional processing is needed after parsing, such as:
- expanding deferred variables (= assignments),

### 2. Traversing Graph and Executing Recipes
Depending on which target we are looking to create, we traverse the dependencies of said target recursively. Once we have reached a node that doesn't not have any dependencies (i.e. a leaf node), the recursive branches start closing by verifiying if the node's dependent(s) are newer or older. IF they are older, then we execute the recipe for the dependent(s) and so on and so forth until we return to the target node. 

make(t1):
    does t1 have dependencies?
        yes:
            for all of t1's dependencies: make()
        no: 
            build t1


Next step would be to enable different tasks. 
Create framework for tasks and let user define their own. (i.e. upload, download, clean, etc)