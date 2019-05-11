The default current case is the experiment 11.


Versions of the key libraries:
NetworkX 2.2
matplotlib 3.0.2
pandas 0.23.1

In case of Python errors, try to go back to these versions, using pip in the form

pip uninstall specificLib && pip install specificLib==versionNumber
(or pip -> pip3)

e.g.,

pip uninstall matplotlib && pip install matplotlib==3.0.2


**To run the experiments of the cases *0a* and *0b*** of the book (or the two of the 2017 article, which are the same),
please use the Oligopoly code of the release V5book, or directly the branch masterP2, running the project with SLAPP 2.0,
which is at [https://github.com/terna/SLAPP2](https://github.com/terna/SLAPP2) and controlling that the parameters are those of rows 1 and 2 of Tables T1.pdf and T2.pdf here. Considering the SMAC (Simple Market Aggregate Clearing mechanism)  version of the *oligopoly* project, the *startHayekianMarket* parameter is not used, while in the Table T2.pdf is set to 51 by default.

To set the correct parameters, for the cases *0a* and *0b**, you can simply modify the parameter absoluteBarrierToBecomeEntrepreneur at row 123 of the file commonVar.py of the above releases of Oligopoly, setting it to 20 (case *0a*) or to 0 (case *0b*).

The path to the folder containing the Oligopoly code has to be included in a file named *project.txt*, to be placed into the main folder os SLAPP.

**For all the cases below**, please use the Oligopoly code of the release V6book, or directly the branch master, running the project with SLAPP 3.0 or higher,
which is at [https://github.com/terna/SLAPP3](https://github.com/terna/SLAPP3).

As above, the path to the folder containing the Oligopoly code has to be included in a file named *project.txt*, to be placed into the main folder of SLAPP.

**To run the experiments of the cases from *1* to *6***

* delete the file schedule.xls;
* duplicate the file **schedule5.xls**;
* rename the result as schedule.xls.

*For each specific experiment*:
* delete the files commonVar.py,  workers.txtx, entrepreneurs.txt (if any), entrepreneurs.txtx (if any);

* for case *X*, duplicate the files commonVar.py.caseX, workers.txtx.caseX, entrepreneurs.txt.caseX or entrepreneurs.txtx.caseX ;

* rename the results as commonVar.py,  workers.txtx, entrepreneurs.txt or entrepreneurs.txtx.

**To run the experiments of the cases *7* and *7b***
* delete the file schedule.xls;
* duplicate the file **schedule6.xls.backwardCompatibily**;
* rename the result as schedule.xls.

*For each specific experiment*:
* delete the files commonVar.py,  workers.txtx, entrepreneurs.txt (if any), entrepreneurs.txtx (if any);

* for case *X*, duplicate the files commonVar.py.caseX, workers.txtx.caseX, entrepreneurs.txt.caseX or entrepreneurs.txtx.caseX ;

* rename the results as commonVar.py,  workers.txtx, entrepreneurs.txt or entrepreneurs.txtx.

The experiments from *1* to *7* also run without the modifications above, but producing slightly different results.

**To run the experiments of the cases from *8* upwards**

If we made the modifications above:
* delete the file schedule.xls;
* duplicate the file schedule6.xls;
* rename the result as schedule.xls.

*For each specific experiment*:
* delete the files commonVar.py,  workers.txtx, entrepreneurs.txt (if any), entrepreneurs.txtx (if any);

* for case *X*, duplicate the files commonVar.py.caseX, workers.txtx.caseX, entrepreneurs.txt.caseX or entrepreneurs.txtx.caseX ;

* rename the results as commonVar.py,  workers.txtx, entrepreneurs.txt or entrepreneurs.txtx.

==========

The parameters of the different cases, contained into the *commonVar.py.caseX* files, are also reported in the tables of the files *T1.pdf* and *T2.pdf*.

The values to be introduced interactively for each case, if any, are reported in the table of the file *T3.pdf*.

The files T1.pdf, T2.pdf, and T3.pdf are in this folder.
