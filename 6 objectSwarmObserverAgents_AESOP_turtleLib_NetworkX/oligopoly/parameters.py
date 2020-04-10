# parameters.py
import myGauss
from Tools import *
import commonVar as common

import networkx as nx
import matplotlib as mplt
import numpy.random as npr
import pandas as pd
from IPython import get_ipython
import pandas as pd
import numpy as np
import sys

def fInput(label):
    x = ""
    while x=="" or " " in x:
        x = input(label)
        try: xR=eval(x) # "" case fails here
        except: x=""
    return xR


def loadParameters(self):

    # projectVersion version and build
    try:
        projectVersion = str(common.projectVersion)
    except BaseException:
        projectVersion = "Unknown"
    try:
        build = str(common.build)
    except BaseException:
        build = "Unknown"
    print(
        "\nProject Oligopoly: version " +
        projectVersion,
        "build",
        build,"\n")

    if sys.version_info[0] < 3:
        print("Python 3 required")
        os.sys.exit(1)

    # creating the dataframe of the paramenters
    try:
        common.str_df
    except BaseException:
        common.par_df = pd.DataFrame(columns=["Parameter internal names",\
                                              "Parameter definitions", "Values"])
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

    mySeed = fInput("random number seed (1 to get it from the clock) ")

    if mySeed == 1:
        random.seed()
        npr.seed()
    else:
        random.seed(mySeed)
        npr.seed(mySeed)

    common.mg=myGauss.myG()

    self.nAgents = 0
    print("No 'bland' agents")

    #self.worldXSize= input("X size of the world? ")
    self.worldXSize = 1
    # print "X size of the world not relevant"

    #self.worldYSize= input("Y size of the world? ")
    self.worldYSize = 1
    # print "y size of the world not relevant"

    # a few thresholds
    print(
        "\nhiringThreshold",
        common.hiringThreshold,
        "firingThreshold",
        common.firingThreshold)
    dataFrameAppend("projectVersion","project version", projectVersion)  # saving pars

    dataFrameAppend("build","build", build)  # saving pars
    dataFrameAppend("mySeed","seed (1 gets it from the clock)", mySeed)  # saving pars
    # wages
    print("wage base", common.wage)
    dataFrameAppend("wage","wage base", common.wage)  # saving pars

    # social welfare compensation
    print("social welfare compensation", common.socialWelfareCompensation)
    dataFrameAppend("socialWelfareCompensation","social welfare compensation",
                    common.socialWelfareCompensation)  # saving pars

    # social welfare compensation
    print("reuse unspent consumption capability [0, 1]", \
                                common.reUseUnspentConsumptionCapability)
    dataFrameAppend("reUseUnspentConsumptionCapability",\
                                "reuse unspent consumption capability [0, 1]",
                    common.reUseUnspentConsumptionCapability)  # saving pars

    # revenue of sales per worker (version 0)
    # print "revenues of sales for each worker in Version 0", \
    #      common.revenuesOfSalesForEachWorker

    # laboor productivity
    print("labor productivity", common.laborProductivity)
    dataFrameAppend("laborProductivity","labor productivity",
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
        dataFrameAppend("rho","expected employment ratio at t=1",
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
    dataFrameAppend("a1","consumption behavior: a1", common.a1)  # saving pars
    dataFrameAppend("b1","consumption behavior: b1", common.b1)  # saving pars
    dataFrameAppend("a2","consumption behavior: a2", common.a2)  # saving pars
    dataFrameAppend("b2","consumption behavior: b2", common.b2)  # saving pars
    dataFrameAppend("a3","consumption behavior: a3", common.a3)  # saving pars
    dataFrameAppend("b3","consumption behavior: b3", common.b3)  # saving pars

    print("consumption random component (SD)",
          common.consumptionRandomComponentSD)
    dataFrameAppend("consumptionRandomComponentSD",
                    "consumption random component (SD)",
                    common.consumptionRandomComponentSD)  # saving pars

    print(("Relative profit threshold to become an entrepreneur %4.2f\n" +
           "with new entrant extra costs %4.2f and duration of the extra costs %d") %
          (common.thresholdToEntrepreneur, common.newEntrantExtraCosts,
           common.extraCostsDuration))
    dataFrameAppend("thresholdToEntrepreneur",
                    "relative profit threshold to become an entrepreneur",
                    common.thresholdToEntrepreneur)  # saving pars
    dataFrameAppend("newEntrantExtraCosts","new entrant extra costs",
                    common.newEntrantExtraCosts)  # saving pars

    dataFrameAppend("extraCostsDuration","duration (# of cycles) of the extra costs",
                    common.extraCostsDuration)  # saving pars
    print("Random component of planned production, uniformly distributed between %4.2f%s and %4.2f%s" %
          (-common.randomComponentOfPlannedProduction * 100, "%",
           common.randomComponentOfPlannedProduction * 100, "%"))
    dataFrameAppend("randomComponentOfPlannedProduction",
                    "min(*-1)/max random rel. component of planned production",
                    common.randomComponentOfPlannedProduction)  # saving pars

    print(
        "Absolute barrier to become entrepreneur, max number in a time step: ",
        common.absoluteBarrierToBecomeEntrepreneur)
    dataFrameAppend("absoluteBarrierToBecomeEntrepreneur",
                    "max new entrant number in a time step",
                    common.absoluteBarrierToBecomeEntrepreneur)  # saving pars

    print(
        "\nRelative threshold to lose the entrepreneur status (becoming an unemployed worker) %4.2f\n" %
        common.thresholdToWorker)
    dataFrameAppend("thresholdToWorker",
                    "relative threshold from entrepreneur to unempl.",
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
    dataFrameAppend("maxDemandRelativeRandomShock",
                    "min(*-1)/max of uniform demand relative random shock",
                    common.maxDemandRelativeRandomShock)  # saving pars

    print("Node numbers in graph:", common.nodeNumbersInGraph)

    print("Full employment threshold " +
          "%4.2f%s and wage step up in full employment %4.2f%s"
          % (common.fullEmploymentThreshold * 100, "%",
             common.wageStepInFullEmployment * 100, "%"))
    dataFrameAppend("fullEmploymentThreshold","full employment threshold",
                    common.fullEmploymentThreshold)  # saving pars
    dataFrameAppend("wageStepInFullEmployment","wage step up in full employment",
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
    dataFrameAppend("temporaryRelativeWageIncrementAsBarrier",
                    "wage relative increment as an entry barrier",
                    common.temporaryRelativeWageIncrementAsBarrier)  # saving pars
    dataFrameAppend("maxAcceptableOligopolistRelativeIncrement",
                    "trigger level (relative increment of olig. firms)",
                    common.maxAcceptableOligopolistRelativeIncrement)  # saving par

    print(
        "\nMeasuring the new entrant number in a cumulative way %s\n" %
        common.cumulativelyMeasuringNewEntrantNumber)
    dataFrameAppend("cumulativelyMeasuringNewEntrantNumber",
                    "Measuring the new entrant number in a cumulative way",
                    common.cumulativelyMeasuringNewEntrantNumber)  # saving pars

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
    dataFrameAppend("productionCorrectionPsi",\
                    "min (val/2.) and max (val) lost production due to work troubles",
                    common.productionCorrectionPsi)  # saving pars

    dataFrameAppend("NaN", "probability of work troubles, see below",
                    np.NaN)  # saving par

    if common.wageCutForWorkTroubles:
        dataFrameAppend("wageCutForWorkTroubles",
                        "cut also the wages", "yes")  # saving pars
    else:
        dataFrameAppend("wageCutForWorkTroubles",
                        "cut also the wages", "no")  # saving pars

    dataFrameAppend("penaltyValue","price penalty for the firms if work troubles",
                    common.penaltyValue)  # saving par

    print("\nHayekian market starts at cycle = %3d\n" %
            common.startHayekianMarket)
    dataFrameAppend("startHayekianMarket",
                        "cycle to start the hayekian market",
                        common.startHayekianMarket)  # saving pars

    print("\ninfos on substep output management = %5s\n" %
            common.checkResConsUnsoldProd)
    dataFrameAppend("checkResConsUnsoldProd",
                        "infos on substep output management",
                        common.checkResConsUnsoldProd)  # saving pars


    print("\nhayekian market sell price modification = %10s\n" %
            common.hParadigm)
    dataFrameAppend("hParadigm",
                        "hayekian market sell price modification",
                        common.hParadigm)  # saving pars

    print("\nentrepreneurs mind if plannedProduction falls = %10s\n" %
            common.entrepreneursMindIfPlannedProductionFalls)
    dataFrameAppend("entrepreneursMindIfPlannedProductionFalls",
                        "entrepreneurs mind if plannedProduction falls",
                        common.entrepreneursMindIfPlannedProductionFalls)
                        # saving pars

    print("\nthreshold to decrease the price if total plannedP falls = %.2f\n" %
            common.thresholdToDecreaseThePriceIfTotalPlannedPFalls)
    dataFrameAppend("thresholdToDecreaseThePriceIfTotalPlannedPFalls",
                        "threshold to decrease the price if total plannedP falls",
                        common.thresholdToDecreaseThePriceIfTotalPlannedPFalls)
                        # saving pars

    print(\
    "\n(quasi) hayekian market sold threshold to lower the prices = %.2f\n" %
            common.soldThreshold1)
    dataFrameAppend("soldThreshold1",
                        "quasi h. market sold threshold lo lower the p.",
                        common.soldThreshold1)  # saving pars

    print(\
    "\n(quasi) hayekian market sold threshold to raise the prices = %.2f\n" %
            common.soldThreshold2)
    dataFrameAppend("soldThreshold2",
                        "quasi h. market sold threshold lo raise the p.",
                        common.soldThreshold2)  # saving pars

    print("\n'quasi' h. market, decreasing rate range of the prices = %6.3f\n" %
            common.decreasingRateRange)
    dataFrameAppend("decreasingRateRange",
                        "quasi h. market, decr. r. range of prices",
                        common.decreasingRateRange)  # saving pars

    print("\n'quasi' h. market, increasing rate range of the prices = %6.3f\n" %
            common.increasingRateRange)
    dataFrameAppend("increasingRateRange",
                        "quasi h. market, incr. r. range of prices",
                        common.increasingRateRange)  # saving pars

    print("\nShock in individual starting prices (h. market) = %6.3f\n" %
            common.initShock)
    dataFrameAppend("initShock",
                        "shock in individual starting prices (h. market)",
                        common.initShock)  # saving pars

    print("\nShift in individual starting prices (h. market) = %6.3f\n" %
            common.initShift)
    dataFrameAppend("initShift",
                        "shift in individual starting prices (h. market)",
                        common.initShift)  # saving pars

    print("\nRange of the correction of agent (as buyers) running prices in h. market = %7.4f\n"\
            % common.runningShockB)
    dataFrameAppend("runningShockB",
                        "correction of running prices in h. market (buyers)",
                        common.runningShockB)  # saving pars

    print("\nRange of the correction of agent (as sellers) running prices in h. market = %7.4f\n"\
            % common.runningShockS)
    dataFrameAppend("runningShockS",
                        "correction of running prices in h. market (sellers)",
                        common.runningShockS)  # saving pars

    print("\nShift in individual buyer running prices (h. market) = %6.3f\n" %
            common.runningShiftB)
    dataFrameAppend("runningShiftB",
                        "shift in individual buyer running prices (h. market)",
                        common.runningShiftB)  # saving pars

    print("\nShift in individual seller running prices (h. market) = %6.3f\n" %
            common.runningShiftS)
    dataFrameAppend("runningShiftS",
                        "shift in individual seller running prices (h. market)",
                        common.runningShiftS)  # saving pars

    print("\nJump in seller prices (full and quasi h. market) = %5.2f\n" % common.jump)
    dataFrameAppend("jump", "Jump in seller prices (full and quasi h. market)",
                        common.jump)  # saving pars

    print("\nProb. of a jump in seller prices (full and quasi h. market) = %5.2f\n"
                      % common.pJump)
    dataFrameAppend("pJump",
                "Prob. of a jump in seller prices (full and quasi h. market)",
                        common.pJump)  # saving pars

    print("\nPrice switch if profit falls (quasi h. market) = %7s\n"
                      % common.priceSwitchIfProfitFalls)
    dataFrameAppend("priceSwitchIfProfitFalls",
                            "Price switch if profit falls (quasi h. market)",
                        common.priceSwitchIfProfitFalls)  # saving pars

    print("\nPrice reverse action after %4d (q. h. m.);\nif <0, no other action in the while"
                      % common.profitStrategyReverseAfterN)
    dataFrameAppend("profitStrategyReverseAfterN",
     "P. reverse action after %4d (q. h. m.); if <0, no other action in the while",
                        common.profitStrategyReverseAfterN)  # saving pars

    print("\nquasi hayekian choice to drive sellers' price mod. = %9s\n" %
            common.quasiHchoice)
    dataFrameAppend("quasiHchoice",
                        "quasi hayekian choice to drive sellers' price mod.",
                        common.quasiHchoice)  # saving pars

    # Max quota (base 1) of the consumption in each sub step of a cycle
    print("\nMax quota (base 1) of the consumptions in each sub step of a cycle")
    common.consumptionQuota=fInput("(enter any value in a non-hayekian simulation): ")

    dataFrameAppend("consumptionQuota",
                        "Max quota (b. 1) of the cons. in each sub step of a cycle",
                        common.consumptionQuota)  # saving pars


    # Quota (0 <= Q <= 1) of the consumption quantities in hayekian phase at
    # t==-1; the quota of the quantity at t==-2 is (1 - Q)
    print(\
     "\nQuota (0 <= Q <= 1) of the consumption quantities in hayekian phase")
    common.Q = fInput("(Q is the weight of the quantity at t==-1;\n(1 - Q) is the weight "+\
                      "of the quantity at t==-2: "+\
                      "\n(enter any value in a non-hayekian simulation): ")

    if common.Q < 0 or common.Q > 1:
        print("out of range (0 <= Q <= 1)")
        os.sys.exit(1)

    dataFrameAppend("Q",
                    "Quota Q and (1 - Q) (0 <= Q <= 1) of c. at t-1 and t-2 in h. phase",
                    common.Q)  # saving pars



    # cycles
    self.nCycles = fInput("How many cycles? (0 = exit) ")

    dataFrameAppend("nCycles","# of cycles", self.nCycles)  # saving par

    v = input("verbose? (y/[n]) ")
    if v == "y" or v == "Y":
        common.verbose = True  # predefined False
    print("If running in IPython, the messages of the model about che creation" +
          "\nof each agent are automatically off, to avoid locking the run.")


def dataFrameAppend(name, definition, value):

    common.parsDict[name]=definition

    par_df2 = pd.DataFrame([[name, definition, value]],
                           columns=["Parameter internal names",\
                                    "Parameter definitions", "Values"])
    # print par_df2

    common.par_df = common.par_df.append(par_df2, ignore_index=True)
    # print common.par_df #warning: here the row index starts from 0
