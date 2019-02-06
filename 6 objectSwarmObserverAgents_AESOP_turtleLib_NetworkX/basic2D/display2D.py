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
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        if IPy: dots = ax.plot([],[],'ro')
