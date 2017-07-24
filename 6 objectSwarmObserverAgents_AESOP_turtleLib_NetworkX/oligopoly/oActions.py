from Tools import *
from Agent import *
import time
import csv
import graphicDisplayGlobalVarAndFunctions as gvf
import commonVar as common
import pandas as pd
import parameters as par

# to eliminate an annoying warning at time 1 in time series plot
import warnings
warnings.filterwarnings("ignore", module="matplotlib")


def do1b(address):

    # having the map of the agent
    agL = []
    for ag in address.modelSwarm.agentList:
        agL.append(ag.number)
    agL.sort()
    # print "\noActions before drawGraph agents", agL
    # print "oActions before drawGraph nodes", common.g.nodes()

    # basic action to visualize the networkX output
    gvf.openClearNetworkXdisplay()
    gvf.drawGraph()


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

    if subStep == "pause":
        input("Hit enter key to continue")
        return True

    elif subStep == "collectStructuralData":
        collectStructuralData(address.modelSwarm.agentList, common.cycle)
        return True

    elif subStep == "collectTimeSeries":
        collectTimeSeries(address.modelSwarm.agentList, common.cycle)
        return True

    elif subStep == "visualizePlot":
        visualizePlot()
        return True

    elif subStep == "prune":
        common.prune = True
        newValue = input(("Prune links with weight < %d\n" +
                          "Enter to confirm " +
                          "or introduce a new level: ") %
                         common.pruneThreshold)
        if newValue != "":
            common.pruneThreshold = int(newValue)
        return True

    # this subStep performs only partially the "end" item; the execution
    # will continue in ObserverSwarm.py
    elif subStep == "end":
        if not common.IPython or common.graphicStatus == "PythonViaTerminal":
            # the or is about ipython running in a terminal
            # += and ; as first character because a first part
            # of the string toBeExecuted is already defined in
            # commonVar.py
            common.toBeExecuted += ";gvf.plt.figure(2);gvf.plt.close()"

    else:
        return False


# collect Structural Data
def collectStructuralData(aL, t):
    # creating the dataframe
    try:
        common.str_df
    except BaseException:
        common.str_df = pd.DataFrame(columns=['entrepreneurs', 'workers'])
        print("\nCreation of fhe structural dataframe\n")
        # print common.str_df

    nWorkers = 0
    nEntrepreneurs = 0
    for ag in aL:
        if ag.agType == "entrepreneurs":
            nEntrepreneurs += 1
        if ag.agType == "workers":
            nWorkers += 1
    # print nEntrepreneurs, nWorkers
    str_df2 = pd.DataFrame([[nEntrepreneurs, nWorkers]],
                           columns=['entrepreneurs', 'workers'])
    # print str_df2

    common.str_df = common.str_df.append(str_df2, ignore_index=True)
    # print common.str_df #warning: here the row index starts from 0
    #(correctly in this case, being initial data
    # in each period)


# collect time series
def collectTimeSeries(aL, t):

    # creating the dataframe
    try:
        common.ts_df
    except BaseException:
        common.ts_df = pd.DataFrame(
            columns=[
                'unemployed',
                'totalProfit',
                'totalProduction',
                'plannedProduction',
                'price',
                'wage'])
        print("\nCreation of fhe time series dataframe\n")
        # print common.ts_df

    unemployed = 0
    for ag in aL:
        if not ag.employed:
            unemployed += 1

    ts_df2 = pd.DataFrame([[unemployed,
                            common.totalProfit,
                            common.totalProductionInA_TimeStep,
                            common.totalPlannedProduction,
                            common.price,
                            common.wage]],
                          columns=['unemployed',
                                   'totalProfit',
                                   'totalProduction',
                                   'plannedProduction',
                                   'price',
                                   'wage'])
    # print ts_df2

    # set previous price (t-1)
    common.p0 = common.price

    common.ts_df = common.ts_df.append(ts_df2, ignore_index=True)
    # print common.ts_df #warning: here the row index starts from 0


