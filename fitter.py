#!/usr/bin/python

from sys        import stdin, stdout, argv
from getopt     import getopt
from numpy      import loadtxt, zeros_like, cos, sin, pi, polyval,\
                       arctan2, unwrap, vstack, savetxt

from numpy.linalg import norm

from fit import fit
from fpar import fpar 

def lininterp(t0, t1, x0, x1):
  def f(t):
    k = (x1-x0)/(t1-t0)
    return x0 + k*(t-t0)
  return f


def period(pars, t):
  """ given parameters and time, calculates the instantaneous period.
  Relies on model and phase """
  ph = phase(pars, t)

  dph = zeros_like(ph)
  dph[1:-1] = (ph[2:] - ph[:-2]) / (t[2:] - t[:-2])

  dph[ 0] = lininterp(t[ 1], t[ 2], dph[ 1], dph[ 2])(t[ 0])
  dph[-1] = lininterp(t[-3], t[-2], dph[-3], dph[-2])(t[-1])

  return 2.0*pi/dph


def phase(pars, t):
  c = pars['cos1'](t)
  s = pars['sin1'](t)
  # T = pars['period'](t)
  T = 24.0

  return unwrap(2.0*pi/T*t + arctan2(s, c))


def cname(i): return 'cos'+str(i)
def sname(i): return 'sin'+str(i)


def make_model(pars):
  def f(t):
    # period = pars['period'](t)
    period = 24.0
    offset = pars['offset'](t)

    phase = 2.0*pi/period*t
    x = offset

    i = 1
    while (cname(i) in pars) and (sname(i) in pars):
      c = pars[cname(i)](t)
      s = pars[sname(i)](t)
      x = x + c*sin(i*phase) + s*cos(i*phase)
      i = i + 1

    return x

  return f


def fit_oscillations(time, data, order, nmodes):
  def model(p, t):
    m = make_model(p)
    return m(t)

  def polynome(repr):
    return fpar(polyval, repr)

  # pars = {'period': polynome([24.0]),
  #         'offset': polynome([1.0])}
  pars = {'offset': polynome([1.0])}
  dummy_polynome = [0.0] * order

  for i in xrange(1, nmodes+1):
    pars[cname(i)] = polynome(dummy_polynome)
    pars[sname(i)] = polynome(dummy_polynome)

    pars, succ = fit(time, data, model, pars)
    if succ != 1:
      print 'success:', succ
    residual = norm(model(pars, time) - data)

  print 'residual:', residual

  return pars


def fitter(time, data, order=4, nmodes=4):
  par = fit_oscillations(time, data, order, nmodes)
  return phase(par, time), period(par, time), make_model(par)(time), par


def get_arguments(argv):
    d = {'--modes': 4, '--order': 4}
    opts, argv = getopt(argv, '', ['modes=', 'order='])
    d.update(dict(opts))
    return int(d['--modes']), int(d['--order'])


def main():
  modes, order = get_arguments(argv[1:])
  u = loadtxt(stdin, unpack=True)
  result = fitter(u[0], u[1], order, modes)
  savetxt(stdout, result.T, fmt='%.6e')

if __name__ == '__main__':
  main()
