from numpy import pi, cos, sin, arctan2, polyval
from pymc import Uniform, Normal, deterministic, MCMC, MAP

from fpar import fpar

def bfitter(time, data):
  def fit_function(o, a1, a2, b1, b2, t):
    omega = 2.0*pi/24.0
    phase = omega*t
    a1 = polyval(a1, t)
    a2 = polyval(a2, t)
    b1 = polyval(b1, t)
    b2 = polyval(b2, t)
    return o + a1*cos(1.0*phase) + b1*sin(1.0*phase) + \
               a2*cos(2.0*phase) + b2*sin(2.0*phase)

  o = Uniform('offset',     lower =  0.0,   upper = 2.0)

  a1 = Uniform('cos1_factor', lower = -1.0e3, upper = 1.0e3, size=3,
               value=[0.0, 0.0, 1.0])
  a2 = Uniform('cos2_factor', lower = -1.0e3, upper = 1.0e3, size=3,
               value=[0.0, 0.0, 1.0])

  b1 = Uniform('sin1_factor', lower = -1.0e3, upper = 1.0e3, size=3,
               value=[0.0, 0.0, 1.0])
  b2 = Uniform('sin2_factor', lower = -1.0e3, upper = 1.0e3, size=3,
               value=[0.0, 0.0, 1.0])

  s = Uniform('sigma',      lower =  0.0,   upper = 1.0e1)

  @deterministic(plot=False)
  def modeled_data(t=time, a1=a1, a2=a2, b1=b1, b2=b2, o=o):
    return fit_function(o, a1, a2, b1, b2, t)

  @deterministic(plot=False)
  def phase(t=time, o=o, a=a1, b=b1):
    a = polyval(a, t)
    b = polyval(b, t)
    return arctan2(a, b)/pi

  y = Normal('y', mu = modeled_data, tau = 1.0/s/s, value=data,
             observed=True)

  m  = MCMC([o, a1, a2, b1, b2, s, modeled_data, y, phase])
  mp = MAP(m)
  mp.fit()

  def f(t):
    return fit_function(o.value, a1.value, a2.value,
                                 b1.value, b2.value, t)


  m.sample(3*10**4, 2*10**4)
  print 'fitting...'
  # mp.fit()
  print 'done.'

  om  = m.trace('offset')     [-100:].mean(0)
  a1m = m.trace('cos1_factor')[-100:].mean(0)
  a2m = m.trace('cos2_factor')[-100:].mean(0)
  b1m = m.trace('sin1_factor')[-100:].mean(0)
  b2m = m.trace('sin2_factor')[-100:].mean(0)

  def g(t):
    return fit_function(om, a1m, a2m, b1m, b2m, t)

  def h(t):
    return fit_function(o.value, a1.value, a2.value,
                                 b1.value, b2.value, t)

  return m, f, g, h
  # return m, g

