# parameters.py
from Tools import *
import commonVar as common

import networkx as nx
import matplotlib as mplt
import numpy.random as npr
import pandas as pd
from IPython import get_ipython
import pandas as pd


def loadParameters(self):

    # creating the dataframe of the paramenters
    try:
        common.str_df
    except BaseException:
        common.par_df = pd.DataFrame(columns=['Parameter names', 'Values'])
        print("\nCreation of fhe parameter dataframe\n")
        # print common.par_df

    # preliminary cntrol
    if common.graphicStatus == "PythonViaTerminal" and common.IPython:
        print("Please do not run the 'oligopoly project' in IPython via a terminal.")
        os.sys.exit(1)

    print('Warning: if running in "jupyter console" the graphic output is missing."')

    print("NetworkX version %s running" % nx.__version__)
    print("matplotlib version %s running" % mplt.__version__)
    print("pandas version %s running\n" % pd.__version__)

    nxv = nx.__version__
    vOK = checkVersion(nxv, 'NetworkX', 1, 9, 1)

    if not vOK:
        print("NetworkX 1.9.1 or greater required")
        os.sys.exit(1)

    mpltv = mplt.__version__
    vOK = checkVersion(mpltv, 'Matplotlib', 1, 5, 1)

    if not vOK:
        print("Matplotlib 1.5.1 or greater required")
        os.sys.exit(1)

    pdv = pd.__version__.split('.')
    vOK = False
    if int(pdv[0]) > 0:
        vOK = True
    if len(pdv) >= 1:
        if int(pdv[0]) == 0 and int(pdv[1]) > 18:
            vOK = True
    if len(pdv) >= 3:
        if int(pdv[0]) == 0 and int(pdv[1]) == 18 and int(pdv[2]) >= 1:
            vOK = True

    if not vOK:
        print("pandas 0.18.1 or greater required")
        os.sys.exit(1)

    # sigma of the normal distribution used in randomize the position of the
    # agents/nodes
    print(
        "sigma of the normal distribution used in randomizing the position of the agents/nodes ",
        common.sigma)

    mySeed = eval(input("random number seed (1 to get it from the clock) "))
    if mySeed == 1:
        random.seed()
        npr.seed()
    else:
        random.seed(mySeed)
        npr.seed(mySeed)

    self.nAgents = 0
    print("No 'bland' agents")

    #self.worldXSize= input("X size of the world? ")
    self.worldXSize = 1
    # print "X size of the world not relevant"

    #self.worldYSize= input("Y size of the world? ")
    self.worldYSize = 1
    # print "y size of the world not relevant"

    # Projct version and thresholds
    try:
        projectVersion = str(common.projectVersion)
    except BaseException:
        projectVersion = "Unknown"
    try:
        build = str(common.build)
    except BaseException:
        build = "Unknown"
    print(
        "\nProject version " +
        projectVersion,
        "build",
        build,
        "\nhiringThreshold",
        common.hiringThreshold,
        "firingThreshold",
        common.firingThreshold)
    dataFrameAppend("project version", projectVersion)  # saving pars
    dataFrameAppend("build", build)  # saving pars
    dataFrameAppend("seed (1 gets it from the clock)", mySeed)  # saving pars
    # wages
    print("wage base", common.wage)
    dataFrameAppend("wage base", common.wage)  # saving pars

    # social welfare compensation
    print("social welfare compensation", common.socialWelfareCompensation)
    dataFrameAppend("social welfare compensation",
                    common.socialWelfareCompensation)  # saving pars

    # revenue of sales per worker (version 0)
    # print "revenues of sales for each worker in Version 0", \
    #      common.revenuesOfSalesForEachWorker

    # laboor productivity
    print("labor productivity", common.laborProductivity)
    dataFrameAppend(
        "labor productivity",
        common.laborProductivity)  # saving pars

    # Poisson mean in plannedProduction
    if common.projectVersion < "3":
        print(
            "Mean value of the Poisson distribution used in production planning " +
            "(not used in V.0; used only at t=1 in V.3);")
        tmp = input(
            "suggested nu=5 (enter to confirm or input a number) ")
        try:
            common.nu = int(tmp)
        except BaseException:
            pass
        print("Resulting value", common.nu)
    if common.projectVersion >= "3":

        print(
            "nu, mean value of the Poisson distribution used in production\n" +
            "planning at time=1, is set internally to match the ratio\n" +
            "between actual and potential initial employed population,")
        print("set to %3.2f" % common.rho)
        dataFrameAppend(
            "expected employment ratio at t=1",
            common.rho)  # saving pars

    # consumption
    print()
    print("consumption behavior with Ci = ai + bi Yi + u\n" +
          "u = N(0,%5.3f)" % common.consumptionRandomComponentSD)
    print(("(1) entrepreneurs as consumers with a1 = %4.2f b1 = %4.2f Y1 = profit(t-1)+wage\n" +
           "(2) employed workers           with a2 = %4.2f b2 = %4.2f Y2 = wage\n" +
           "(3) unemployed workers         with a3 = %4.2f b3 = %4.2f Y3 = socialWelfareCompensation") %
          (common.a1, common.b1, common.a2, common.b2, common.a3, common.b3))
    print()
    dataFrameAppend("consumption behavior: a1", common.a1)  # saving pars
    dataFrameAppend("consumption behavior: b1", common.b1)  # saving pars
    dataFrameAppend("consumption behavior: a2", common.a2)  # saving pars
    dataFrameAppend("consumption behavior: b2", common.b2)  # saving pars
    dataFrameAppend("consumption behavior: a3", common.a3)  # saving pars
    dataFrameAppend("consumption behavior: b3", common.b3)  # saving pars

    print("consumption random component (SD)",
          common.consumptionRandomComponentSD)
    dataFrameAppend("consumption random component (SD)",
                    common.consumptionRandomComponentSD)  # saving pars

    print(("Relative threshold to become an entrepreneur %4.2f\n" +
           "with new entrant extra costs %4.2f and duration of the extra costs %d") %
          (common.thresholdToEntrepreneur, common.newEntrantExtraCosts,
           common.extraCostsDuration))
    dataFrameAppend("relative threshold to become an entrepreneur",
                    common.thresholdToEntrepreneur)  # saving pars
    dataFrameAppend("new entrant extra costs",
                    common.newEntrantExtraCosts)  # saving pars
    dataFrameAppend("duration (# of cycles) of the extra costs",
                    common.extraCostsDuration)  # saving pars

    print("Random component of planned production, uniformly distributed between %4.2f%s and %4.2f%s" %
          (-common.randomComponentOfPlannedProduction * 100, "%",
           common.randomComponentOfPlannedProduction * 100, "%"))
    dataFrameAppend("min random rel. component of planned production",
                    -common.randomComponentOfPlannedProduction)  # saving pars
    dataFrameAppend("max random rel. component of planned production",
                    common.randomComponentOfPlannedProduction)  # saving pars

    print(
        "Absolute barrier to become entrepreneur, max number in a time step: ",
        common.absoluteBarrierToBecomeEntrepreneur)
    dataFrameAppend("max new entrant number in a time step",
                    common.absoluteBarrierToBecomeEntrepreneur)  # saving pars

    print(
        "\nRelative threshold to lose the entrepreneur status (becoming a unemployed worker) %4.2f\n" %
        common.thresholdToWorker)
    dataFrameAppend("relative threshold from entrepreneur to unempl.",
                    common.thresholdToWorker)  # saving pars

    print(
        "Total demand relative random shock, uniformly distributed\nbetween " +
        "-%4.2f%s and +%4.2f%s" %
        (common.maxDemandRelativeRandomShock *
         100,
         "%",
         common.maxDemandRelativeRandomShock *
         100,
         "%"))
    dataFrameAppend("min of uniform demand relative random shock",
                    -common.maxDemandRelativeRandomShock)  # saving pars
    dataFrameAppend("max of uniform demand relative random shock",
                    common.maxDemandRelativeRandomShock)  # saving pars

    print("Node numbers in graph:", common.nodeNumbersInGraph)

    print("Full employment threshold " +
          "%4.2f%s and wage step up in full employment %4.2f%s"
          % (common.fullEmploymentThreshold * 100, "%",
             common.wageStepInFullEmployment * 100, "%"))
    dataFrameAppend("full employment threshold",
                    common.fullEmploymentThreshold)  # saving pars
    dataFrameAppend("wage step up in full employment",
                    common.wageStepInFullEmployment)  # saving pars

    print(
        "Wage relative increment as an entry barrier: " +
        "%4.2f%s; trigger level (relative increment of oligopolistic firms): %4.2f%s" %
        (common.temporaryRelativeWageIncrementAsBarrier *
         100,
         "%",
         common.maxAcceptableOligopolistRelativeIncrement *
         100,
         "%"))
    dataFrameAppend("wage relative increment as an entry barrier",
                    common.temporaryRelativeWageIncrementAsBarrier)  # saving pars
    dataFrameAppend(
        "trigger level (relative increment of olig. firms)",
        common.maxAcceptableOligopolistRelativeIncrement)  # saving par

    print("Production correction (lost production) due to work troubles " +
          "between %4.2f%s and %4.2f%s, if any."
          % (common.productionCorrectionPsi * 100 / 2., "%",
             common.productionCorrectionPsi * 100, "%"))
    print("The correction acts with the probability indicate in the " +
          "file schedule.xls for the method 'workTroubles'")
    print("Is it applied also to the wages of the worker of the firm? ",
          common.wageCutForWorkTroubles)
    print("Price penalty for the firms suffering work troubles %4.2f%s" %
          (common.penaltyValue * 100, "%"))
    dataFrameAppend("min lost production due to work troubles",
                    common.productionCorrectionPsi / 2.)  # saving pars
    dataFrameAppend("max lost production due to work troubles",
                    common.productionCorrectionPsi)  # saving pars
    dataFrameAppend("probability of work troubles, see below",
                    "-")  # saving par
    if common.wageCutForWorkTroubles:
        dataFrameAppend("cut also the wages", "yes")  # saving pars
    else:
        dataFrameAppend("cut also the wages", "no")  # saving pars
    dataFrameAppend("price penalty for the firms if work troubles",
                    common.penaltyValue)  # saving par

    # cycles
    self.nCycles = eval(input("How many cycles? (0 = exit) "))

    dataFrameAppend("# of cycles", self.nCycles)  # saving par

    v = input("verbose? (y/[n]) ")
    if v == "y" or v == "Y":
        common.verbose = True  # predefined False
    print("If running in IPython, the messages of the model about che creation" +
          "\nof each agent are automatically off, to avoid locking the run.")


def dataFrameAppend(name, value):
    par_df2 = pd.DataFrame([[name, value]],
                           columns=['Parameter names', 'Values'])
    # print par_df2

    common.par_df = common.par_df.append(par_df2, ignore_index=True)
    # print common.par_df #warning: here the row index starts from 0
