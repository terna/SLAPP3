# https://github.com/python/cpython/blob/master/Lib/random.py
import random as r
import math
import commonVar as common

class myG():
    # When x and y are two variables from [0, 1), uniformly
    # distributed, then
    #
    #    cos(2*pi*x)*sqrt(-2*log(1-y))
    #    sin(2*pi*x)*sqrt(-2*log(1-y))
    #
    # are two *independent* variables with normal distribution
    # (mu = 0, sigma = 1).
    # tnx to Lambert Meertens, https://en.wikipedia.org/wiki/Lambert_Meertens

    # cos and sin produce small differences in tails in Mac, Linux, Windows
    # so we cut them; we do not truncate them with floor(x*10**n)*10**-n
    # to avoid subtle division errors (1/10 in base 2)

    def __init__(self):

        self.TWOPI=2.0*math.pi
        self.gauss_next=None

    def myGauss0(self,mu, sigma):

        z = self.gauss_next
        self.gauss_next=None
        if z is None:
          x2pi = r.random() * self.TWOPI
          g2rad = math.sqrt(-2.0 * math.log(1.0 - r.random()))
          g2rad=('%1.20f' % g2rad)             # converts also exponent 'e'
                                               # with an extra number of digits
          g2rad=float(g2rad[0:12])      # cutting 'dangeorus' digits (rounding
                                        # effects and different tails in Mac or Linux)


          myCos=('%1.20f' % math.cos(x2pi))    # converts also exponent 'e'
          mySin=('%1.20f' % math.sin(x2pi))    # with an extra number of digits

          myCos=float(myCos[0:12])  # cutting 'dangeorus' digits (rounding
          mySin=float(mySin[0:12])  # effects and different tails in Mac or Linux)

          z = myCos * g2rad
          self.gauss_next=mySin * g2rad
        return mu + z*sigma

    def myGauss(self,mu, sigma):
        if common.fgIn == None and common.fgOu==None:
          try:
            common.example
            if common.example == "11":
                try:
                    common.fgIn=open(common.project+"/exampleGauss/11.txt","r")
                except:
                    common.fgOu=open(common.project+"/exampleGauss/11.txt","w")
          except:
            pass

        if common.fgIn != None:
            g=float(common.fgIn.readline())
            r.gauss(mu, sigma) # to generate two random numbers and maintain
                               # the orginal sequence

        if common.fgOu != None:
            g=r.gauss(mu, sigma)
            print(g,file=common.fgOu)

        return g
