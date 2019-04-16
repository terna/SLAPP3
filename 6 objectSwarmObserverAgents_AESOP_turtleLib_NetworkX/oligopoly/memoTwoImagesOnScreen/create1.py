import matplotlib as mpl
mpl.use("TKAgg")
import matplotlib.pyplot as plt

def create1():

    f=plt.figure()
    mngr = plt.get_current_fig_manager()  # NB, after figure()
    mngr.window.wm_geometry("+0+0")
    mngr.set_window_title("One")
    ax = f.gca()

    return ax
