# WorldState.py
from Tools import *
import commonVar as common


class WorldState(object):
    def __init__(self):
        # the environment
        print("World state has been created.")

    # set market price V1
    def setMarketPriceV1(self):
        # to have a price around 1
        common.price = 1.4 - 0.02 * common.totalProductionInA_TimeStep
        print("Set market price to ", common.price)
        common.price10 = common.price * 10  # to plot

    # set market price V2
    def setMarketPriceV2(self):
        common.price = common.totalPlannedConsumptionInValueInA_TimeStep / \
            common.totalProductionInA_TimeStep
        print("Set market price to ", common.price)

    # set market price V3
    def setMarketPriceV3(self):
        shock0 = random.uniform(-common.maxDemandRelativeRandomShock,
                                common.maxDemandRelativeRandomShock)
        shock = shock0

        print("\n-------------------------------------")

        if shock >= 0:
            common.totalDemandInPrevious_TimeStep = \
                common.totalPlannedConsumptionInValueInA_TimeStep * \
                (1 + shock)
            common.price = (common.totalPlannedConsumptionInValueInA_TimeStep *
                            (1 + shock))  \
                / common.totalProductionInA_TimeStep
            print("Relative shock (symmetric) ", shock0)
            print("Set market price to ", common.price)

        if shock < 0:
            shock *= -1.  # always positive, boing added to the denominator
            common.totalDemandInPrevious_TimeStep = \
                common.totalPlannedConsumptionInValueInA_TimeStep / \
                (1 + shock)
            common.price = (common.totalPlannedConsumptionInValueInA_TimeStep /
                            (1 + shock))  \
                / common.totalProductionInA_TimeStep
            print("Relative shock (symmetric) ", shock0)
            print("Set market price to ", common.price)

        print("-------------------------------------\n")

    # random shock to wages (temporary method to experiment with wages)
    def randomShockToWages(self):
        k = 0.10
        shock = random.uniform(-k, k)

        if shock >= 0:
            common.wage *= (1. + shock)

        if shock < 0:
            shock *= -1.
            common.wage /= (1. + shock)

    # shock to wages (full employment case)
    def fullEmploymentEffectOnWages(self):

        # wages: reset incumbent action if any
        if common.wageAddendum > 0:
            common.wage -= common.wageAddendum
            common.wageAddendum = 0

        # employed people
        peopleList = common.g.nodes()
        totalPeople = len(peopleList)
        totalEmployed = 0
        for p in peopleList:
            if p.employed:
                totalEmployed += 1
        # print totalPeople, totalEmployed
        unemploymentRate = 1. - float(totalEmployed) / \
            float(totalPeople)
        if not common.fullEmploymentStatus and \
           unemploymentRate <= common.fullEmploymentThreshold:
            common.wage *= (1 + common.wageStepInFullEmployment)
            common.fullEmploymentStatus = True

        if common.fullEmploymentStatus and \
           unemploymentRate > common.fullEmploymentThreshold:
            common.wage /= (1 + common.wageStepInFullEmployment)
            common.fullEmploymentStatus = False

    # incumbents rising wages as na entry barrier
    def incumbentActionOnWages(self):

        # current number of entrepreneurs
        peopleList = common.g.nodes()
        nEntrepreneurs = 0
        for p in peopleList:
            if p.agType == "entrepreneurs":
                nEntrepreneurs += 1
        nEntrepreneurs = float(nEntrepreneurs)

        # previous number of entrepreneurs
        nEntrepreneurs0 = common.str_df.iloc[-1, 0]  # indexes Python style

        # print nEntrepreneurs, nEntrepreneurs0

        # wages: reset incumbent action if any
        if common.wageAddendum > 0:
            common.wage -= common.wageAddendum
            common.wageAddendum = 0

        # wages: set
        if nEntrepreneurs / nEntrepreneurs0 - 1 > \
                common.maxAcceptableOligopolistRelativeIncrement:
            common.wageAddendum = common.wage *\
                common.temporaryRelativeWageIncrementAsBarrier
            common.wage += common.wageAddendum
