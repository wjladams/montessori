'''
Created on Mar 19, 2017

@author: wjadams
'''
from plotly.offline import iplot
import numpy as np

def bplot(exp, xmin=-1, xmax=1, npts=100):
    vs = exp.free_symbols
    step = (xmax - xmin)/npts
    if len(vs) != 1:
        raise Exception("Expression did not have 1 variable")
    else:
        var = vs.pop()
    xs = np.arange(xmin, xmax, step)
    ys = [float(exp.subs(var, val)) for val in xs]
    iplot([{"x":xs, "y":ys}])