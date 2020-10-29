# start 6 objectSwarmObserverAgentsAESOP.py


# 'project' is by default both the name of the application and of the subfolder
# that contains its code; the subfolder is supposed to be placed within the
# SLAPP tree

# the folder can can be placed outside the SLAPP tree if we place a file
# project.txt in the folder "6 objectSwarmObserverAgents_AESOP_turtleLib_NetworkX"
# the file has to contain the path and the name of the folder of the project


def runSLAPP():
    global start_pyDir
    print("\nSLAPP v3.3.9 build 20201029\n")
    import os

    confirm = "n"
    found = False
    start_pyDir = os.getcwd()
    names1 = os.listdir("./")
    names2 = os.listdir("../")
    name = False
    if "project.txt" in names1: #main folder
        name = "project.txt"
    if "project.txt" in names2: # folder 6...
        name = "../project.txt"
    if name:
        currentProject = open(name, "r")
        pathAndProject = currentProject.readline()
        if pathAndProject[-1] == "\n" or pathAndProject[-1] == "\r":
            pathAndProject = pathAndProject[0:-1]
        if pathAndProject[-1] == "\n" or pathAndProject[-1] == "\r":
            pathAndProject = pathAndProject[0:-1]
        # -1 means: last character
        # [0:-1] means: the string but the last caracter
        # the last caracter is eliminated in the given case (twice) to avoid
        # interferences between the control characters within the file and the
        # path definition
        print("path and project = " + pathAndProject)
        confirm = input("do you confirm? ([y]/n): ")
        if confirm == "y" or confirm == "Y" or confirm == "":
            found = True
        currentProject.close()

    if confirm == "y" or confirm == "Y" or confirm == "":
        project = pathAndProject
    else:
        p=None
        while p==None:
            project = input("Project name? ")
            if project not in names1:
                print("Project " + project + " not found")
            else: p=project
        else:
            found = True
            project = "./" + project

    if found:
        import sys
        sys.path.append("./$$slapp$$")
        if confirm != "y" and confirm != "Y" and confirm != "":
            sys.path.append(project)
        else:
            sys.path.append(pathAndProject)

        import commonVar as common
        # if kernelUsesNumpyRandom is defined (True or False) in commonVar.py
        # of the project, no other action is requested
        try:
            common.kernelUsesNumpyRandom
        # if the definition is missing, we do it here
        except BaseException:
            common.kernelUsesNumpyRandom = False
        #print("kernelUsesNumpyRandom =", common.kernelUsesNumpyRandom)

        import Tools as tl
        import graphicControl as gc

        gc.graphicControl()
        # print common.graphicStatus

        # project reported in common for possible uses in other SLAPP segments or
        # applications
        # it contains (i) or the path (relative to the start.py position) of a project
        # existing within the SLAPP hierarchy, or (ii) the absolute path to a project
        # placed outside
        common.project = project

        common.IPython = tl.checkRunningIn()
        if common.IPython:
            print("running in IPython")
        else:
            print("running in Python")

        import ObserverSwarm as obs


        # if debug is defined (True or False) in commonVar.py of the project, no
        # other action is requested
        try:
            common.debug
        # if the definition is missing, we do it here
        except BaseException:
            common.debug = False  # if debug il True a large part of the try/except
            # structures will be bypassed, so the errors will
            # be managed directly by the Python interpreter

            # this choice can be useful when you build a new project
            # and as an expert user you want to check the errors
            # in a basic way
        print("debug =", common.debug)

        observerSwarm = obs.ObserverSwarm(project)
        common.pro = project  # to be used within the oActions.py and
                              # mActions.py extensions

        # create objects
        observerSwarm.buildObjects()

        # create actions
        observerSwarm.buildActions()

        # run
        observerSwarm.run()

        if common.IPython:
            print(
                "End of the run! TO RUN AGAIN IN JUPYTER REMEMBER TO RESTART THE KERNEL")


# running alone
if __name__ == "__main__":
    runSLAPP()
