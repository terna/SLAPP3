# commonVar.py

projectVersion = "5bPy3"

build = "20170611"

debug = False

# controlling the existence of an agent with number==0 used by reset
# step in modelActions.txt
agent1existing = False

# the time is set by ObserverSwarm with
# common.cycle=1
# in the benginning

prune = False
pruneThreshold = 0

g = 0  # this variable will contain the address of the graph
g_labels = 0  # this variable will contain the address of the labels
g_edge_labels = 0  # this variable will contain the address of the labels of the edges

btwn = 0  # this variable will contain the betweenness centrality indicators
clsn = 0  # this variable will contain the closeness centrality indicators


orderedListOfNodes = []
verbose = False
clonedN = 0

# sigma of the normal distribution used in randomize the position of the agents/nodes
# sigma=0.7
sigma = 1.2

# size of the nodes
nsize = 150

# demand funtion paramenters (1) entrepreneurs as consumers (2) employed workers
#(3) unemployed workers
# with Ci = ai + bi Y + u
# u=N(0,consumptionErrorSD)
consumptionRandomComponentSD = 0.3

#(1)
a1 = 0.4
b1 = 0.55
# Y1=profit(t-1)+wage NB no negative consumption if profit(t-1) < 0

#(2)
a2 = 0.3
b2 = 0.65
# Y2=wage

#(3)
socialWelfareCompensation = 0.3
a3 = 0
b3 = 1
# Y3=socialWelfareCompensation

#wages and revenues
wage = 1.

fullEmploymentThreshold = 0.05
wageStepInFullEmployment = 0.10
fullEmploymentStatus = False

wageAddendum = 0
maxAcceptableOligopolistRelativeIncrement = 0.20
temporaryRelativeWageIncrementAsBarrier = 0.15


revenuesOfSalesForEachWorker = 1.005

# work troubles, production correction Psi, relative value
productionCorrectionPsi = 0.10
# does it generate a cut of the wages
wageCutForWorkTroubles = False
# price penalty for work troubles
penaltyValue = 0  # was 0.10

# labor productivity
laborProductivity = 1

# thresholds (for Version 0)
hiringThreshold = 0
firingThreshold = 0

# macro variables
totalProductionInA_TimeStep = 0
totalPlannedConsumptionInValueInA_TimeStep = 0

# Poisson mean in makeProoductionPlan, will be modified in paramenters.py
# in the function loadParameters
nu = 5

# to internally calculate the Poisson mean (nu) in makeProoductionPlan
# for time=1 in V3 we use the ratio rho
rho = 0.9

# threshold toEntrepreneur
thresholdToEntrepreneur = 0.15  # was 0.20
extraCostsDuration = 3
newEntrantExtraCosts = 60  # was 100.0 # was 2.0

randomComponentOfPlannedProduction = 0.10

# max new entrant number in a time step
absoluteBarrierToBecomeEntrepreneur = 20

maxDemandRelativeRandomShock = 0.15  # was 0.10 #was 0.20

# threshold toWorker
thresholdToWorker = -0.20


nodeNumbersInGraph = False

# step to be executed at end (plus an optional second part added
# within oActions.py)
toBeExecuted = "saveTimeSeries()"
