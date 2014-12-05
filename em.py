#!/usr/bin/python

from os.path import join
from sys import stdin, argv, exit
from numpy import loadtxt, zeros_like, arange, pi, mean
from pylab import figure, gca

from  fitter import  fitter
from hfitter import hfitter


def decimate(u, stride=5):
  return u[::stride]


def plot_fit(dfit, tfit, ax=None, stride=5):
  if not ax: ax = gca()

  tmax = dfit[2]['time'].max()/24.0
  for d in dfit:
    time = decimate(d['time'])/24.0
    data = decimate(d['data'])
    fit  = decimate(d['fit' ])
    ax.plot(time, fit , 'b-')
    ax.plot(time, data, 'r.')
  ax.set_xlim(00.0, tmax)
  ax.set_xlabel('time [d]')
  ax.set_ylabel('data (red), fit(blue)')


def plot_period(dfit, tfit, ax=None, stride=5):
  if not ax: ax = gca()

  for d in dfit:
    time = decimate(d['time'  ])/24.0
    peri = decimate(d['period'])
    ax.plot(time, peri, 'b-', linewidth=2.0)
  ax.set_xlabel('time [d]')
  ax.set_ylabel('tau (blue), T (green) [h]')
  ax.set_xlim(00.0, dfit[2]['time'].max()/24.0)
  ax.set_ylim(20.0, 27.0)

  time = decimate(tfit[0]['time'  ])/24.0
  pert = decimate(tfit[0]['period'])
  ax.plot(time, pert, 'g--', linewidth=2.0)
  T = mean(pert)
  ax.annotate('T='+str(T), xy=(0.025, 0.975),
      xycoords='figure fraction', horizontalalignment='left',
      verticalalignment='top')

  temp = tfit[0]['temp']
  Z = (temp.max() - temp.min())/2
  ax.annotate('Z='+str(Z), xy=(0.975, 0.975),
      xycoords='figure fraction', horizontalalignment='right',
      verticalalignment='top')


def plot_phase(dfit, tfit, ax=None, stride=5):
  if not ax: ax = gca()

  time = decimate(dfit[1]['time'  ])/24.0

  tpha = decimate(tfit[0]['phase'])
  dpha = decimate(dfit[1]['phase'])

  dph  = (tpha - dpha)/2.0/pi*24.0

  ax.plot(time, dph, 'b-', linewidth=2.0)

  ax.set_xlabel('time [d]')
  ax.set_ylabel('phase diff [h]')

  m = mean(dph)
  ax.set_xlim(00.0, dfit[2]['time'].max()/24.0)
  ax.set_ylim(m - 6.0, m + 6.0)


def segmenter(time, data, temp):
  dtemp = zeros_like(temp)
  dtemp[1:-1] = temp[2:] - temp[:-2]

  mask = zeros_like(time, dtype=bool)
  mask[1:-1] = (abs(dtemp[1:-1]) > 1.0e-3)

  ix = arange(time.shape[0])

  if len(ix[mask]) < 2:
    print 'too few temperature changes found'
    exit(-1)

  i = [0, ix[mask].min(), ix[mask].max(), len(time)]
  
  return [(time[a:b], data[a:b], temp[a:b])
         for (a,b) in zip(i[:-1], i[1:])]



# main entry point

if len(argv) < 3:
  print 'using: entrainometer.py data.txt split_dir'
  exit(-1)

filename   = argv[1]
output_dir = argv[2]

u = loadtxt(filename, unpack=True)
scn_time = u[0]

ncols = u.shape[0]
nSCN  = (ncols-1)/2

for scn in xrange(nSCN):
# for scn in xrange(1):
  print ''
  print 'SCN no', scn
  data_ix = 1 + scn*2
  temp_ix = data_ix + 1

  scn_data = u[data_ix]
  scn_temp = u[temp_ix]

  dfit = []
  tfit = []

  segs = segmenter(scn_time, scn_data, scn_temp)
  for (segno, seg) in enumerate(segs):
    time, data, temp = seg[0], seg[1], seg[2]

    # there can be some trailing zeros in the data
    while data[-1] == 0.0:
      time = time[:-1]
      data = data[:-1]
      temp = temp[:-1]

    d = {}
    print 'fitting data'
    d['time'] = time
    d['data'] = data
    d['phase'], d['period'], d['fit'], d['pars'] = fitter(time, data)
    dfit.append(d)

    if segno == 1:
      t = {}
      print 'fitting temperature'
      t['time'] = time
      t['temp'] = temp
      t['phase'], t['period'], t['fit'], t['pars'] = fitter(time, temp)
      tfit.append(t)

  fig = figure(figsize=(12, 3.5))
  fig.subplots_adjust(hspace=0.25, wspace=0.3, left=0.07,   right=0.98,
                                               bottom=0.16, top=0.80)
  ax1 = fig.add_subplot(131)
  ax2 = fig.add_subplot(132)
  ax3 = fig.add_subplot(133)
  plot_fit   (dfit, tfit, ax1, 5)
  plot_period(dfit, tfit, ax2, 5)
  plot_phase (dfit, tfit, ax3, 5)

  fname = output_dir + '/SCN%02d.pdf'%scn
  print 'exporting to %s'%fname
  fig.savefig(output_dir + '/SCN%02d.pdf'%scn)
