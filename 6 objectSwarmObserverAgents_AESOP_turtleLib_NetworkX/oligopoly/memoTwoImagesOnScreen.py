# this file contains a preparatory exercise, kept here as a memo for future similar problems
# the technique below is implemented in oligopoly project, files:
# graphicDisplayGlobalVarAndFunctions.py and
# oActions.py

import matplotlib as mpl
mpl.use("TKAgg")

import matplotlib.pyplot as plt


plt.figure(1)
mngr1 = plt.get_current_fig_manager()  # NB, after figure()
mngr1.window.wm_geometry("+0+0")
mngr1.set_window_title("One")

plt.ion()
plt.plot([1, 2, 3])
plt.draw()

plt.figure(2)
mngr2 = plt.get_current_fig_manager()
mngr2.window.wm_geometry("+650+0")
mngr2.set_window_title("Two")

plt.plot([3, 2, 1])
plt.draw()


input('enter')

plt.figure(1)

plt.plot([1, 2, 3, 44])
plt.draw()

plt.figure(2)

plt.plot([44, 3, 2, 1])
plt.draw()


input('enter')
plt.close()
plt.figure(1)

plt.close()

"""



"""
