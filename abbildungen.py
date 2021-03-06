#!/usr/bin/python

from matplotlib.pylab import figure, GridSpec
from plotter import loadfits, plot_data_fit, plot_periods, plot_phase
from bluebars import plot_bluebars

t2226dir = "data/t22-26/output/pickles/"
t24dir   = "data/t24/output/pickles/"

#
# Figure 1
#
# SCN06
# SCN04

def dataplot(dfit, tfit, ax, stride=5):
  plot_bluebars(dfit[1]['time'], dfit[1]['data'], tfit[0]['temp'], ax)
  for i in xrange(3):
    t = dfit[i]['time'][::stride]/24.0
    d = dfit[i]['data'][::stride]
    ax.plot(t, d, color="red")

  ax.set_xlabel('time [d]')
  ax.set_ylabel('bioluminescence')

  ax.set_xlim(0.0, dfit[2]['time'].max()/24.0)
  ax.set_ylim(0.0, 2.0)


def datafitplot(dfit, tfit, ax, stride=5):
  plot_bluebars(dfit[1]['time'], dfit[1]['data'], tfit[0]['temp'], ax)
  for i in xrange(3):
    t = dfit[i]['time'][::stride]/24.0
    d = dfit[i]['data'][::stride]
    f = dfit[i][ 'fit'][::stride]
    ax.plot(t, f, "b-", linewidth=1)
    ax.plot(t, d, "r.")

  ax.set_xlabel('time [d]')
  ax.set_ylabel('bioluminescence')

  ax.set_xlim(0.0, dfit[2]['time'].max()/24.0)
  ax.set_ylim(0.0, 2.0)


fig = figure(figsize=(3*4, 1*3.0))
fig.subplots_adjust(hspace = 0.25, wspace = 0.30,
                    left   = 0.07, right  = 0.98,
                    bottom = 0.21, top    = 0.90)

ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

dfit, tfit = loadfits(t2226dir+"SCN06.pickle")
dataplot(dfit, tfit, ax1)
dfit, tfit = loadfits(t2226dir+"SCN04.pickle")
dataplot(dfit, tfit, ax2)

ax1.text(0.9, 0.87, "(A)", transform=ax1.transAxes)
ax2.text(0.9, 0.87, "(B)", transform=ax2.transAxes)
# ax3.text(0.85, 0.07, "(C)", transform=ax3.transAxes)

fig.savefig('first.pdf')
fig.savefig('first.tiff')



#
# figure second
#

dfit, tfit = loadfits(t24dir+"SCN05.pickle")
fig = figure(figsize=(3*4, 2*3.0))
fig.subplots_adjust(hspace = 0.32, wspace = 0.25,
                    left   = 0.07, right  = 0.98,
                    bottom = 0.11, top    = 0.97)


gridspec = GridSpec(2, 2)
subplotspec = gridspec.new_subplotspec((0,0),rowspan=1,colspan=2)
ax1 = fig.add_subplot(subplotspec)
subplotspec = gridspec.new_subplotspec((1,0),rowspan=1,colspan=1)
ax2 = fig.add_subplot(subplotspec)
subplotspec = gridspec.new_subplotspec((1,1),rowspan=1,colspan=1)
ax3 = fig.add_subplot(subplotspec)

datafitplot(dfit, tfit, ax1, 7)

#
# ax2
# 

for i in xrange(3):
  t = dfit[i]['time'][::5]/24.0
  p = dfit[i]['period'][::5]
  ax2.plot(t, p, "b-")

ax2.plot([4.0, 20.0], [24.0, 24.0], "g--")

ax2.set_xlim(0.0, dfit[2]['time'].max()/24.0)
ax2.set_ylim(24.0-3.0, 24.0+3.0)

ax2.set_xlabel("time [d]")
ax2.set_ylabel("period")

#
# ax3
#
plot_phase(dfit, tfit, ax3)
ax1.text(0.96, 0.07, "(A)", transform=ax1.transAxes)
ax2.text(0.90, 0.07, "(B)", transform=ax2.transAxes)
ax3.text(0.90, 0.07, "(C)", transform=ax3.transAxes)

fig.savefig('second.pdf')
fig.savefig('second.tiff')



#
# third figure
#

fig = figure(figsize=(3*4, 2*3.0))
fig.subplots_adjust(hspace = 0.32, wspace = 0.30,
                    left   = 0.07, right  = 0.98,
                    bottom = 0.11, top    = 0.97)

ax1 = fig.add_subplot(2, 3, 1)
ax2 = fig.add_subplot(2, 3, 2)
ax3 = fig.add_subplot(2, 3, 3)
ax4 = fig.add_subplot(2, 3, 4)
ax5 = fig.add_subplot(2, 3, 5)
ax6 = fig.add_subplot(2, 3, 6)

# SCN05
dfit, tfit = loadfits(t2226dir+"SCN05.pickle")
datafitplot(dfit, tfit, ax1, 10)
plot_phase(dfit, tfit, ax2)

# SCN03
dfit, tfit = loadfits(t2226dir+"SCN03.pickle")
datafitplot(dfit, tfit, ax4, 12)
plot_phase(dfit, tfit, ax5)

idxSmaller = [0, 1, 6, 7]
idxLarger  = [2, 4]
namesSmaller = [t2226dir+"SCN%02d.pickle"%i for i in idxSmaller]
namesLarger  = [t2226dir+"SCN%02d.pickle"%i for i in idxLarger ]
clrs         = ['blue', 'red', 'darkgreen', 'darkviolet']

def mplotphases(names, ax, colors):
  for (name, color) in zip(names, colors):
    dfit, tfit = loadfits(name)
    plot_phase(dfit, tfit, ax, 5, color)

mplotphases(namesLarger,  ax6, clrs)
mplotphases(namesSmaller, ax3, clrs)

ax1.text(0.85, 0.07, "(A)", transform=ax1.transAxes)
ax2.text(0.85, 0.07, "(B)", transform=ax2.transAxes)
ax3.text(0.85, 0.07, "(C)", transform=ax3.transAxes)
ax4.text(0.85, 0.07, "(D)", transform=ax4.transAxes)
ax5.text(0.85, 0.07, "(E)", transform=ax5.transAxes)
ax6.text(0.85, 0.07, "(F)", transform=ax6.transAxes)

fig.savefig("third.pdf")
fig.savefig("third.tiff")
