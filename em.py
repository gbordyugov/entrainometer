#!/usr/bin/python

from os.path import join
from sys import stdin, argv, exit
from numpy import loadtxt, zeros_like, arange
from pickle import dump, HIGHEST_PROTOCOL

from  fitter import  fitter
from hfitter import hfitter


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
  print 'using: entrainometer.py data.txt output_dir'
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
      t['phase'], t['period'], t['fit'], t['pars'] = fitter(time, temp, 4, 4)
      tfit.append(t)

  di = {}
  di['datafit'] = dfit
  di['tempfit'] = tfit

  fname = output_dir + '/SCN%02d.pickle'%scn
  fhandle = open(fname, 'w')
  dump(di, fhandle)
  fhandle.close()
