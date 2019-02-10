#display2d.py for the basic2D project
import matplotlib.pyplot as plt

def checkRunningInIPython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


def display3D(agentList, cycle, nCycles, sleep):
    global IPy, ax, dots, fig, myDisplay # to avoid missing assignment errors

    # preparing the frame space
    if cycle==1:
        IPy=checkRunningInIPython()
        # Create a named display, if in iPython
        if IPy: myDisplay = display(None, display_id=True)

        #for i in range(len(agentList)):
        #    print("agent",agentList[i].number)

        # prepare graphic space
        fig, ax = plt.subplots(figsize=(7,7))
        # asking the dimension of the world to one of the agents (the 0 one)
        ax.set_xlim(agentList[0].lX, agentList[0].rX)
        ax.set_ylim(agentList[0].bY, agentList[0].tY)
        if IPy: dots, = ax.plot([],[],'ro')

    if not IPy:
        plt.gca().cla()
        # asking the dimension of the world to one of the agents (the 0 one)
        ax.set_xlim(agentList[0].lX, agentList[0].rX)
        ax.set_ylim(agentList[0].bY, agentList[0].tY)

    # update data from the agents' world
    xList=[]
    yList=[]

    for i in range(len(agentList)):
        x,y=agentList[i].reportPos()
        xList.append(x)
        yList.append(y)

    if IPy:
        dots.set_data(xList, yList)
    else:
        ax.plot(xList,yList,'ro')

    # display
    if cycle==1: ax.set_title(str(cycle)+" initial frame")
    if cycle>1 and cycle<nCycles: ax.set_title(str(cycle))
    if cycle==nCycles: ax.set_title(str(cycle)+" final frame")

    if IPy: myDisplay.update(fig)
    else: fig.canvas.draw()

    plt.pause(sleep+0.001) # if sleep is 0, it locks the figure
    print("end cycle",cycle,"of the animation")
