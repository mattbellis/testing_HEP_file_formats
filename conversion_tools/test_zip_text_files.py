import cms_tools as cms

import sys

import numpy as np
import matplotlib.pylab as plt


infilename = sys.argv[1]
collisions = cms.get_collisions_from_filename(infilename)

values = []
valuesjet = []
valuesmet = [[],[]]
valueselectron = []

for i,collision in enumerate(collisions):

    if i%1000==0:
        print(i)

    jets,muons,electrons,photons,met = collision

    for jet in jets:
        e,px,py,pz,btag = jet
        valuesjet.append(e)

#print(valuesjet)

plt.figure()
plt.hist(valuesjet,bins=100,range=(0,500))

#plt.show()


