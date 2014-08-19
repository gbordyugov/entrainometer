#!/usr/bin/python

from os.path import join
from sys import stdin, argv, exit
from numpy import loadtxt, savetxt, zeros_like, arange, vstack, pi, mean,\
                  hypot
import pylab as p

from fitter import fitter

def save_graphics(s, dfit, tfit, output_dir, stride=5):
  def decimate(u, stride=5):
    return u[::stride]

  # fig = p.figure(figsize=(12, 3.5))
  fig = p.figure(figsize=(12, 3.5))
  fig.subplots_adjust(hspace=0.25, wspace=0.3, left=0.07,   right=0.98,
                                               bottom=0.16, top=0.80)
  ncolumns = 3
  tmax = dfit[2]['time'].max() / 24.0
  p.subplot(1, ncolumns, 1)
  for i in xrange(3):
    time = decimate(dfit[i]['time'])/24.0
    data = decimate(dfit[i]['data'])
    fit  = decimate(dfit[i]['fit' ])
    p.plot(time, fit , 'b-')
    p.plot(time, data, 'r.')
  p.xlim(00.0, tmax)
  p.xlabel('time [d]')
  p.ylabel('data (red), fit(blue)')

  ax = p.subplot(1, ncolumns, 2)
  for i in xrange(3):
    time = decimate(dfit[i]['time'  ])/24.0
    peri = decimate(dfit[i]['period'])
    p.plot(time, peri, 'b-', linewidth=2.0)
  p.xlabel('time [d]')
  p.ylabel('tau (blue), T (green) [h]')
  p.xlim(00.0, tmax)
  p.ylim(20.0, 27.0)

  time = decimate(tfit[1]['time'  ])/24.0
  pert = decimate(tfit[1]['period'])
  p.plot(time, pert, 'g--', linewidth=2.0)
  T = mean(pert)
  ax.annotate('T='+str(T), xy=(0.025, 0.975),
      xycoords='figure fraction', horizontalalignment='left',
      verticalalignment='top')

  temp = tfit[1]['temp']
  Z = (temp.max() - temp.min())/2
  ax.annotate('Z='+str(Z), xy=(0.975, 0.975),
      xycoords='figure fraction', horizontalalignment='right',
      verticalalignment='top')

  p.subplot(1, ncolumns, 3)
  time = decimate(dfit[1]['time'  ])/24.0
  tpha = decimate(tfit[1]['phase'])
  dpha = decimate(dfit[1]['phase'])
  dph  = (tpha - dpha)/2.0/pi*24.0
  p.plot(time, dph, 'b-', linewidth=2.0)
  p.xlabel('time [d]')
  p.ylabel('phase diff [h]')
  p.xlim(00.0, tmax)
  m = mean(dph)
  p.ylim(m - 6.0, m + 6.0)

  fname = join(output_dir, 'SCN'+str(scn)+'.pdf')
  p.savefig(fname)

  # fname = join(output_dir, 'SCN'+str(scn)+'.svg')
  # p.savefig(fname)
  p.close()


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

  dfit = {}; tfit = {}

  segs = segmenter(scn_time, scn_data, scn_temp)
  for (segno, seg) in enumerate(segs):
    time, data, temp = seg[0], seg[1], seg[2]

    # there can be some trailing zeros in the data
    while data[-1] == 0.0:
      time = time[:-1]
      data = data[:-1]
      temp = temp[:-1]

    dfit[segno] = {}; d = dfit[segno]
    print 'fitting data'
    d['time'] = time
    d['data'] = data
    d['phase'], d['period'], d['fit'], d['pars'] = fitter(time, data)

    if segno == 1:
      tfit[segno] = {}; t = tfit[segno]
      print 'fitting temperature'
      t['time'] = time
      t['temp'] = temp
      t['phase'], t['period'], t['fit'], t['pars'] = fitter(time, temp)

  save_graphics(scn, dfit, tfit, output_dir)
