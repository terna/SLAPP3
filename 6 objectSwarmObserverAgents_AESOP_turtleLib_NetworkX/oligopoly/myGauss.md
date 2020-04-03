We refer to the book "Rethinking macroeconomics with endogenous market
structure",vreporting the version "6book" of this simulation. You can replicate
all the resultsvreported there. To do that, follow the file
**runningSpecificCases.md** in this folder.

myGauss.py introduces an improvement of the gaussian random number generation
performed by random.gauss in Python, to assure both (i) backward compatibility
with full replication of book cases from 1 to 11, and (ii) the full replication
of new experiments in Mac, Linux and Windows.

This is done:

in case (i) using exactly the random values used while calculating
the experiments which are in the book (the data are online or in the GitHub
repository of Oligopoly; *if you use the Oligopoly version included in SLAPP,
automatically you access the online values*);

in case (ii) generating random gaussian values which are exactly the same in
the operating system listed above.

For **Mac users**: if you experience 'certificate error' while accessing online
data, go to Macintosh HD > Applications > Python3.6 folder (or whatever version
  of python you're using) > double click on "Install Certificates.command" file.

From
https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
