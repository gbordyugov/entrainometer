from numpy import unwrap, arctan2, imag, real, zeros_like, pi
from scipy.signal import hilbert

# def fitter(time, data, order=4, nmodes=4):
#   par = fit_oscillations(time, data, order, nmodes)
#   return phase(par, time), period(par, time), make_model(par)(time), par

def lininterp(t0, t1, x0, x1):
  k = (x1-x0)/(t1-t0)
  def f(t):
    return x0 + k*(t-t0)
  return f


def period(phase, t):
  dph = zeros_like(phase)
  dph[1:-1] = (phase[2:] - phase[:-2]) / (t[2:] - t[:-2])

  dph[ 0] = lininterp(t[ 1], t[ 2], dph[ 1], dph[ 2])(t[ 0])
  dph[-1] = lininterp(t[-3], t[-2], dph[-3], dph[-2])(t[-1])

  return 2.0*pi/dph


def phase(x, y):
  return unwrap(arctan2(y,x))

def hfitter(time, data):
  z = hilbert(data, 32)
  x, y  = real(z), imag(z)

  ph = phase(x-x.mean(), y)
  pe = period(ph, time)

  return ph, pe, data, None

