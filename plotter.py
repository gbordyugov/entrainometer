#!/usr/bin/python

from glob import glob
from re import search
from sys import stdin, argv, exit
from numpy import loadtxt, zeros_like, arange, pi, mean
from pylab import figure, gca
from pickle import load

def decimate(u, stride=5):
  return u[::stride]


def plot_zg_fit(dfit, tfit, ax=None, stride=5):
  if not ax: ax = gca()

  tmax = dfit[2]['time'].max()/24.0
  t = tfit[0]
  time = decimate(t['time'])/24.0
  data = decimate(t['temp'])
  fit  = decimate(t['fit' ])
  ax.plot(time, fit , 'b-')
  ax.plot(time, data, 'r.')
  ax.set_xlabel('time [d]')
  ax.set_ylabel('data (red), fit(blue)')


def plot_data_fit(dfit, tfit, ax=None, stride=5):
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


def loadfits(finput):
  fhandle = open(finput, 'r')
  di = load(fhandle)
  fhandle.close()
  
  dfit = di['datafit']
  tfit = di['tempfit']

  return dfit, tfit


def savestandardpdf(dfit, tfit, foutput):
  fig = figure(figsize=(3*4, 3.5))
  fig.subplots_adjust(hspace=0.25, wspace=0.3, left=0.07, right=0.98,
                                               bottom=0.16, top=0.80)
  n = 130
  ax1 = fig.add_subplot(n+1)
  ax2 = fig.add_subplot(n+2)
  ax3 = fig.add_subplot(n+3)

  plot_data_fit(dfit, tfit, ax1, 5)
  plot_period  (dfit, tfit, ax2, 5)
  plot_phase   (dfit, tfit, ax3, 5)

  fig.savefig(foutput)


def main(input_dir, output_dir):
  files = glob(input_dir+'/SCN*.pickle')
  files.sort()
  
  for finput in files:
    match = search("SCN(\d+)\.pickle", finput)
    scn = int(match.group(1))
  
    print "reading from %s"%finput
    dfit, tfit = loadfits(finput)
  
    foutput = output_dir + '/SCN%02d.pdf'%scn
    print 'exporting to %s'%foutput
    savestandardpdf(dfit, tfit, foutput)



#
# main entry point
#

if "__main__" == __name__:
  if len(argv) < 3:
    print 'using: entrainometer.py input_dir otput_dir'
    exit(-1)
  
  main(argv[1], argv[2])

