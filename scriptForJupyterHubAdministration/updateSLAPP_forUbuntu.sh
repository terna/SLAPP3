
#!/bin/bash

rm -R --force SLAPP*
git clone https://github.com/terna/SLAPP3

cd SLAPP3
#rm -R ./-pictures
#rm SLAPP_Reference_Handbook.pdf
rm iRunShell.ipynb
mv iRunShell.ipynb.onlineVersion iRunShell.ipynb

cd ~/SLAPP3/"6 objectSwarmObserverAgents_AESOP_turtleLib_NetworkX"
rm -R --force oligopoly
git clone https://github.com/terna/oligopoly

cd
