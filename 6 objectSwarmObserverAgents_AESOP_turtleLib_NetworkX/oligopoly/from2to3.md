May 2017

## **Moving to Python 3**

### Automatic changes

The first step has been that of using *2to3*, which is part of the Python 2 distribution, with the script *my2to3* (reported here), containing:  

    #!/bin/bash  
    2to3 -W "$1" > changes  
    mv changes "$1".changes  

e.g.  

    my2to3 "a file.py"

(with the usual chain of ../../ etc. in the beginning (before my2to3) and the name of the file quoted if it contains spaces)

produces:

    a file.py : the corrected file   
    a file.bak : the backup of the previous .py file   
    a file.changes : the list of the changes

The correction done in this way are mainly related to *print* and *input* statements

**Handmade** corrections

To *parameters.py*, documented in the commit *parameters.py hand made corrections*

To *Agent.py*, with str for version "3" comparing
