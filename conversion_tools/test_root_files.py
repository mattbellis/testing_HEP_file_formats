import ROOT

import sys

import numpy as np
import matplotlib.pylab as plt


# Open the file and set the tree
f = ROOT.TFile(sys.argv[1])
tree = f.Get("Events")

tree.Print()

nentries = tree.GetEntries()

# Holder for your data
energies = []

for nentry in range(nentries):

    if nentry%10000==0:
        print(nentry)

    tree.GetEntry(nentry)

    njets = tree.njet
    for i in range(0,njets):
        energies.append(tree.jete[i])

    #x = tree.muone
    #y = tree.electrone

#print(energies)
print(len(energies))

plt.figure()
plt.hist(energies,bins=100,range=(0,500))

plt.show()


