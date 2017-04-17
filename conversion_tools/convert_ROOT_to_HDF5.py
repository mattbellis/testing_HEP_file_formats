import cms_tools as cms
import sys
import ROOT
from array import array

infilename = sys.argv[1]
hdffilename = "%s.hdf5" % (infilename.split(".")[0])
f = ROOT.TFile(infilename)

tree = f.Get("Events")

branches = tree.GetListOfBranches()

names = ['muon','electron','jet','photon']

data = {}

for branch in branches:
    name = branch.GetName()
    print(name)
    data[name] = []
    print(branch.GetTitle())

nentries = tree.GetEntries()

for i in range(0,nentries):

    tree.GetEvent(i)

    x = getattr(tree,'njet')
    print(x)

    for branch in branches:
        name = branch.GetName()
        x = getattr(tree,name)
        print(x)

    







