import ROOT

import sys

import numpy as np
import matplotlib.pylab as plt


f = ROOT.TFile(sys.argv[1])

tree = f.Get("Events")

# Uncomment this if you just want to see what is stored
# in the file.
#print("In the file...")
#f.ls()
#print("In the TTree....")
#tree.Print()
#exit()

nentries = tree.GetEntries()

values = []
valuesjet = []
valuesmet = [[],[]]
valueselectron = []

for nentry in range(nentries):

    if nentry%1000==0:
        print(nentry)

    tree.GetEntry(nentry)

    njets = tree.njet
    for i in range(0,njets):
        valuesjet.append(tree.jete[i])

#print(valuesjet)

plt.figure()
plt.hist(valuesjet,bins=100,range=(0,500))

#plt.show()


