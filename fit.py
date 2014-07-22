from scipy.optimize import leastsq
from fpar import fpar

def fit(t, x, f, pardict):
  """ fits x = x(t) by f(pardict, t) """

  def pars2arr(pd):
    """ given a dict of parameters pd, construct array arr """
    return [a for (k, p) in pd.items() for a in p.repr]

  def arr2pars(arr):
    """ given array arr, construct a dict of parameters dpars """
    dpars = {}
    for (k, p) in pardict.items():
      dpars[k] = fpar(p.f, arr[:len(p.repr)].tolist())
      arr = arr[len(p.repr):]
    return dpars

  def error(arr):
    return x - f(arr2pars(arr), t)

  newarr, succ = leastsq(error, pars2arr(pardict))
  return arr2pars(newarr), succ
