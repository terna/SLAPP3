from Tools import *
from Agent import *
import os
import random
import commonVar as common


def do0(address):
    self = address  # if necessary
    askEachAgentInCollection(address.agentList, Agent.setNewCycleValues)


def do1(address):
    self = address  # if necessary

    # keep safe the original list
    address.agentListCopy = address.agentList[:]
    # never in the same order (please comment if you want to keep
    # always the same sequence
    random.shuffle(address.agentListCopy)


def createTheAgent(self, line, num, agType):
    # explicitly pass self, here we use a function

    # check for at least one agent with number==1
    if num == 1:
        common.agent1existing = True

        #create file for first hayekian step output
        import csv
        common.csvf=open(common.pro + "/" +\
           "firstStepOutputInHayekianMarket.csv", "w")
        common.wr=csv.writer(common.csvf)
        common.closed=False

    # workers
    if agType == "workers":
        anAgent = Agent(num, self.worldState,
                        float(line.split()[1]) + random.gauss(0, common.sigma),
                        float(line.split()[2]) + random.gauss(0, common.sigma),
                        agType=agType)
        self.agentList.append(anAgent)
        anAgent.setAgentList(self.agentList)

    # entrepreneurs
    elif agType == "entrepreneurs":
        anAgent = Agent(num, self.worldState,
                        float(line.split()[1]) + random.gauss(0, common.sigma),
                        float(line.split()[2]) + random.gauss(0, common.sigma),
                        agType=agType)
        self.agentList.append(anAgent)

        # anAgent.setAgentList(self.agentList) #in ModelSwarm.py

    else:
        print("Error in file " + agType + ".txt")
        os.sys.exit(1)
