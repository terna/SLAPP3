from Tools import *
from Agent import *
import time
import csv
import graphicDisplayGlobalVarAndFunctions as gvf
import commonVar as common
import pandas as pd
import parameters as par
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# to eliminate an annoying warning at time 1 in time series plot
import warnings
warnings.filterwarnings("ignore", module="matplotlib")


def do1b(address):

    if common.cycle == 1:
            # setting Figure for the net
            if not common.IPython or common.graphicStatus == "PythonViaTerminal":
                # the or is about ipython running in a terminal
                f=gvf.plt.figure(num=2)
                mngr1 = gvf.plt.get_current_fig_manager()  # NB, after figure()
                mngr1.window.wm_geometry("+650+0")
                mngr1.set_window_title("Links Entrepreneurs - Workers")

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
                'consumptionQ',
                #'hPriceSd',
                'hPSd',
                'price',
                'wage'])
        print("\nCreation of fhe time series dataframe\n")
        # print common.ts_df

    unemployed = 0
    for ag in aL:
        if not ag.employed:
            unemployed += 1

    # hiding unexisting mean or sd of prices, in the pre-hayekian period
    # or in the hayekian one if data are too few
    # -100 is used in checkHayekianPrices function of WorldState.py
    if common.price == -100: common.price=np.nan
    hPSd_=common.hPSd
    if common.hPSd==-100: hPSd_=np.nan

    # hiding unexisting measure of consumtion in quantity in the pre-hayekian
    # phase
    if common.totalConsumptionInQuantityInA_TimeStep==0:
        common.totalConsumptionInQuantityInA_TimeStep=np.nan

    ts_df2 = pd.DataFrame([[unemployed,
                            common.totalProfit,
                            common.totalProductionInA_TimeStep,
                            common.totalPlannedProduction,
                            common.totalConsumptionInQuantityInA_TimeStep,
                            hPSd_,
                            common.price,
                            common.wage]],
                          columns=['unemployed',
                                   'totalProfit',
                                   'totalProduction',
                                   'plannedProduction',
                                   'consumptionQ',
                                   'hPSd',
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

    if not common.IPython or common.graphicStatus == "PythonViaTerminal":
        # the or is about ipython running in a terminal
        f= gvf.plt.figure()
        mngr2 = gvf.plt.get_current_fig_manager()
        mngr2.window.wm_geometry("+0+0")
        mngr2.set_window_title("Time series")
        params = {'legend.fontsize': 10}
        gvf.plt.rcParams.update(params)
        common.axPlot = f.gca()
        gvf.plt.ion()

    if not common.IPython or common.graphicStatus == "PythonViaTerminal":
        # the or is about ipython running in a terminal
        common.axPlot.cla()

        ts_dfOut = common.ts_df
        # set index to start from 1
        ts_dfOut.index += 1
        myPlot = ts_dfOut.plot(
            secondary_y=[
                #'hPriceSd',
                'price',
                'wage'],
            marker="*",
            color=[
                "OrangeRed",
                "LawnGreen",
                "Blue",
                "Violet",
                "lightblue",
                "Pink",
                "Gray",
                "Brown"],
            ax=common.axPlot)
        myPlot.set_ylabel(
'unemployed, totalProfit, totalProduction, plannedProduction, consumptionQ, hPSd')
        myPlot.right_ax.set_ylabel('price, wage')
        myPlot.legend(loc='upper left')
        myPlot.axes.right_ax.legend(loc='lower right')
        gvf.plt.pause(0.01)

    if common.IPython and not common.graphicStatus == "PythonViaTerminal":
        # the and not is about ipython running in a terminal
        f2 = gvf.plt.figure()
        myax = f2.gca()
        #myax.set_autoscale_on(True)
        gvf.plt.title('Time Series')

        ts_dfOut = common.ts_df
        # set index to start from 1
        ts_dfOut.index += 1

        myPlot = ts_dfOut.plot(
            secondary_y=[
                #'hPriceSd',
                'price',
                'wage'],
            marker="*",
            color=[
                "OrangeRed",
                "LawnGreen",
                "Blue",
                "Violet",
                "lightblue",
                "Pink",
                "Gray",
                "Brown"],xlim=[0.9,common.cycle+0.1],
            ax=myax)
        myPlot.set_ylabel(
'unemployed, totalProfit, totalProduction, plannedProduction, consumptionQ, hPSd')
        myPlot.right_ax.set_ylabel('price, wage')
        myPlot.legend(loc='upper left')
        myPlot.axes.right_ax.legend(loc='lower right')

    #if not common.IPython or common.graphicStatus == "PythonViaTerminal":
        # the or is about ipython running in a terminal
        #gvf.plt.figure(1)
        # gvf.plt.show()
        # gvf.plt.pause(0.01) #to display the sequence

    if common.IPython and not common.graphicStatus == "PythonViaTerminal":
        # the and not is about ipython running in a terminal
        gvf.plt.show()


# saving time data via toBeExecuted in commonVar.py
def saveData():

    if common.fgIn!=None: common.fgIn.close()
    #closing fgOu
    if common.fgOu != None:
        common.fgOu.close()
        import zipfile
        compression = zipfile.ZIP_DEFLATED
        print("creating the archive "+common.case+".txt.zip in folder "+common.project+\
              "/exampleGauss/")
        z = zipfile.ZipFile(common.project+"/exampleGauss/"+common.case+".txt.zip", mode='w')
        z.write(common.project+"/exampleGauss/"+common.case+".txt",arcname=common.case+".txt",\
                compress_type=compression)
        print('zip compressed')

        import os
        print("removing file "+common.case+".txt from folder "+common.project+\
              "/exampleGauss/")
        os.remove(common.project+"/exampleGauss/"+common.case+".txt")

    # used in myGauss.py


    # using methodProbs which is a dictionary generated by SLAPP
    par.dataFrameAppend("notExisting",\
                        "from schedule.xls: work trouble probability",
                        common.methodProbs['workTroubles'])


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

    fileName = tt + "_firms.csv"
    csvfile = open(common.pro + "/" + fileName, "w")
    common.firm_df.to_csv(csvfile, index_label=False, index=False)
    csvfile.close()

    # the common.modPars_df can be missing
    try:
        common.modPars_df
        fileName = tt + "_modPars.csv"
        csvfile = open(common.pro + "/" + fileName, "w")
        common.modPars_df.to_csv(csvfile, index_label=False, index=False)
        print("Five files with date and hour", tt, "written in oligopoly folder.")

    except BaseException:
        print("Four files with date and hour", tt, "written in oligopoly folder.")



# special action code, to be activated if the time
# (cycle) is equal to ...
#
def makeSpecialAction():

    if common.cycle == 1:

        files=os.listdir(common.pro)

        if "modPars.txt" in files:
            common.file_modPars=True
            print("The special action has to be activated at cycle ... ")
            common.activationCycle = int(input("-1 if never "))

        else:
            print("\nWarning: no file 'modPars.txt', the specialAction "+\
                  "item has no effect.\n\n")



    if common.file_modPars and common.cycle == common.activationCycle:
        print("\n***Special action at time =", common.cycle)
        print("***Modification of the following parameters\n")

        common.nameValues={}
        fIn=open(common.pro+"/modPars.txt","r")

        for line in fIn:
              line=line.replace('\t',' ')
              lineS=line.split() #one or more spaces as a delimiter

              n=lineS[0]

              if n=="mySeed" or n=="projectVersion" or n=="build" \
                     or n=="notExisting" or n=="nCycles":
                  print("Impossible to modify the '"+n+"' parameter in this way.")
                  print("Program exiting.")
                  os.sys.exit(1)

              try: v=int(lineS[1])
              except:
                   try: v=float(lineS[1])
                   except: v=lineS[1]


              if common.check(n)[0]:
                print('existing parameter '+n+', former value',\
                       common.check(n)[1], ' new value ', v,'\n')
                collectModPars(n,common.check(n)[1],v)
              else:
                print('added parameter '+n+', value ', v,'\n')
                collectModPars(n,np.NaN,v)

              common.nameValues[n]=v

        fIn.close()

        common.setVar()


# collect modified parameters
def collectModPars(parName, previousValue, newValue):
            # creating the dataframe
            try:
                common.modPars_df
            except BaseException:
                common.modPars_df = pd.DataFrame(columns=[\
                                    "Parameter internal names",\
                                    "Parameter definitions", \
                                    "previousValue","newValue"])
                print("Creation of the modified parameter database\n")
                # print common.modPars_df

                # recording the modification cycle

                modPars_df2 = pd.DataFrame([\
                            ["NaN","Modifications at time = "+str(common.activationCycle), \
                             np.NaN, np.NaN]], columns=[\
                                               "Parameter internal names",\
                                               "Parameter definitions", \
                                               "previousValue","newValue"])

                common.modPars_df = common.modPars_df.append(modPars_df2, \
                                              ignore_index=True)

                # regular data recording
            modPars_df2 = pd.DataFrame([[parName, common.parsDict[parName],
                                         previousValue, newValue]],
                                   columns=["Parameter internal names",\
                                            "Parameter definitions", \
                                            "previousValue","newValue"])

            common.modPars_df = common.modPars_df.append(modPars_df2, \
                                                     ignore_index=True)
            #print (common.modPars_df)
