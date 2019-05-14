from create1 import *
from create2 import *

ax1=create1()
create2()

plt.ion()

a=[1, 2, 3]
ax1.plot(a)
plt.show()
plt.pause(0.1) # plt.pause are fundamentals for the interaction

plt.figure(2)
b=[3, 2, 1]
plt.plot(b)
plt.show()
plt.pause(0.1)

input("enter to continue")

ax1.cla()
plt.figure(2).clf()

a.append(10)
b.append(-10)

ax1.plot(a)
plt.show()
plt.pause(0.1)

plt.figure(2)
plt.plot(b)
plt.show()
plt.pause(0.1)

input("enter to finish")

plt.close()
plt.close()


