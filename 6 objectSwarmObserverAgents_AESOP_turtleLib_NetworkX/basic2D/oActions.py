from Tools import *
from Agent import *
from display2D import *


def do1b(address):
    pass


def do2a(address, cycle):
    self = address  # if necessary

    # ask each agent, without parameters

    print("Time = ", cycle, "ask all agents to report position")
    askEachAgentInCollection(
        address.modelSwarm.getAgentList(),
        Agent.reportPosition)


def do2b(address, cycle):
    self = address  # if necessary

    # ask a single agent, without parameters
    print("Time = ", cycle, "ask first agent to report position")
    if address.modelSwarm.getAgentList() != []:
        askAgent(address.modelSwarm.getAgentList()[0],
                 Agent.reportPosition)


def otherSubSteps(subStep, address):
    if subStep == "display2D":
        print("display2D under development!!!","Time = ",common.cycle)
        display2D(address.modelSwarm.agentList, common.cycle, address.nCycles,
                  common.sleep)
        return True

    #elif ...

    else:
        return False
