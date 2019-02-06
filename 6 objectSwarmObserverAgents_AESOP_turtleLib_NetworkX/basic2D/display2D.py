#display2d.py for the basic2D project
import matplotlib.pyplot as plt

def checkRunningInIPython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


def display2D(agentList, cycle):
    if cycle==1:
        IPy=checkRunningInIPython()
        # Create a named display, if in iPython
        if IPy: myDisplay = display(None, display_id=True)

        #for i in range(len(agentList)):
        #    print("agent",agentList[i].number)

        # prepare graphic space
        fig, ax = plt.subplots(figsize=(7,7))
        ax.set_xlim(agentList[0].lX, agentList[0].rX)
        ax.set_ylim(agentList[0].bY, agentList[0].tY)
        if IPy: dots = ax.plot([],[],'ro')
