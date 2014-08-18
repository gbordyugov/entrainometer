from numpy import pi, linspace, cos, sin, loadtxt
from numpy.random import randn
from bfitter import bfitter

ppday = 100
ndays = 10
tau   = 24.0
sigma = 0.3
phase = pi/3.0

def signal(t):
  omega = 2.0*pi/tau
  return 1.0 + (1.0+t*0.1)*sin(omega*t + phase)

t = linspace(0.0, ndays*24.0, ppday*ndays+1)
data = signal(t) + randn(t.shape[0])*0.1

u = loadtxt('data/test.txt', unpack=True)
t    = u[0,::5]
data = u[1,::5]
