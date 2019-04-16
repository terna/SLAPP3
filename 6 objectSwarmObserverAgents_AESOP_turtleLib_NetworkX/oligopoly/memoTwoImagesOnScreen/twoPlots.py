from create1 import *
from create2 import *

ax1=create1()
ax2=create2()

plt.ion()

a=[1, 2, 3]
ax1.plot(a)
plt.show()
plt.pause(0.1) # plt.pause are fundamentals for the interaction

b=[3, 2, 1]
ax2.plot(b)
plt.show()
plt.pause(0.1)

a.append(10)
b.append(-10)

input("enter to continue")

ax1.cla()
ax2.cla()


ax1.plot(a)
plt.show()
plt.pause(0.1)

ax2.plot(b)
plt.show()
plt.pause(0.1)

input("enter to finish")

plt.close()
plt.close()


