from scipy import stats
from math import sqrt
import pandas as pd
from IPython.display import display
import numpy as np
from datetime import datetime
class ABTest:
    def set_cs(self , c1, s1, c2, s2):
        ctr1, ctr2 = c1 / s1 , c2 / s2
        #print c1, s1, c2, s2
        #print ctr1, ctr2, ctr1 - ctr2, ((ctr1 - ctr2) * 2) / (ctr1 + ctr2)
        self.ca, self.sa, self.cb, self.sb =  c1, s1, c2, s2
    def pctr(self):
        actr = (self.ca / self.sa)
        bctr = (self.cb / self.sb)
        print "%s=%f, %s=%f, %s - %s=%f" % ( self.atag, actr, self.btag, bctr, self.atag, self.btag, actr-bctr)
    def printresult(self, result):
        print result[1], result[-1], result[0]
        print result[3] result[4]
    def ztest(self, z):
        result = ["score test", self.date]
        pval = stats.norm.cdf(z)
        if z > 0.:
            pval = 1. - pval
        result.append( "z=%f" % z)
        result.append( "pval=%f" %  pval)
        result.append( "H0: p_a == p_b")
        if pval < 0.05:
            result.append( 'reject H0')
        else:
            result.append( 'can\'t reject H0')
        self.printresult(result)

    def score_test(self):
        st = self.score_test_stat()
        self.ztest(st)

    def chi2test(self):
        c1, s1, c2, s2 = self.ca, self.sa, self.cb, self.sb
        #test: chi2=1.158368 pval=0.281804
        #c1, s1, c2, s2 = (10., 56000., 21., 78000.)
        obs = np.array([c1, c2, s1 - c1, s2 - c2])
        pclick = (c1 + c2) / (s1 + s2)
        p = np.array( [pclick] * 2 + [1 - pclick] * 2 )
        exp = np.array([s1, s2, s1, s2]) * p
        chi2 = sum(np.square( (obs - exp) ) / exp)
        pval = 1 -  stats.chi2.cdf(chi2, 1)
        result = ["chi2 test", self.date]
        result.append("chi2=%f" % chi2)
        #pval = 1 - stats.chi2.cdf(3.84, 1)
        result.append("pval=%f" % (pval))
        result.append("H0: p_a == p_b")
        if pval < 0.05:
            result.append('reject H0')
        else:
            result.append('can\'t reject H0')
        self.printresult(result)


    def score_test_stat(self):
        c1, s1, c2, s2 = self.ca, self.sa, self.cb, self.sb
        p1 = c1 / s1
        p2 = c2 / s2
        p = (c1 + c2) / (s1 + s2)
        z = (p1 - p2) / sqrt ( p * ( 1 - p) * ( (1 / s1) + (1 / s2) ) )
        return z

def test():
    abtest = ABTest()
    abtest.date = "20160127 tag=305872 (25% split) vs tag=305724 (25% split)" 
    abtest.set_cs(6062., 86642., 6412., 87003.)
    abtest.score_test()
    abtest.chi2test()
    abtest.date = "tag=212631(50% split) vs tag=305724 (25% split)" 
    abtest.set_cs(13449., 174044., 6412., 87003.)
    abtest.score_test()
    abtest.chi2test()
    abtest.date = "tag=212631, 50% split vs 100% split" 
    abtest.set_cs(13449., 174044., 19688., 243131.)
    abtest.score_test()
    abtest.chi2test()


def main():
    test()

if __name__ == "__main__":
    main()
