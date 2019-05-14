import matplotlib as mpl
mpl.use("TKAgg")
import matplotlib.pyplot as plt

def create2():

    f=plt.figure(2)
    mngr = plt.get_current_fig_manager()
    mngr.window.wm_geometry("+650+0")
    mngr.set_window_title("Two")



