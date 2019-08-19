"Book" is used here to make reference to [M. Mazzoli, M. Morini, and P. Terna (2019), Rethinking Macroeconomics with Endogenous Market Structure](https://www.cambridge.org/core/books/rethinking-macroeconomics-with-endogenous-market-structure/CF5640C357029D9E49BE67D63A3FB122#).

The final rows of Appendix C of the book recall this file.



*Running Oligopoy project*

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

==========


**Running oligopoly code online**


*Using myBinder*

We can run the model online, via [https://mybinder.org](https://mybinder.org),
accessing the file system at
[https://mybinder.org/v2/gh/terna/SLAPP3/master](https://mybinder.org/v2/gh/terna/SLAPP3/master) to modify – if necessary – the content of the folder ***oligopoly*** contained into the
folder ***6 objectSwarmObserverAgents_AESOP_turtleLib_NetworkX***.

Be patient, the preparation process can be quite long.

Then, from the main folder, we launch the *iRunShellOnline.ipynb* file, and finally we follow the instructions contained in it.

We can also jump directly to the *iRunShellOnline.ipynb* file following: [https://mybinder.org/v2/gh/terna/SLAPP3/master?filepath=iRunShellOnline.ipynb](https://mybinder.org/v2/gh/terna/SLAPP3/master?filepath=iRunShellOnline.ipynb)

In this way, We will run directly the *book case 11*, the default one.


*Using Colab*

at [https://colab.research.google.com](https://colab.research.google.com) sign in
with a Google account

Use File/New Python3 notebook and then enter

!git clone https://github.com/terna/SLAPP3

(if you execute a cell via the arrow, then use '+ Code' button if you need to
create room for a new cell; executing the cells with shift+enter, automatically
you have also a new cell below)

cd SLAPP3
run iRunShellOnline.ipynb

then enter: oligopoly / 111 / 0.10 / 0.25 /50 / n

To modify the files of Oligopoy, e.g., following the Appendix C of the book, go
to [https://github.com/terna/SLAPP3](https://github.com/terna/SLAPP3) and fork
the git to have your copy (at a new address), then modify the content of the
folder ***oligopoly*** contained into the
folder ***6 objectSwarmObserverAgents_AESOP_turtleLib_NetworkX***.

Finally, run the new git in Colab, as above.


*Using JupyterLab in myBinder*

At [https://jupyterlab.readthedocs.io/en/stable/](https://jupyterlab.readthedocs.io/en/stable/) in the first rows of the page we have a link to open JupiterLab in myBinder (Try it in myBinder).

The link is: [https://mybinder.org/v2/gh/jupyterlab/jupyterlab-demo/master?urlpath=lab/tree/demo](https://mybinder.org/v2/gh/jupyterlab/jupyterlab-demo/master?urlpath=lab/tree/demo)


Open the link and when active, create a new Python3 notebook and execute:

     !git clone https://github.com/terna/SLAPP3

     cd SLAPP3

     pip install -r requirements.txt

     run iRunShell.ipynb

or

     run iRunShellOnline.ipynb

Then, as above, the replies are: oligopoly / 111 / 0.10 / 0.25 /50 / n

In the left column, clicking on *6 objectSwarmObserverAgents_AESOP_turtleLib_NetworkX*
and the on *oligopoly*, you can modify any file.

After the conclusion of a run, the results are saved into the online file system.

There you can find the readingCsvOutput_par_corr_BWter.ipynb notebook; running
it and choosing the correct set of input files, you obtain the results
and the figures of the book.


*Using JupyterLab in Colab*

it would be nice to use JupyterLab in Colab, to run SLAPP and Oligopoly. Thank to
the readers that will send us any suggestion ...

Currently (August 2019), we know that it is possible to have JupyterLab in Colab,
but it is very complicated. E.g., [https://medium.com/@swaroopkml96/jupyterlab-and-google-drive-integration-with-google-colab-42a8d64a9b63](https://medium.com/@swaroopkml96/jupyterlab-and-google-drive-integration-with-google-colab-42a8d64a9b63)
