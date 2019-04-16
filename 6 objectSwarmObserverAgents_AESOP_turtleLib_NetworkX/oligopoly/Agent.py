# Agent.py
from Tools import *
from agTools import *
from random import *
import graphicDisplayGlobalVarAndFunctions as gvf
import commonVar as common
import numpy.random as npr
import numpy
import pandas as pd
import os



def mySort(ag):
    if ag == []:
        return []
    numAg = []
    for a in ag:
        numAg.append((a.number, a))
    numAg.sort()
    agSorted = []
    for i in range(len(numAg)):
        agSorted.append(numAg[i][1])
    return agSorted

def applyRationallyTheRateOfChange(base,rate):
        if rate >= 0:
            return base*(1+rate)
        if rate <  0:
            return base/(1+abs(rate))

class Agent(SuperAgent):
    def __init__(self, number, myWorldState,
                 xPos=0, yPos=0, agType=""):

        # print xPos,yPos

        # the graph
        if gvf.getGraph() == 0:
            gvf.createGraph()
        common.g.add_node(self)

        # the environment

        self.agOperatingSets = []
        self.number = number
        self.agType = agType
        self.numOfWorkers = 0  # never use it directly to make calculations
        self.profit = 0
        self.plannedProduction = 0
        self.soldProduction = 0
        self.revenue = 0
        self.consumption = 0
        self.consumptionQuantity=0
        self.employed = False
        self.extraCostsResidualDuration = 0
        self.profitStrategyReverseAfterN=0
        self.priceSwitchIfProfitFalls=""

        if agType == 'workers': #useful in initial creation
            common.orderedListOfNodes.append(self)
            # use to keep the order
            # in output (ex. adjacency matrix)

            # colors at http://www.w3schools.com/html/html_colornames.asp
            gvf.colors[self] = "OrangeRed"

            self.employed = False

            self.workTroubles = 0

            self.unspentConsumptionCapability = 0

            self.jump = 0


        if agType == 'entrepreneurs': #useful in initial creation
            common.orderedListOfNodes.append(self)
            # use to keep the order
            # in output (ex. adjacency matrix)

            # colors at http://www.w3schools.com/html/html_colornames.asp
            gvf.colors[self] = "LawnGreen"

            self.employed = True
            self.plannedProduction = -100  # not used in plots if -100
            self.hasTroubles = 0

            self.unspentConsumptionCapability = 0

            self.jump = 0

        self.myWorldState = myWorldState
        self.agType = agType

        # the agents
        if common.verbose:
            print("agent of type", self.agType,
                  "#", self.number, "has been created at", xPos, ",", yPos)

        gvf.pos[self] = (xPos, yPos)
        if common.nodeNumbersInGraph:
            common.g_labels[self] = str(number)
        # to be used to clone (if any)
        self.xPos = xPos
        self.yPos = yPos

        # price memory
        self.buyPrice  = -1000
        self.sellPrice = 1000
        self.sellPriceDefined=False

        # consumption planning for the current cycle
        # if the planning has been made, the variable contains
        # the number of the cycle
        self.consumptionPlanningInCycleNumber = -1

        #  status to be used in actOnMarketPlace acting as a buyer
        #  0 means never used
        #  1 if previous action was a successful buy attempt
        # -1 if previous action was an unsuccessful buy attempt
        self.statusB = 0

        #  status to be used in actOnMarketPlace acting as a seller
        #  0 means never used
        #  1 if previous action was a successful sell attempt
        # -1 if previous action was an unsuccessful sell attempt
        self.statusS = 0


    # talk
    def talk(self):
        print(self.agType, self.number)

    # reset values, redefining the method of agTools.py in $$slapp$$
    def setNewCycleValues(self):
        # the if is to save time, given that the order is arriving to
        # all the agents (in principle, to reset local variables)
        if not common.agent1existing:
            print("At least one of the agents has to have number==1")
            print("Missing that agent, all the agents are resetting common values")

        if self.number == 1 or not common.agent1existing:

            # introduced with V6
            # V6 reset block starts hene
            # this part is specific of the first hayekian cycle
            # where it replaces the lack of a previous value in
            # quantity
            # here, if possible, we use the price at t-2
            if common.startHayekianMarket > 1:
               if common.cycle == common.startHayekianMarket:
                  if len(common.ts_df.price.values) == 1:
                     previuosPrice = common.ts_df.price.values[-1]  # t=2
                  if len(common.ts_df.price.values) > 1:
                     previuosPrice = common.ts_df.price.values[-2]  # t>2
                  # the code above can act only if t>1
                  if common.cycle > 1: # if == 1 do nothing
                                       # makeProductionPlan acts
                                       # establishing directly
                                       # self.plannedProduction and the total
                                       # common.totalPlannedProduction
                     common.totalConsumptionInQuantityInPrevious_TimeStep = \
                       common.totalPlannedConsumptionInValueInA_TimeStep  \
                       / previuosPrice

            # not in case common.cycle == common.startHayekianMarket == 1
            elif common.cycle > common.startHayekianMarket:
                common.totalConsumptionInQuantityInPrevious2_TimeStep= \
                 common.totalConsumptionInQuantityInPrevious1_TimeStep # init. in common
                common.totalConsumptionInQuantityInPrevious1_TimeStep = \
                 common.totalConsumptionInQuantityInA_TimeStep
                if common.cycle==common.startHayekianMarket+1:
                 common.totalConsumptionInQuantityInPrevious_TimeStep = \
                 common.totalConsumptionInQuantityInPrevious1_TimeStep
                if common.cycle > common.startHayekianMarket+1:
                 common.totalConsumptionInQuantityInPrevious_TimeStep = \
                 common.Q*common.totalConsumptionInQuantityInPrevious1_TimeStep +\
                 (1-common.Q)*common.totalConsumptionInQuantityInPrevious2_TimeStep

            # !!!! here we can use also delayed values, look at !!!! in
            # notesOnHayekianTransformation.md

            common.totalConsumptionInQuantityInA_TimeStep = 0

            # list of all the transaction prices in a cycle of the
            # hayekian market
            common.hayekianMarketTransactionPriceList_inACycle=[]
            # v6 reset block ends here

            common.totalProductionInA_TimeStep = 0
            common.totalPlannedConsumptionInValueInA_TimeStep = 0

            common.totalProfit = 0
            common.totalPlannedProduction = 0

            # ratio sellers/buyers
            common.ratioSellersBuyersAlreadySet=False

        # troubles related idividual variables
        if self.agType == "entrepreneurs":
            self.hasTroubles = 0
        if self.agType == "workers":
            self.workTroubles = 0


    # hireIfProfit
    def hireIfProfit(self):

        # workers do not hire
        if self.agType == "workers":
            return

        if self.profit <= common.hiringThreshold:
            return

        tmpList = []
        for ag in self.agentList:
            if ag != self:
                if ag.agType == "workers" and not ag.employed:
                    tmpList.append(ag)

        if len(tmpList) > 0:
            hired = tmpList[randint(0, len(tmpList) - 1)]

            hired.employed = True
            gvf.colors[hired] = "Aqua"
            gvf.createEdge(self, hired)  # self, here, is the hiring firm

        # count edges (workers) of the firm, after hiring (the values is
        # recorded, but not used directly)
        self.numOfWorkers = gvf.nx.degree(common.g, nbunch=self)
        # nbunch : iterable container, optional (default=all nodes)
        # A container of nodes. The container will be iterated through once.
        print("entrepreneur", self.number, "has",
              self.numOfWorkers, "edge/s after hiring")

    def hireFireWithProduction(self):

        # workers do not hire/fire
        if self.agType == "workers":
            return

        # to decide to hire/fire we need to know the number of employees
        # the value is calcutated on the fly, to be sure of accounting for
        # modifications coming from outside
        # (nbunch : iterable container, optional (default=all nodes)
        # A container of nodes. The container will be iterated through once.)

        laborForce0 = gvf.nx.degree(common.g, nbunch=self) + \
            1  # +1 to account for the entrepreneur herself

        # required labor force
        laborForceRequired = int(
            self.plannedProduction / common.laborProductivity)

        #
        # countUnemployed=0
        # for ag in self.agentList:
        #    if not ag.employed: countUnemployed+=1

        # print "I'm entrepreneur %d laborForce %d and required %d unemployed are %d" %\
        #(self.number, laborForce0, laborForceRequired, countUnemployed)

        # no action
        if laborForce0 == laborForceRequired:
            return

        # hire
        if laborForce0 < laborForceRequired:
            n = laborForceRequired - laborForce0
            tmpList = []
            for ag in self.agentList:
                if ag != self:
                    if ag.agType == "workers" and not ag.employed:
                        tmpList.append(ag)

            if len(tmpList) > 0:
                k = min(n, len(tmpList))
                shuffle(tmpList)
                for i in range(k):
                    hired = tmpList[i]
                    hired.employed = True
                    gvf.colors[hired] = "Aqua"
                    gvf.createEdge(self, hired)
                    # self, here, is the hiring firm

            # count edges (workers) of the firm, after hiring (the values is
            # recorded, but not used directly)
            self.numOfWorkers = gvf.nx.degree(common.g, nbunch=self)
            # nbunch : iterable container, optional (default=all nodes)
            # A container of nodes. The container will be iterated through
            # once.
            print(
                "entrepreneur",
                self.number,
                "is applying prod. plan and has",
                self.numOfWorkers,
                "edge/s after hiring")

        # fire
        if laborForce0 > laborForceRequired:
            n = laborForce0 - laborForceRequired

            # the list of the employees of the firm
            #entrepreneurWorkers = gvf.nx.neighbors(common.g, self) with nx 2.0
            entrepreneurWorkers = list(common.g.neighbors(self))
            # print "entrepreneur", self.number, "could fire",
            # entrepreneurWorkers

            # the list returnes by nx is unstable as order
            entrepreneurWorkers = mySort(entrepreneurWorkers)

            if len(entrepreneurWorkers) > 0:  # has to be, but ...
                shuffle(entrepreneurWorkers)
                for i in range(n):
                    fired = entrepreneurWorkers[i]

                    gvf.colors[fired] = "OrangeRed"
                    fired.employed = False

                    # common.g_edge_labels.pop((self,fired)) no labels in edges
                    common.g.remove_edge(self, fired)

            # count edges (workers) after firing (recorded, but not used
            # directly)
            self.numOfWorkers = gvf.nx.degree(common.g, nbunch=self)
            # nbunch : iterable container, optional (default=all nodes)
            # A container of nodes. The container will be iterated through
            # once.
            print(
                "entrepreneur",
                self.number,
                "is applying prod. plan and has",
                self.numOfWorkers,
                "edge/s after firing")

    # fireIfProfit
    def fireIfProfit(self):

        # workers do not fire
        if self.agType == "workers":
            return

        if self.profit >= common.firingThreshold:
            return

        # the list of the employees of the firm
        #entrepreneurWorkers = gvf.nx.neighbors(common.g, self) with nx 2.0
        entrepreneurWorkers = list(common.g.neighbors(self))
        # print "entrepreneur", self.number, "could fire", entrepreneurWorkers

        # the list returnes by nx is unstable as order
        entrepreneurWorkers = mySort(entrepreneurWorkers)

        if len(entrepreneurWorkers) > 0:
            fired = entrepreneurWorkers[randint(
                0, len(entrepreneurWorkers) - 1)]

            gvf.colors[fired] = "OrangeRed"
            fired.employed = False

            # common.g_edge_labels.pop((self,fired)) no label in edges
            common.g.remove_edge(self, fired)

            # count edges (workers) after firing (recorded, but not used
            # directly)
            self.numOfWorkers = gvf.nx.degree(common.g, nbunch=self)
            # nbunch : iterable container, optional (default=all nodes)
            # A container of nodes. The container will be iterated through
            # once.
            print("entrepreneur", self.number, "has",
                  self.numOfWorkers, "edge/s after firing")

    # produce
    def produce(self):

        # this is an entrepreneur action
        if self.agType == "workers":
            return

        # to produce we need to know the number of employees
        # the value is calcutated on the fly, to be sure of accounting for
        # modifications coming from outside
        # (nbunch : iterable container, optional (default=all nodes)
        # A container of nodes. The container will be iterated through once.)

        laborForce = gvf.nx.degree(common.g, nbunch=self) + \
            1  # +1 to account for the entrepreneur herself
        print("I'm entrepreneur", self.number, "my laborforce is", laborForce)

        # productivity is set to 1 in the benginning from common space
        self.production = common.laborProductivity * \
            laborForce

        # totalProductionInA_TimeStep
        common.totalProductionInA_TimeStep += self.production
        # having a copy, that is update after each agent's action
        common.totalProductionInPrevious_TimeStep = common.totalProductionInA_TimeStep

    # produce
    def produceV5(self):

        # this is an entrepreneur action
        if self.agType == "workers":
            return

        # to produce we need to know the number of employees
        # the value is calcutated on the fly, to be sure of accounting for
        # modifications coming from outside
        # (nbunch : iterable container, optional (default=all nodes)
        # A container of nodes. The container will be iterated through once.)

        laborForce = gvf.nx.degree(common.g, nbunch=self) + \
            1  # +1 to account for the entrepreneur herself
        print("I'm entrepreneur", self.number, "my laborforce is", laborForce)

        # productivity is set to 1 in the benginning from common space
        self.production = common.laborProductivity * \
            laborForce

        # print "I'm entrepreneur",self.number,"production before correction is",\
        #    self.production

        # correction for work troubles, if any
        # self.hasTroubles is 0 if no troubles
        self.production *= (1. - self.hasTroubles)

        # print "I'm entrepreneur",self.number,"production after correction is",\
        #    self.production


        # totalProductionInA_TimeStep
        common.totalProductionInA_TimeStep += self.production
        # having a copy, that is update after each agent's action
        common.totalProductionInPrevious_TimeStep = common.totalProductionInA_TimeStep

    # makeProductionPlan
    def makeProductionPlan(self):

        # this is an entrepreneur action
        if self.agType == "workers":
            return

        if common.projectVersion >= "3" and common.cycle == 1:
            nEntrepreneurs = 0
            for ag in self.agentList:
                if ag.agType == "entrepreneurs":
                    nEntrepreneurs += 1
            # print nEntrepreneurs
            nWorkersPlus_nEntrepreneurs = len(self.agentList)
            # print nWorkersPlus_nEntrepreneurs
            common.nu = (
                common.rho * nWorkersPlus_nEntrepreneurs) / nEntrepreneurs
            # print common.rho, common.nu

        if (common.projectVersion >= "3" and common.cycle == 1) or \
                common.projectVersion < "3":
            self.plannedProduction = npr.poisson(
                common.nu, 1)[0]  # 1 is the number
            # of element of the returned matrix (vector)
            # print self.plannedProduction

            common.totalPlannedProduction += self.plannedProduction
            # print "entrepreneur", self.number, "plan", self.plannedProduction,\
            #  "total", common.totalPlannedProduction

    # adaptProductionPlan
    def adaptProductionPlan(self):
        if common.cycle > 1:
            nEntrepreneurs = 0
            for ag in self.agentList:
                if ag.agType == "entrepreneurs":
                    nEntrepreneurs += 1

            # previous period price
            #print ("++++++++++++++++++++++", common.ts_df.price.values[-1])
            #print ("&&&&&&&&&&&&&&&&&&&&&&",len(common.ts_df.price.values))

            if len(common.ts_df.price.values) == 1:
                previuosPrice = common.ts_df.price.values[-1]  # t=2
            if len(common.ts_df.price.values) > 1:
                previuosPrice = common.ts_df.price.values[-2]  # t>2
            # NB adapt acts from t>1

            self.plannedProduction = (common.totalDemandInPrevious_TimeStep /
                                      previuosPrice) \
                / nEntrepreneurs

            #self.plannedProduction += gauss(0,self.plannedProduction/10)

            shock = uniform(
                -common.randomComponentOfPlannedProduction,
                common.randomComponentOfPlannedProduction)

            if shock >= 0:
                self.plannedProduction *= (1. + shock)

            if shock < 0:
                shock *= -1.
                self.plannedProduction /= (1. + shock)
            # print self.number, self.plannedProduction

            common.totalPlannedProduction += self.plannedProduction
            # print "entrepreneur", self.number, "plan", self.plannedProduction,\
            #    "total", common.totalPlannedProduction

    # adaptProductionPlanV6
    def adaptProductionPlanV6(self):

        # pre hayekian period
        if common.cycle > 1 and common.cycle < common.startHayekianMarket:
            # count of the entrepreneur number
            nEntrepreneurs = 0
            for ag in self.agentList:
                if ag.agType == "entrepreneurs":
                    nEntrepreneurs += 1

            # with the scheme of prices until V.5c_fd
            if len(common.ts_df.price.values) == 1:
                previuosPrice = common.ts_df.price.values[-1]  # t=2
            if len(common.ts_df.price.values) > 1:
                previuosPrice = common.ts_df.price.values[-2]  # t>2
            # NB adapt acts from t>1

            self.plannedProduction = (common.totalDemandInPrevious_TimeStep /
                                      previuosPrice) \
                / nEntrepreneurs

            shock = uniform(
                -common.randomComponentOfPlannedProduction,
                common.randomComponentOfPlannedProduction)

            if shock >= 0:
                self.plannedProduction *= (1. + shock)

            if shock < 0:
                shock *= -1.
                self.plannedProduction /= (1. + shock)
            # print self.number, self.plannedProduction

            common.totalPlannedProduction += self.plannedProduction
            # print "entrepreneur", self.number, "plan", self.plannedProduction,\
            #    "total", common.totalPlannedProduction

        # hayekian period
        if common.cycle >1 and common.cycle >= common.startHayekianMarket:
            #the case common.cycle==1, with common.startHayekianMarket==1, is
            #absorbed by makeProductionPlan

            nEntrepreneurs = 0
            for ag in self.agentList:
                if ag.agType == "entrepreneurs":
                    nEntrepreneurs += 1


            self.plannedProduction = \
                      common.totalConsumptionInQuantityInPrevious_TimeStep \
                      / nEntrepreneurs

            shock = uniform(
                -common.randomComponentOfPlannedProduction,
                common.randomComponentOfPlannedProduction)

            if shock >= 0:
                self.plannedProduction *= (1. + shock)

            if shock < 0:
                shock *= -1.
                self.plannedProduction /= (1. + shock)
            # print self.number, self.plannedProduction

            common.totalPlannedProduction += self.plannedProduction
            # print "entrepreneur", self.number, "plan", self.plannedProduction,\
            #    "total", common.totalPlannedProduction

            # to record sold production and revenue in hayekian phase
            self.soldProduction=0
            self.revenue=0


    # set initial sell and buy prices in hayekian market
    def setInitialPricesHM(self):

        # 1 -----------------------------------------
        if common.cycle >= common.startHayekianMarket:
          if not common.ratioSellersBuyersAlreadySet:
              nEntrepreneurs = 0
              for ag in self.agentList:
                if ag.agType == "entrepreneurs":
                          nEntrepreneurs += 1
              nSellers=nEntrepreneurs

              nBuyers=len(self.agentList)

              common.ratioSellersBuyersAlreadySet=True
              common.ratioSellersBuyers=nSellers/nBuyers
              print("\nRatio sellers/buyers =",common.ratioSellersBuyers,"\n")
              # in setNewCycleValues common.ratioSellersBuyersAlreadySet=False
              # at the beginning of each cycle

        # 2 -----------------------------------------
        if common.cycle == common.startHayekianMarket and \
                        not common.priceWarmingDone:
           # setting the basic price uniquely before the first hayekian cycle
           common.sellPrice=1000
           common.buyPrice=-1000
           if common.startHayekianMarket>1:
            if len(common.ts_df.price.values) == 1:
              common.buyPrice  = common.sellPrice = \
                      common.ts_df.price.values[-1] # the last price
              #print("Ag.", self.number,"buying at", self.buyPrice,
              #                         "selling at",self.sellPrice)
              # NB the code above can act only if t>1
            if len(common.ts_df.price.values) > 1:
              common.buyPrice  = common.sellPrice = \
                      common.ts_df.price.values[-2] # the second last price
              #print("Ag.", self.number,"buying at", self.buyPrice,
              #                         "selling at",self.sellPrice)
              # NB the code above can act only if t>2
              # NB NB  we set the sellPrice also for workers but we do not
              #        use it
              #        when a worker becomes an entreprenuer she copies the
              #        sell price of the firm she is coming from

           else: # case t==1 being common.startHayekianMarket==1
                 # look at the equilibrium price that would have been created
                 # at t==1 in the non-hayekian execution

                 # in the common.startHayekianMarket == 1 case, when
                 # actOnMaketPlace is activated
                 # we already have
                 # common.totalPlannedConsumptionInValueInA_TimeStep and
                 # common.totalProductionInA_TimeStep
                 # so, we can calculate
              common.buyPrice  = common.sellPrice = \
                            common.totalPlannedConsumptionInValueInA_TimeStep \
                            / common.totalProductionInA_TimeStep
                 # outside WorldState setMarketPriceV3 method, to avoid here
                 # random shocks
                 # NB NB  we set the sellPrice also for workers but we do not
                 #        use it
                 #        when a worker becomes an entreprenuer she copies the
                 #        sell price of the firm she is coming from

           #startingHayekianCommonPrice
           print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
           print("starting hayekian common price",common.buyPrice)
           print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

           common.priceWarmingDone = True

        # 3 -----------------------------------------
        # individual starting prices
        if common.cycle == common.startHayekianMarket:

           #starting sell price
           self.sellPrice = \
                     applyRationallyTheRateOfChange(common.sellPrice,\
                        uniform(-common.initShift*common.initShock, \
                                (1-common.initShift)*common.initShock))
           if self.agType=="entrepreneurs":
               print("entrepreneur", self.number, "has initial sell price",\
                                     self.sellPrice)
           self.sellPriceDefined=True

           # starting individual buy price
           self.buyPrice = \
                     applyRationallyTheRateOfChange(common.buyPrice,\
                        uniform((common.initShift-1)*common.initShock, \
                                common.initShift*common.initShock))



    # modify a specific sell price with a jump on the side of the up
    # corrections, in full hayekian market
    # NB we are at the end of each cycle
    def nextSellPriceJumpFHM(self):
        if self.agType != "entrepreneurs": return
        if common.hParadigm=="quasi": return

        if common.pJump != -1 and npr.uniform(0,1)<=common.pJump:
            if self.jump == 0:
                self.jump=common.jump
                self.sellPrice *= 1 + self.jump
                print("entrepreur # ", self.number, \
                      "raises the sell price with a jump")
            else:
                self.sellPrice /= 1 + self.jump
                self.jump=0
                print("entrepreur # ", self.number, \
                      "reduces the sell price with a jump back")


    # modify sell prices in quasi hayekian market
    # NB we are at the end of each cycle
    def nextSellPricesQHM(self):
        if self.agType != "entrepreneurs": return
        if common.hParadigm=="full": return

        # hayekian period, "quasi" hayekian paradigm

        # i) considering relative unsold quantity
        if common.hParadigm=="quasi" and common.quasiHchoice=="unsold":
         if common.cycle >= common.startHayekianMarket:

          oldP=self.sellPrice
          if common.cycle >1 and \
           common.entrepreneursMindIfPlannedProductionFalls and \
           common.ts_df.iloc[-1, 3] / common.totalPlannedProduction - 1 >= \
                   common.thresholdToDecreaseThePriceIfTotalPlannedPFalls:
           # indexing Python style, pos. -1 is the last one
            self.sellPrice = applyRationallyTheRateOfChange(self.sellPrice,\
                                     uniform(common.decreasingRateRange, 0))
            print(("end of t = %d entrepreneur %d initial production"+\
                   " %.2f sold  %.3f \nold price %.3f new price %.3f as "+\
                   " total plannedProduction falls") %\
                   (common.cycle,self.number,self.production,\
                    self.soldProduction,oldP,self.sellPrice))

          else:
            if self.soldProduction/self.production <= common.soldThreshold1:
                self.sellPrice = applyRationallyTheRateOfChange(self.sellPrice,\
                                        uniform(common.decreasingRateRange, 0))
            if self.production/self.production>=common.soldThreshold2:
                self.sellPrice = applyRationallyTheRateOfChange(self.sellPrice,\
                                        uniform(0, common.increasingRateRange))

            print(("end of t = %d entrepreneur %d initial production"+\
                   " %.2f sold  %.3f \nold price %.3f new price %.3f") %\
                   (common.cycle,self.number,self.production,\
                    self.soldProduction,oldP,self.sellPrice))
          return

        # ii) considering randomUp
        if common.hParadigm=="quasi" and common.quasiHchoice=="randomUp":
            if common.pJump != -1 and npr.uniform(0,1)<=common.pJump:
                        if self.jump == 0:
                            self.jump=common.jump
                            self.sellPrice *= 1 + self.jump
                            print("entrepreur # ", self.number, \
                                  "raises the sell price with a jump")
                        else:
                            self.sellPrice /= 1 + self.jump
                            self.jump=0
                            print("entrepreur # ", self.number, \
                                  "reduces the sell price with a jump back")

            return

        # iii) consideirng profit falls to act on price
        if common.hParadigm=="quasi" and common.quasiHchoice=="profit":
          if common.cycle >= common.startHayekianMarket:
               if self.profitStrategyReverseAfterN==0:
                   if common.priceSwitchIfProfitFalls=="raise":

                    if npr.uniform(0,1)<=0.6:
                        self.priceSwitchIfProfitFalls="raise"
                    else:
                        self.priceSwitchIfProfitFalls="lower"

                   if common.priceSwitchIfProfitFalls=="lower":

                    if npr.uniform(0,1)<=0.4:
                        self.priceSwitchIfProfitFalls="raise"
                    else:
                        self.priceSwitchIfProfitFalls="lower"

                   if common.pJump != -1 and self.profit <0 and \
                                 npr.uniform(0,1)<=common.pJump:
                     if self.priceSwitchIfProfitFalls=="raise":
                        self.sellPrice *= 1 + common.jump
                        print("entrepreur # ", self.number, \
                        "with profit<0, is raising the sell price")
                        self.profitStrategyReverseAfterN=\
                                  common.profitStrategyReverseAfterN
                        #  0 means: acting again always possible
                        #  a value > the number of cycles means:
                        #           acting again never possible
                     if self.priceSwitchIfProfitFalls=="lower":
                        self.sellPrice /= 1 + common.jump
                        print("entrepreur # ", self.number, \
                        "with profit<0, is lowering the sell price")
                        self.profitStrategyReverseAfterN=\
                                  common.profitStrategyReverseAfterN

               else:
                   self.profitStrategyReverseAfterN-=1
                   if self.profitStrategyReverseAfterN==0:
                     if self.priceSwitchIfProfitFalls=="raise":
                        self.sellPrice /= 1 + common.jump
                        print("entrepreur # ", self.number, \
                        "lowering back the sell price")
                     if self.priceSwitchIfProfitFalls=="lower":
                        self.sellPrice *= 1 + common.jump
                        print("entrepreur # ", self.number, \
                        "raising back the sell price")

          return

        # here in error
        print("Using the 'quasi' option in hayekian market:\n",\
              "the",common.quasiHchoice, "value is not one of the\n",
              "valid option (unsold, randomUp, profit)")
        os.sys.exit(1)


    # all acting as consumers on the market place
    def actOnMarketPlace(self):
        if common.cycle < common.startHayekianMarket: return

        # in each sub step, we show residual consumption and production; the
        # code operates on different agents, but consistently (in each call,
        # the elaboration jumps from an instance of agent to another one)
        if common.checkResConsUnsoldProd:

         #print(self.number)
         if common.withinASubstep:
            common.internalSubStepAgentCounter+=1
            #print('*',common.internalSubStepAgentCounter)
            if common.internalSubStepAgentCounter==len(self.agentList):
                common.withinASubstep=False

         else: # not withinASubstep
            common.withinASubstep=True
            common.internalSubStepAgentCounter=1
            if common.currentCycle != common.cycle:
                  common.currentCycle = common.cycle
                  common.subStepCounter=0
                  common.readySellerList=False
                  print()
            common.subStepCounter+=1
            residualConsumptionCapabilityInValue=0
            residualUnsoldProduction=0
            for anAgent in self.agentList:
                residualConsumptionCapabilityInValue += anAgent.consumption
                if anAgent.agType=="entrepreneurs":
                    residualUnsoldProduction+= \
                    anAgent.production - anAgent.soldProduction
            print(\
"subc. %2d.%3d starts with cons. capab. (v) %.1f and uns. p. (q) %.1f"\
% (common.cycle, common.subStepCounter, residualConsumptionCapabilityInValue,\
                                        residualUnsoldProduction))



        try: common.wr.writerow
        except:
            print("The file firstStepOutputInHayekianMarket.csv was not"+\
                  " created in mActions.py")
            os.sys.exit(1)


        # first call in each cycle, preparing action (only once per cycle)
        #if self.currentCycle != common.cycle:
        if not common.readySellerList:
               #self.currentCycle = common.cycle

           common.readySellerList=True
           # we check that the planning of the consumption has been
           # made for the current cycle
           if self.consumptionPlanningInCycleNumber != common.cycle:
               print('Attempt of using actOnMarketPlace method before'+\
                     ' consumption planning')
               os.sys.exit(1) # to stop the execution, in the calling module
                           # we have multiple except, with 'SystemExit' case

           # create a temporary list of sellers, starting each step (cycle)
           common.sellerList=[]
           for anAg in self.agentList:
               if anAg.getType() == "entrepreneurs":
                   if not anAg.sellPriceDefined:
                       print("Inconsistent situation, an active selles"\
                       +" has no sell price defined.")
                       os.sys.exit(1)
                   else: common.sellerList.append(anAg)


        # acting (NB self.consumption comes from planConsumptionInValueV6)
        # if buying action is possible
        #print("cycle",common.cycle,"ag",self.number,"cons val",self.consumption)

        if self.consumption > 0:
          if common.sellerList != []:
            # chose a seller
            mySeller=common.sellerList[randint(0,len(common.sellerList)-1)]
            sellerQ=mySeller.production - mySeller.soldProduction
            if sellerQ>0:
              # try a deal
              if self.buyPrice <  mySeller.sellPrice:
                 self.statusB=mySeller.statusS=-1
              if self.buyPrice >= mySeller.sellPrice:
                 self.statusB=mySeller.statusS= 1

                 #print(common.cycle,"entr.",mySeller.number,\
                 #  mySeller.production,mySeller.soldProduction,\
                 #  mySeller.sellPrice)

                 # NB production can be < plannedProduction due to lack of workers

                 # consumption in value cannot exceed self.maxConsumptionInAStep
                 buyerQ=min(self.consumption/mySeller.sellPrice, sellerQ,\
                            self.maxConsumptionInAStep/mySeller.sellPrice)

                 mySeller.soldProduction+=buyerQ
                 mySeller.revenue+=buyerQ*mySeller.sellPrice
                 self.consumption-=buyerQ*mySeller.sellPrice
                 self.unspentConsumptionCapability=self.consumption
                 #print("cycle",common.cycle,"ag",self.number,"deal: cons val",\
                 #        buyerQ*mySeller.sellPrice,"price",mySeller.sellPrice)
                 # saving the price of the transaction
                 common.hayekianMarketTransactionPriceList_inACycle.\
                        append(mySeller.sellPrice)

                 common.totalConsumptionInQuantityInA_TimeStep += buyerQ


            #ouput -  seller has no goods to sell
            elif common.cycle==common.startHayekianMarket:
                     common.wr.writerow\
                     (["nogoods", "buy", numpy.nan, self.consumption, self.number,\
                     "sell", numpy.nan,mySeller.number])

            #output - deal vs. nodeal
            if common.cycle==common.startHayekianMarket:
                if mySeller.statusS==1:
                    common.wr.writerow\
                    (["deal", "buy", self.buyPrice, self.consumption, self.number,\
                    "sell", mySeller.sellPrice,mySeller.number])
                if mySeller.statusS==-1 and mySeller.sellPriceDefined:
                    common.wr.writerow\
                    (["nodeal", "buy", self.buyPrice, self.consumption, self.number,\
                    "sell", mySeller.sellPrice,mySeller.number])


            # correct running prices

            # if the status is != 0 the agent has already been acting
            if self.statusB == 1:  # buyer case (statusB 1, successful buy attempt,
                               # acting mostly to decrease the reservation price)
              self.buyPrice = applyRationallyTheRateOfChange(self.buyPrice,\
                                  uniform(-(1-common.runningShiftB)* \
                                        common.runningShockB, \
                                        common.runningShiftB* \
                                        common.runningShockB))

            if self.statusB == -1: # buyer case (statusB -1, unsuccessful buy attempt,
                               # acting mostly to increase the reservation price)
              self.buyPrice = applyRationallyTheRateOfChange(self.buyPrice,\
                                  uniform(-common.runningShiftB* \
                                        common.runningShockB, \
                                        (1-common.runningShiftB)* \
                                        common.runningShockB))

            if mySeller.statusS == 1 and common.hParadigm=="full" or \
                                     (common.hParadigm=="quasi" and \
                                     common.cycle==common.startHayekianMarket):
                               # seller case (statusS 1, successful sell attempt,
              mySeller.sellPrice = applyRationallyTheRateOfChange(mySeller.sellPrice,\
                                       common.ratioSellersBuyers*\
                                       uniform(-common.runningShiftS* \
                                        common.runningShockS,
                                        (1-common.runningShiftS)* \
                                        common.runningShockS))

            if mySeller.statusS == -1 and common.hParadigm=="full" or \
                                     (common.hParadigm=="quasi" and \
                                     common.cycle==common.startHayekianMarket):
                               # seller case (statusS -1, unsuccess. s. attempt,
                               # acting mostly to decrease the reservation price)
              mySeller.sellPrice = applyRationallyTheRateOfChange(mySeller.sellPrice,\
                                       common.ratioSellersBuyers*\
                                       uniform(-(1-common.runningShiftS)* \
                                        common.runningShockS, \
                                        common.runningShiftS* \
                                        common.runningShockS))

            #print("ag.", self.number, "new prices", self.buyPrice, mySeller.sellPrice)

            # cleaning the situation (redundant)\\
            self.statusB=mySeller.statusS=0

          #output - common.sellerList==[]
          elif common.cycle==common.startHayekianMarket:
               common.wr.writerow\
                (["nosellers", "buy", self.buyPrice, self.consumption, self.number,\
                "sell", numpy.nan,numpy.nan])

        #output - self.consumption<=0
        elif common.cycle==common.startHayekianMarket:
             common.wr.writerow\
               (["noconsumption", "buy", numpy.nan, self.consumption, self.number,\
               "sell", numpy.nan,numpy.nan])

        #output close
        if common.cycle==common.startHayekianMarket+1 and not common.closed:
            common.csvf.close()
            common.closed=True


    # calculateProfit V0
    def evaluateProfitV0(self):

        # this is an entrepreneur action
        if self.agType == "workers":
            return

        # the number of producing workers is obtained indirectly via
        # production/laborProductivity
        # print self.production/common.laborProductivity
        self.profit = (self.production / common.laborProductivity) * \
            (common.revenuesOfSalesForEachWorker -
             common.wage) + gauss(0, 0.05)

        # calculateProfit
    def evaluateProfit(self):

        # this is an entrepreneur action
        if self.agType == "workers":
            return

        # backward compatibily to version 1
        try:
            XC = common.newEntrantExtraCosts
        except BaseException:
            XC = 0
        try:
            k = self.extraCostsResidualDuration
        except BaseException:
            k = 0

        if k == 0:
            XC = 0
        if k > 0:
            self.extraCostsResidualDuration -= 1

        # the number of pruducing workers is obtained indirectly via
        # production/laborProductivity
        # print self.production/common.laborProductivity
        self.costs = common.wage * \
            (self.production / common.laborProductivity) + XC

        # the entrepreur sells her production, which is contributing - via
        # totalActualProductionInA_TimeStep, to price formation
        self.profit = common.price * self.production - self.costs

        common.totalProfit += self.profit

        # calculateProfit
    def evaluateProfitV5(self):

        # this is an entrepreneur action
        if self.agType == "workers":
            return

        # backward compatibily to version 1
        try:
            XC = common.newEntrantExtraCosts
        except BaseException:
            XC = 0
        try:
            k = self.extraCostsResidualDuration
        except BaseException:
            k = 0

        if k == 0:
            XC = 0
        if k > 0:
            self.extraCostsResidualDuration -= 1

        # the number of pruducing workers is obtained indirectly via
        # production/laborProductivity
        # print self.production/common.laborProductivity

        # how many workers, not via productvity due to possible troubles
        # in production

        laborForce = gvf.nx.degree(common.g, nbunch=self) + \
            1  # +1 to account for the entrepreneur herself

        # the followin if/else structure is for control reasons because if
        # not common.wageCutForWorkTroubles we do not take in account
        # self.workTroubles also if != 0; if = 0 is non relevant in any case
        if common.wageCutForWorkTroubles:
            self.costs = (common.wage - self.hasTroubles) \
                * (laborForce - 1) \
                + common.wage * 1 +  \
                XC
            # above, common.wage * 1 is for the entrepreur herself

        else:
            self.costs = common.wage * laborForce + \
                XC
        # print "I'm entrepreur", self.number, "costs are",self.costs

        # penalty Value
        pv = 0
        if self.hasTroubles > 0:
            pv = common.penaltyValue

        # the entrepreur sells her production, which is contributing - via
        # totalActualProductionInA_TimeStep, to price formation
        self.profit = common.price * (1. - pv) * self.production - self.costs
        print("I'm entrepreur", self.number, "my price is ",
              common.price * (1. - pv))


        # individual data collection
        # creating the dataframe

        try:
            common.firm_df
        except BaseException:
            common.firm_df = pd.DataFrame(
                    columns=[
                        'production',
                        'profit'])
            print("\nCreation of fhe dataframe of the firms (individual data)\n")

        firm_df2 = pd.DataFrame([[self.production, self.profit]],
                           columns=['production', 'profit'])
        common.firm_df = common.firm_df.append(firm_df2, ignore_index=True)


        common.totalProfit += self.profit

    # calculateProfit
    def evaluateProfitV6(self):

        # this is an entrepreneur action
        if self.agType == "workers":
            return

        # backward compatibily to version 1
        try:
            XC = common.newEntrantExtraCosts
        except BaseException:
            XC = 0
        try:
            k = self.extraCostsResidualDuration
        except BaseException:
            k = 0

        if k == 0:
            XC = 0
        if k > 0:
            self.extraCostsResidualDuration -= 1

        # the number of pruducing workers is obtained indirectly via
        # production/laborProductivity
        # print self.production/common.laborProductivity

        # how many workers, not via productvity due to possible troubles
        # in production

        laborForce = gvf.nx.degree(common.g, nbunch=self) + \
            1  # +1 to account for the entrepreneur herself

        # the followin if/else structure is for control reasons because if
        # not common.wageCutForWorkTroubles we do not take in account
        # self.workTroubles also if != 0; if = 0 is non relevant in any case
        if common.wageCutForWorkTroubles:
            self.costs = (common.wage - self.hasTroubles) \
                * (laborForce - 1) \
                + common.wage * 1 +  \
                XC
            # above, common.wage * 1 is for the entrepreur herself

        else:
            self.costs = common.wage * laborForce + \
                XC
        # print "I'm entrepreur", self.number, "costs are",self.costs

        # penalty Value
        pv = 0
        if self.hasTroubles > 0:
            pv = common.penaltyValue

        # V6 - before hayekian phase
        if common.cycle < common.startHayekianMarket:
           # the entrepreur sells her production, which is contributing - via
           # totalActualProductionInA_TimeStep, to price formation
           self.profit = common.price * (1. - pv) * self.production - self.costs
           print("I'm entrepreur", self.number, "my price is ",
              common.price * (1. - pv))

        # V6 - into the hayekian phase
        else:
           self.profit = self.revenue - self.costs
           print("I'm entrepreur", self.number, "my individual price is ",
              self.sellPrice)


        # individual data collection
        # creating the dataframe

        try:
            common.firm_df
        except BaseException:
            common.firm_df = pd.DataFrame(
                    columns=[
                        'production',
                        'profit'])
            print("\nCreation of fhe dataframe of the firms (individual data)\n")


        firm_df2 = pd.DataFrame([[self.production, self.profit]],
                           columns=['production', 'profit'])
        common.firm_df = common.firm_df.append(firm_df2, ignore_index=True)


        common.totalProfit += self.profit

    # consumptions
    def planConsumptionInValue(self):
        self.consumption = 0
        #case (1)
        # Y1=profit(t-1)+wage NB no negative consumption if profit(t-1) < 0
        # this is an entrepreneur action
        if self.agType == "entrepreneurs":
            self.consumption = common.a1 + \
                common.b1 * (self.profit + common.wage) + \
                gauss(0, common.consumptionRandomComponentSD)
            if self.consumption < 0:
                self.consumption = 0
            # profit, in V2, is at time -1 due to the sequence in schedule2.xls

        #case (2)
        # Y2=wage
        if self.agType == "workers" and self.employed:
            self.consumption = common.a2 + \
                common.b2 * common.wage + \
                gauss(0, common.consumptionRandomComponentSD)

        #case (3)
        # Y3=socialWelfareCompensation
        if self.agType == "workers" and not self.employed:
            self.consumption = common.a3 + \
                common.b3 * common.socialWelfareCompensation + \
                gauss(0, common.consumptionRandomComponentSD)

        # update totalPlannedConsumptionInValueInA_TimeStep
        common.totalPlannedConsumptionInValueInA_TimeStep += self.consumption
        # print "C sum", common.totalPlannedConsumptionInValueInA_TimeStep

    # consumptions
    def planConsumptionInValueV5(self):
        self.consumption = 0
        #case (1)
        # Y1=profit(t-1)+wage NB no negative consumption if profit(t-1) < 0
        # this is an entrepreneur action
        if self.agType == "entrepreneurs":
            self.consumption = common.a1 + \
                common.b1 * (self.profit + common.wage) + \
                gauss(0, common.consumptionRandomComponentSD)
            if self.consumption < 0:
                self.consumption = 0
            # profit, in V2, is at time -1 due to the sequence in schedule2.xls

        #case (2)
        # Y2=wage
        if self.agType == "workers" and self.employed:
            # the followin if/else structure is for control reasons because if
            # not common.wageCutForWorkTroubles we do not take in account
            # self.workTroubles also if != 0; if = 0 is non relevant in any
            # case
            if common.wageCutForWorkTroubles:
                self.consumption = common.a2 + \
                    common.b2 * common.wage * (1. - self.workTroubles) + \
                    gauss(0, common.consumptionRandomComponentSD)
                # print "worker", self.number, "wage x",(1.-self.workTroubles)
            else:
                self.consumption = common.a2 + \
                    common.b2 * common.wage + \
                    gauss(0, common.consumptionRandomComponentSD)

        #case (3)
        # Y3=socialWelfareCompensation
        if self.agType == "workers" and not self.employed:
            self.consumption = common.a3 + \
                common.b3 * common.socialWelfareCompensation + \
                gauss(0, common.consumptionRandomComponentSD)

        # update totalPlannedConsumptionInValueInA_TimeStep
        common.totalPlannedConsumptionInValueInA_TimeStep += self.consumption
        # print "C sum", common.totalPlannedConsumptionInValueInA_TimeStep

        self.consumptionPlanningInCycleNumber=common.cycle

    # consumptions
    def planConsumptionInValueV6(self):
        self.consumption = 0
        #case (1)
        # Y1=profit(t-1)+wage NB no negative consumption if profit(t-1) < 0
        # this is an entrepreneur action
        if self.agType == "entrepreneurs":
            self.consumption = common.a1 + \
                common.b1 * (self.profit + common.wage) + \
                gauss(0, common.consumptionRandomComponentSD)
            if self.consumption < 0:
                self.consumption = 0
            # profit, in V2, is at time -1 due to the sequence in schedule2.xls

        #case (2)
        # Y2=wage
        if self.agType == "workers" and self.employed:
            # the followin if/else structure is for control reasons because if
            # not common.wageCutForWorkTroubles we do not take in account
            # self.workTroubles also if != 0; if = 0 is non relevant in any
            # case
            if common.wageCutForWorkTroubles:
                self.consumption = common.a2 + \
                    common.b2 * common.wage * (1. - self.workTroubles) + \
                    gauss(0, common.consumptionRandomComponentSD)
                # print "worker", self.number, "wage x",(1.-self.workTroubles)
            else:
                self.consumption = common.a2 + \
                    common.b2 * common.wage + \
                    gauss(0, common.consumptionRandomComponentSD)

        #case (3)
        # Y3=socialWelfareCompensation
        if self.agType == "workers" and not self.employed:
            self.consumption = common.a3 + \
                common.b3 * common.socialWelfareCompensation + \
                gauss(0, common.consumptionRandomComponentSD)

        # reuse unspent consumption capability
        #if self.number==1:
        #    print("reuse unspent consumption capability", \
        #                            self.unspentConsumptionCapability)
        self.consumption += common.reUseUnspentConsumptionCapability * \
                            self.unspentConsumptionCapability

        if self.consumption < 0:
            #print('*************************************',self.employed, \
            #        self.consumption)
            self.consumption=0


        # max cons. in each step of a cycles of the hayekian phase
        self.maxConsumptionInAStep=self.consumption*common.consumptionQuota

        # update totalPlannedConsumptionInValueInA_TimeStep
        if common.cycle < common.startHayekianMarket or \
           (common.cycle == common.startHayekianMarket and \
           common.startHayekianMarket == 1):
           # the 'or' condition is necessary In the hayekian perspective,
           # when the start is a cyce 1; the value of
           # common.totalPlannedConsumptionInValueInA_TimeStep is necessary
           # in the warming phase: look at the 'else' within
           # the second block in setInitialPricesHM

           common.totalPlannedConsumptionInValueInA_TimeStep += self.consumption
           # print "C sum", common.totalPlannedConsumptionInValueInA_TimeStep

        self.consumptionPlanningInCycleNumber=common.cycle

    # to entrepreneur
    def toEntrepreneur(self):
        if self.agType != "workers" or not self.employed:
            return

        #myEntrepreneur = gvf.nx.neighbors(common.g, self)[0] with nx 2.0
        myEntrepreneur = list(common.g.neighbors(self))[0]
        myEntrepreneurProfit = myEntrepreneur.profit
        if myEntrepreneurProfit >= common.thresholdToEntrepreneur:
            print("I'm worker %2.0f and myEntrepreneurProfit is %4.2f" %
                  (self.number, myEntrepreneurProfit))
            common.g.remove_edge(myEntrepreneur, self)

            # originally, it was a worker
            if self.xPos > 0:
                gvf.pos[self] = (self.xPos - 15, self.yPos)
            # originally, it was an entrepreneur
            else:
                gvf.pos[self] = (self.xPos, self.yPos)
            # colors at http://www.w3schools.com/html/html_colornames.asp
            gvf.colors[self] = "LawnGreen"
            self.agType = "entrepreneurs"
            self.employed = True
            self.extraCostsResidualDuration = common.extraCostsDuration

    # to entrepreneurV3
    def toEntrepreneurV3(self):
        if self.agType != "workers" or not self.employed:
            return
        # print float(common.absoluteBarrierToBecomeEntrepreneur)/ \
        #               len(self.agentList)
        if random() <= float(common.absoluteBarrierToBecomeEntrepreneur) / \
                len(self.agentList):
            #myEntrepreneur = gvf.nx.neighbors(common.g, self)[0] with nx 2.0
            myEntrepreneur = list(common.g.neighbors(self))[0]
            myEntrepreneurProfit = myEntrepreneur.profit
            myEntrepreneurCosts = myEntrepreneur.costs
            if myEntrepreneurProfit / myEntrepreneurCosts >= \
                    common.thresholdToEntrepreneur:
                print(
                    "Worker %2.0f is now an entrepreneur (previous firm relative profit %4.2f)" %
                    (self.number, myEntrepreneurProfit / myEntrepreneurCosts))
                common.g.remove_edge(myEntrepreneur, self)

                # originally, it was a worker
                if self.xPos > 0:
                    gvf.pos[self] = (self.xPos - 15, self.yPos)
                # originally, it was an entrepreneur
                else:
                    gvf.pos[self] = (self.xPos, self.yPos)
                # colors at http://www.w3schools.com/html/html_colornames.asp
                gvf.colors[self] = "LawnGreen"
                self.agType = "entrepreneurs"
                self.employed = True
                self.extraCostsResidualDuration = common.extraCostsDuration


    # to entrepreneurV6
    def toEntrepreneurV6(self):
        if self.agType != "workers" or not self.employed:
            return
        # print float(common.absoluteBarrierToBecomeEntrepreneur)/ \
        #               len(self.agentList)
        if random() <= float(common.absoluteBarrierToBecomeEntrepreneur) / \
                len(self.agentList):
            #myEntrepreneur = gvf.nx.neighbors(common.g, self)[0] with nx 2.0
            myEntrepreneur = list(common.g.neighbors(self))[0]
            myEntrepreneurProfit = myEntrepreneur.profit
            myEntrepreneurCosts = myEntrepreneur.costs
            if myEntrepreneurProfit / myEntrepreneurCosts >= \
                    common.thresholdToEntrepreneur:
                print(
                    "Worker %2.0f is now an entrepreneur (previous firm relative profit %4.2f)" %
                    (self.number, myEntrepreneurProfit / myEntrepreneurCosts))
                common.g.remove_edge(myEntrepreneur, self)

                # originally, it was a worker
                if self.xPos > 0:
                    gvf.pos[self] = (self.xPos - 15, self.yPos)
                # originally, it was an entrepreneur
                else:
                    gvf.pos[self] = (self.xPos, self.yPos)
                # colors at http://www.w3schools.com/html/html_colornames.asp
                gvf.colors[self] = "LawnGreen"
                self.agType = "entrepreneurs"
                self.employed = True
                self.extraCostsResidualDuration = common.extraCostsDuration

                if common.cycle >=common.startHayekianMarket:
                  if myEntrepreneur.sellPriceDefined:
                    self.sellPrice=myEntrepreneur.sellPrice
                    self.jump=myEntrepreneur.jump
                    print("with the same sell price of the the previous firm",\
                          self.sellPrice)
                    self.profitStrategyReverseAfterN=\
                                     myEntrepreneur.profitStrategyReverseAfterN
                    self.priceSwitchIfProfitFalls=\
                                     myEntrepreneur.priceSwitchIfProfitFalls
                  else:
                    print("New entrepreneur cannot copy the price of previous firm")
                    os.sys.exit(1)


    # to workers
    def toWorker(self):
        if self.agType != "entrepreneurs":
            return

        if self.profit <= common.thresholdToWorker:
            print("I'm entrepreneur %2.0f and my profit is %4.2f" %
                  (self.number, self.profit))

            # the list of the employees of the firm, IF ANY
            #entrepreneurWorkers = gvf.nx.neighbors(common.g, self) with nx 2.0
            entrepreneurWorkers = list(common.g.neighbors(self))
            print("entrepreneur", self.number, "has",
                   len(entrepreneurWorkers),
                  "workers to be fired")

            if len(entrepreneurWorkers) > 0:
                for aWorker in entrepreneurWorkers:
                    gvf.colors[aWorker] = "OrangeRed"
                    aWorker.employed = False

                    common.g.remove_edge(self, aWorker)

            self.numOfWorkers = 0

            # originally, it was an entrepreneur
            if self.xPos < 0:
                gvf.pos[self] = (self.xPos + 15, self.yPos)
            # originally, it was a worker
            else:
                gvf.pos[self] = (self.xPos, self.yPos)
            # colors at http://www.w3schools.com/html/html_colornames.asp
            gvf.colors[self] = "OrangeRed"
            self.agType = "workers"
            self.employed = False

    # to workersV3
    def toWorkerV3(self):
        if self.agType != "entrepreneurs":
            return

        # check for newborn firms
        try:
            self.costs
        except BaseException:
            return

        if self.profit / self.costs <= common.thresholdToWorker:
            print("I'm entrepreneur %2.0f and my relative profit is %4.2f" %
                  (self.number, self.profit / self.costs))

            # the list of the employees of the firm, IF ANY
            #entrepreneurWorkers = gvf.nx.neighbors(common.g, self) with nx 2.0
            entrepreneurWorkers = list(common.g.neighbors(self))
            print("entrepreneur", self.number, "has",
                  len(entrepreneurWorkers),
                  "workers to be fired")

            if len(entrepreneurWorkers) > 0:
                for aWorker in entrepreneurWorkers:
                    gvf.colors[aWorker] = "OrangeRed"
                    aWorker.employed = False

                    common.g.remove_edge(self, aWorker)

            self.numOfWorkers = 0

            # originally, it was an entrepreneur
            if self.xPos < 0:
                gvf.pos[self] = (self.xPos + 15, self.yPos)
            # originally, it was a worker
            else:
                gvf.pos[self] = (self.xPos, self.yPos)
            # colors at http://www.w3schools.com/html/html_colornames.asp
            gvf.colors[self] = "OrangeRed"
            self.agType = "workers"
            self.employed = False

    # work troubles
    def workTroubles(self):

            # NB this method acts with the probability set in the schedule.txt
            # file
        if self.agType != "entrepreneurs":
            return

        # production shock due to work troubles

        psiShock = uniform(common.productionCorrectionPsi / 2,
                           common.productionCorrectionPsi)
        self.hasTroubles = psiShock
        print("Entrepreneur", self.number, "is suffering a reduction of "
              "production of", psiShock * 100, "%, due to work troubles")

        if common.wageCutForWorkTroubles:
            # the list of the employees of the firm
            #entrepreneurWorkers = gvf.nx.neighbors(common.g, self) with nx 2.0
            entrepreneurWorkers = list(common.g.neighbors(self))
            for aWorker in entrepreneurWorkers:
                # avoiding the entrepreneur herself, as we are refering to her
                # network of workers
                aWorker.workTroubles = psiShock
                # print "Worker ", aWorker.number, "is suffering a reduction of "\
                #      "wage of", psiShock*100, "%, due to work troubles"

    # get graph
    def getGraph(self):
        return common.g

    # get type
    def getType(self):
        return self.agType
