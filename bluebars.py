#!/usr/bin/python

from sys import argv
from numpy import zeros_like, abs, arange, loadtxt

from pylab import figure, plot, fill_between, xlim, ylim, xlabel, ylabel,\
                  savefig


def plot_scn(scn, time, data, temp):
  figure()
  time = time/24.0
  plot(time, data, '-')

  temp = temp-temp.min()
  temp = temp/temp.max()*2.0
  fill_between(time, 2.0, temp, color='blue', alpha=0.3)

  pdfname = output_dir + '/SCN%02d.pdf'%scn
  print 'plotting SCN %d into %s'%(scn, pdfname)
  xlabel('time [h]')

  xlim(time.min()-1.0, time.max()+1.0)
  savefig(pdfname)


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
  print 'using: entrainometer.py data.txt graphics_dir'
  exit(-1)

filename   = argv[1]
output_dir = argv[2]

u = loadtxt(filename, unpack=True)
scn_time = u[0]

ncols = u.shape[0]
nSCN  = (ncols-1)/2

for scn in xrange(nSCN):
# for scn in xrange(1):
  data_ix = 1 + scn*2
  temp_ix = data_ix + 1

  scn_data = u[data_ix]
  scn_temp = u[temp_ix]

  dfit = {}; tfit = {}

  segs = segmenter(scn_time, scn_data, scn_temp)
  seg = segs[1]
  time, data, temp = seg[0], seg[1], seg[2]

  # there can be some trailing zeros in the data
  while data[-1] == 0.0:
    time = time[:-1]
    data = data[:-1]
    temp = temp[:-1]
    
  plot_scn(scn, time, data, temp)

