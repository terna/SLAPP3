# Agent.py
from Tools import *
from agTools import *


class Agent(SuperAgent):
    def __init__(self, number, myWorldState,
                 xPos, yPos, zPos, lX=0, rX=0, bY=0, tY=0, bZ=0, tZ=0,
                 agType=""):
                 # 0 definitions to be replaced (useful only if the
                 # dimensions are omitted and we do not use space)

        # the environment
        self.agOperatingSets = []
        self.number = number
        self.lX = lX
        self.rX = rX
        self.bY = bY
        self.tY = tY
        self.bZ = bZ
        self.tZ = tZ
        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType
        # the agent
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        print("agent", self.agType, "#", self.number,
              "has been created at", self.xPos, ",", self.yPos, ",", self.zPos)

    # ",**d" in the parameter lists of the methods is a place holder
    # in case we use, calling the method, a dictionary as last par

    # eating
    def eat(self, **d):
        print("I'm %s agent # %d: " % (self.agType, self.number), end=' ')
        print("nothing to eat here!")

    # dancing
    def dance(self, **d):
        print("I'm %s agent # %d: " % (self.agType, self.number), end=' ')
        if self.agType == "tasteA":
            print("I'm an A, nice to dance here!")
        elif self.agType == "tasteB":
            print("I'm a B, not so nice to dance here!")
        elif self.agType == "tasteC":
            print("I'm a C, why to dance here?")

        else:
            print("it's not time to dance!")

    # the action, also jumping
    def randomMovement(self, **k):
        if random.random() <= self.myWorldState.getGeneralMovingProb():
            print("agent %s # %d moving" % (self.agType, self.number))
            self.jump = 1
            if "jump" in k:
                self.jump = k["jump"]
            dx = randomMove(self.jump)
            self.xPos += dx
            dy = randomMove(self.jump)
            self.yPos += dy
            #self.xPos = (self.xPos + self.worldXSize) % self.worldXSize
            #self.yPos = (self.yPos + self.worldYSize) % self.worldYSize
            if self.xPos < self.lX:
                self.xPos = self.lX
            if self.xPos > self.rX:
                self.xPos = self.rX
            if self.yPos < self.bY:
                self.yPos = self.bY
            if self.yPos > self.tY:
                self.yPos = self.tY

    # report
    def reportPosition(self, **d):
        print(self.agType, "agent # ", self.number, " is at X = ",
              self.xPos, " Y = ", self.yPos)

    def reportPos(self, **d):
        return (self.xPos, self.yPos)


    # adding a task (from v. 1.35 of SLAPP)
    # common is derived importing Tools
    def addTask(self):

        newTask = "all dance"

        print(
            "agent",
            self.number,
            "adding a task for cycle",
            common.cycle + 1)
        if common.cycle + 1 not in common.addTasks:
            common.addTasks[common.cycle + 1] = []
        common.addTasks[common.cycle + 1].append(newTask)

    # eliminating a task (from v. 1.35 of SLAPP)
    # common is derived importing Tools
    def elimTask(self):

        killTask = "tasteC eat"

        print("agent", self.number, "eliminating a task for cycle",
              common.cycle + 2)
        if common.cycle + 2 not in common.elimTasks:
            common.elimTasks[common.cycle + 2] = []
        common.elimTasks[common.cycle + 2].append(killTask)


# returns -1, 0, 1  with equal probability
def randomMove(jump):
    return random.randint(-1, 1) * jump
