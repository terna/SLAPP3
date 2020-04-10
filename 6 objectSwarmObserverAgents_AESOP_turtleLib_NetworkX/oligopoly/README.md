# Oligopoly
(readme build 20200410)


Marco Mazzoli, Matteo Morini, and Pietro Terna

The model and its construction are reported in [Oligopoly.pdf](Oligopoly.pdf). The code of the project is at [https://github.com/terna/oligopoly](https://github.com/terna/oligopoly).

A  concise presentation of the simulation mechanism is reported in the following
image:

<p align="center">
<img src="./OligopolyOutline.png" width="350" />
</p>

The book [M.Mazzoli, M.Morini, and P.Terna (2019), *Rethinking macroeconomics with endogenous market structure*, Cambridge University Press](https://www.cambridge.org/gb/academic/subjects/economics/macroeconomics-and-monetary-economics/rethinking-macroeconomics-endogenous-market-structure?format=HB&isbn=9781108482608); [other details](https://www.cambridge.org/core/books/rethinking-macroeconomics-with-endogenous-market-structure/CF5640C357029D9E49BE67D63A3FB122#). See also [Introduction and Chapter 1](https://books.google.it/books?id=iIHCDwAAQBAJ&pg=PR4&dq=mazzoli+terna&hl=it&sa=X&ved=0ahUKEwjfnpCVyIboAhWrw8QBHSVdDNAQ6AEIKTAA#v=onepage&q&f=false) via Googe Books.

We have also the [slides](slides_of_a_presentazione_of_the_model.pdf) of an old presentation of the Oligopoly model at [WEHIA 2017](http://www.wehia2017.com).

An article, [Business Cycle in a Macromodel with Oligopoly and Agents' Heterogeneity: An Agent-Based Approach, (2017)](http://rdcu.be/tlE6) of M.Mazzoli, M.Morini, and P.Terna, discusses the model and its results (if you experience problems in reading, please use Firefox). <sub><sup>[Look at *Erratum* below].<sub><sup>

The Oligopoly model uses [SLAPP](https://terna.github.io/SLAPP/) as its agent-based modeling shell.

To run a specific case of the above quoted article or of the book *Rethinking macroeconomics with endogenous market structure* of M.Mazzoli, M.Morini, and P.Terna, please look at the Appendix C of the book itself or to the file [runningSpecificCases.md](https://github.com/terna/oligopoly/blob/master/runningSpecificCases.md).

It is possible to run Oligopoly directly online, via [https://mybinder.org](https://mybinder.org),
accessing the file system at
[https://mybinder.org/v2/gh/terna/SLAPP3/master](https://mybinder.org/v2/gh/terna/SLAPP3/master) to modify – if necessary – the content of the folder ***oligopoly*** contained into the
folder ***6 objectSwarmObserverAgents_AESOP_turtleLib_NetworkX***.

Then, from the main folder, we launch the *iRunShellOnline.ipynb* file, and finally we follow the instructions contained in it.

______________________________________

<sub><sup>*Erratum for the paper above*: in Table 1, the **Expected employment ratio at t=1** is **0.9** and not 0.8.<sub><sup>
