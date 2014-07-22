from numpy import linspace, select, zeros_like, hypot, pi, vstack, \
                  savetxt
from scipy.integrate import odeint

daylength = 24.0
ndays = 20
T     = ndays * daylength

ppd   = 100 # points per days

def periodic(t, T):
  reminder = t%T
  conds   = [reminder < 12.0, reminder >= 12.0]
  choices = [-1.0, 1.0]
  return select(conds, choices)

def zeitgeber(t):
  a = 1.0*T/4.0
  b = 3.0*T/4.0
  s = (t - a)*(t - b)
  conds = [s <= 0.0, s > 0.0]
  choices = [0.05, 0.0]
  a = select(conds, choices)
  return a * periodic(t, 24.0)

tau = 22.0
omega = 2.0*pi/tau
def rhs(u, t):

  def nonlin(x, y):
    r = hypot(x, y)
    r2 = r*r

    fx = (1.0 - r)*x - omega*y
    fy = (1.0 - r)*y + omega*x
    return fx, fy


  f = zeros_like(u)

  rhs1 = nonlin(u[0], u[1])
  rhs2 = nonlin(u[2], u[3])

  f[0] = rhs1[0]
  f[1] = rhs1[1]
  f[2] = rhs2[0] + zeitgeber(t)
  f[3] = rhs2[1]


  return f

t = linspace(0.0, T, ppd*ndays+1)

ic = [0.0, 1.0]*2

s = odeint(rhs, ic, t)

s = s.T
# output = vstack([t, s[0], zeitgeber(t), s[2], zeitgeber(t)]).T
output = vstack([t, s[2], zeitgeber(t)]).T
savetxt('test.txt', output, fmt='%.6e')
