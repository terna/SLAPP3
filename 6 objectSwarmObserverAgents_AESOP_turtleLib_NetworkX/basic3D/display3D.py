#display2d.py for the basic3D project
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3

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
        fig = plt.figure(figsize=(7,7))
        ax = p3.Axes3D(fig)
        # asking the dimension of the world to one of the agents (the 0 one)
        ax.set_xlim(agentList[0].lX, agentList[0].rX)
        ax.set_ylim(agentList[0].bY, agentList[0].tY)
        ax.set_zlim(agentList[0].bZ, agentList[0].tZ)
        if IPy: dots = ax.plot3D([],[],'ro')


    if not IPy:
        plt.gca().cla()
        # asking the dimension of the world to one of the agents (the 0 one)
        ax.set_xlim(agentList[0].lX, agentList[0].rX)
        ax.set_ylim(agentList[0].bY, agentList[0].tY)
        ax.set_zlim(agentList[0].bZ, agentList[0].tZ)

    # update data from the agents' world
    xList=[]
    yList=[]
    zList=[]

    for i in range(len(agentList)):
        x,y,z=agentList[i].reportPos()
        xList.append(x)
        yList.append(y)
        zList.append(z)

    if IPy:
        dots.set_data(xList, yList)
        dots.set_3d_properties(zList)
    else:
        ax.plot3D(xList,yList,zList,'ro')

    # display
    if cycle==1: ax.set_title(str(cycle)+" initial frame")
    if cycle>1 and cycle<nCycles: ax.set_title(str(cycle))
    if cycle==nCycles: ax.set_title(str(cycle)+" final frame")

    if IPy: myDisplay.update(fig)
    else: fig.canvas.draw()

    plt.pause(sleep+0.001) # if sleep is 0, it locks the figure
    print("end cycle",cycle,"of the animation")
