First of all, have a look to the scheme in OligopolyOutline.png

SETTING THE INITIAL OR CURRENT QUANTITY TO BE PRODUCED

in Agent.py (via modelActions.txt reset)

setNewCycleValues

price to be used to establish the first global quantity, based on
common.totalPlannedConsumptionInValueInA_TimeStep

for V6 Version, when

common.cycle == common.startHayekianMarket

(startHayekianMarket is the
value k in the 'Making of')

being common.cycle => t

if common.startHayekianMarket > 1
if t>2 we use the price at -2
if t==2 we use the price at -1

implicitly, if common.cycle==1, makeProductionPlan gives common.totalPlannedProduction
(and individual self.plannedProduction)
related to the *rho* value and we do not need to establish neither a previous
price nor the common.totalConsumptionInQuantityInPrevious_TimeStep
(we will use self.plannedProduction and common.totalPlannedProduction
determined by makeProductionPlan)

indeed,

in Agent.py makeProductionPlan
works only if common.cycle == 1, establishing both
self.plannedProduction and
common.totalPlannedProduction

---

in Agent.py adaptProductionPlanV6


we have to take in consideration the alternative

1) if common.cycle > 1 and common.cycle < common.startHayekianMarket:
this situation excludes the case common.startHayekianMarket==1
and establishes both
self.plannedProduction and
common.totalPlannedProduction

2) if common.cycle >1 and common.cycle >= common.startHayekianMarket:
     #the case common.cycle==1, with common.startHayekianMarket==1, is
     #absorbed by makeProductionPlan

in the regular situation:
self.plannedProduction and
common.totalPlannedProduction
derive directly from common.totalConsumptionInQuantityInPrevious_TimeStep

!!!!
or (NOVELTY) from common.totalConsumptionInQuantityInPrevious2_TimeStep
with a mix of the two measures with weights

w and (1 - w) having (0 <= w <= 1)

and (with common.w)

    common.totalConsumptionInQuantityInPrevious_TimeStep = \
      common.w * common.totalConsumptionInQuantityInPrevious_TimeStep +\
      (1 - common.w) * common.totalConsumptionInQuantityInPrevious2_TimeStep

!!!!



---

SETTING THE INITIAL PRICE THAT THE AGENTS ADOPT TO START THEIR ACTION IN THE HAYEKIAN PHASE


in actOnMaketPlace, how to define the initial price used to buy and sell?

if common.cycle >= common.startHayekianMarket

we have, only once, the priceWarming phase
in which we differentiate the common.startHayekianMarket>1 or
common.startHayekianMarket>2 cases from the ==1 case in which common.ts_df
has to be created

in the common.startHayekianMarket == 1 case, when actOnMaketPlace is activated
we already have common.totalPlannedConsumptionInValueInA_TimeStep and
common.totalProductionInA_TimeStep

so, we can calculate
common.price = common.totalPlannedConsumptionInValueInA_TimeStep \
               / common.totalProductionInA_TimeStep

outside WorldState setMarketPriceV3 method, to avoid here random shocks
