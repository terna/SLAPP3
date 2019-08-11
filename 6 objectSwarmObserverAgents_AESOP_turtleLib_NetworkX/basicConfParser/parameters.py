# parameters.py
from Tools import *
import INIreader as ini


def loadParameters(self):

    # Project version
    try:
        projectVersion = str(common.projectVersion)
    except BaseException:
        projectVersion = "Unknown"
    print("\nProject version " + projectVersion)

    print ("random number seed (1 to get it from the clock) :", common.mySeed)
    if common.mySeed == 1:
        random.seed()
    else:
        random.seed(common.mySeed)

    self.nAgents = common.nAgents
    print("Employing",self.nAgents,"bland agent(s)")

    #self.worldXSize= input("X size of the world? ")
    self.worldXSize = 50
    print("X size of the world? ", self.worldXSize)

    #self.worldYSize= input("Y size of the world? ")
    self.worldYSize = 50
    print("Y size of the world? ", self.worldYSize)

    self.nCycles = common.nCycles
    print("Number of cycles (0 = exit) :", self.nCycles)
