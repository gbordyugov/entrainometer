#!/usr/bin/python

from numpy import loadtxt, zeros_like, arange, savetxt, vstack
from sys import argv, exit, stdout

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


def extractor(u):
  time = u[0]
  data = u[columnno]
  temp = u[tempno]
  
  segs = segmenter(time, data, temp)
  s = segs[sliceno]
  return s[0], s[1], s[2]


if __name__ == '__main__':
  if len(argv) < 4:
    print 'usage: extractor.py filename columnno sliceno [tempno]'
    exit(-1)
  
  filename =     argv[1]
  columnno = int(argv[2])
  sliceno  = int(argv[3])
  
  if len(argv) < 5:
    tempno = columnno+1
  else:
    tempno = int(argv[4])

  u = loadtxt(filename, unpack=True)
  time, data, temp = extractor(u)
  savetxt(stdout, vstack([time, data, temp]).T, fmt='%.9e')