# graphical function
def visualizePlot():

    # Matplotlib colors
    # http://matplotlib.org/api/colors_api.html

    # html colors
    # http://www.w3schools.com/html/html_colornames.asp

    if common.cycle == 1 and \
       (not common.IPython or common.graphicStatus == "PythonViaTerminal"):
        # the or is about ipython running in a terminal
        gvf.plt.figure(2)
        mngr2 = gvf.plt.get_current_fig_manager()
        mngr2.window.wm_geometry("+0+0")
        mngr2.set_window_title("Time series")

        params = {'legend.fontsize': 10}
        gvf.plt.rcParams.update(params)

    if not common.IPython or common.graphicStatus == "PythonViaTerminal":
        # the or is about ipython running in a terminal
        gvf.plt.ion()
        f2 = gvf.plt.figure(2)
        gvf.plt.clf()
        myax = f2.gca()
        # myax.set_autoscale_on(True)

        ts_dfOut = common.ts_df
        # set index to start from 1
        ts_dfOut.index += 1
        myPlot = ts_dfOut.plot(
            secondary_y=[
                'price',
                'wage'],
            marker="*",
            color=[
                "OrangeRed",
                "LawnGreen",
                "Blue",
                "Violet",
                "Gray",
                "Brown"],
            ax=myax)
        myPlot.set_ylabel(
            'unemployed, totalProfit, totalProduction, plannedProduction')
        myPlot.right_ax.set_ylabel('price, wage')
        myPlot.legend(loc='upper left')
        myPlot.axes.right_ax.legend(loc='lower right')

    if common.IPython and not common.graphicStatus == "PythonViaTerminal":
        # the and not is about ipython running in a terminal
        f2 = gvf.plt.figure()
        myax = f2.gca()
        # myax.set_autoscale_on(True)
        gvf.plt.title('Time Series')

        ts_dfOut = common.ts_df
        # set index to start from 1
        ts_dfOut.index += 1
        myPlot = ts_dfOut.plot(
            secondary_y=[
                'price',
                'wage'],
            marker="*",
            color=[
                "OrangeRed",
                "LawnGreen",
                "Blue",
                "Violet",
                "Gray",
                "Brown"],
            ax=myax)
        myPlot.set_ylabel(
            'unemployed, totalProfit, totalProduction, plannedProduction')
        myPlot.right_ax.set_ylabel('price, wage')
        myPlot.legend(loc='upper left')
        myPlot.axes.right_ax.legend(loc='lower right')

    if not common.IPython or common.graphicStatus == "PythonViaTerminal":
        # the or is about ipython running in a terminal
        gvf.plt.figure(1)
        # gvf.plt.show()
        # gvf.plt.pause(0.01) #to display the sequence

    if common.IPython and not common.graphicStatus == "PythonViaTerminal":
        # the and not is about ipython running in a terminal
        gvf.plt.show()


# saving time series via toBeExecuted in commonVar.py
def saveTimeSeries():

    # using methodProbs which is a distionary generated by SLAPP
    par.dataFrameAppend("from schedule.xls: work trouble probability",
                        common.methodProbs["workTroubles"])

    tt = time.strftime("%Y%m%d_%H-%M-%S")

    fileName = tt + "_par.csv"
    csvfile = open(common.pro + "/" + fileName, "w")
    common.par_df.to_csv(csvfile, index_label=False, index=False)
    csvfile.close()

    fileName = tt + "_ts.csv"
    csvfile = open(common.pro + "/" + fileName, "w")
    common.ts_df.to_csv(csvfile, index_label=False, index=False)
    csvfile.close()

    fileName = tt + "_str.csv"
    csvfile = open(common.pro + "/" + fileName, "w")
    common.str_df.to_csv(csvfile, index_label=False, index=False)
    csvfile.close()

    print("Three files with date and hour", tt, "written in oligopoly folder.")
