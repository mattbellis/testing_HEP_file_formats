import cms_tools as cms
import sys
import ROOT
from array import array

infilename = sys.argv[1]
collisions = cms.get_collisions_from_filename(infilename)

# Open the ROOT file
rootfilename = "%s.root" % (infilename.split(".")[0])
f = ROOT.TFile(rootfilename, "RECREATE")
f.cd()

tree = ROOT.TTree("Events", "Events")

# jets
njet = array('i', [-1])
tree.Branch('njet', njet, 'njet/I')
jetbtag = array('f', 16*[-1.])
tree.Branch('jetbtag', jetbtag, 'jetbtag[njet]/F')
jetpx = array('f', 16*[-1.])
tree.Branch('jetpx', jetpx, 'jetpx[njet]/F')
jetpy = array('f', 16*[-1.])
tree.Branch('jetpy', jetpy, 'jetpy[njet]/F')
jetpz = array('f', 16*[-1.])
tree.Branch('jetpz', jetpz, 'jetpz[njet]/F')
jete = array('f', 16*[-1.])
tree.Branch('jete', jete, 'jete[njet]/F')

# Muons
nmuon = array('i', [-1])
tree.Branch('nmuon', nmuon, 'nmuon/I')
muonq = array('f', 16*[-1.])
tree.Branch('muonq', muonq, 'muonq[nmuon]/F')
muonpx = array('f', 16*[-1.])
tree.Branch('muonpx', muonpx, 'muonpx[nmuon]/F')
muonpy = array('f', 16*[-1.])
tree.Branch('muonpy', muonpy, 'muonpy[nmuon]/F')
muonpz = array('f', 16*[-1.])
tree.Branch('muonpz', muonpz, 'muonpz[nmuon]/F')
muone = array('f', 16*[-1.])
tree.Branch('muone', muone, 'muone[nmuon]/F')


# electrons
nelectron = array('i', [-1])
tree.Branch('nelectron', nelectron, 'nelectron/I')
electronq = array('f', 16*[-1.])
tree.Branch('electronq', electronq, 'electronq[nelectron]/F')
electronpx = array('f', 16*[-1.])
tree.Branch('electronpx', electronpx, 'electronpx[nelectron]/F')
electronpy = array('f', 16*[-1.])
tree.Branch('electronpy', electronpy, 'electronpy[nelectron]/F')
electronpz = array('f', 16*[-1.])
tree.Branch('electronpz', electronpz, 'electronpz[nelectron]/F')
electrone = array('f', 16*[-1.])
tree.Branch('electrone', electrone, 'electrone[nelectron]/F')

# photons
nphoton = array('i', [-1])
tree.Branch('nphoton', nphoton, 'nphoton/I')
photonpx = array('f', 16*[-1.])
tree.Branch('photonpx', photonpx, 'photonpx[nphoton]/F')
photonpy = array('f', 16*[-1.])
tree.Branch('photonpy', photonpy, 'photonpy[nphoton]/F')
photonpz = array('f', 16*[-1.])
tree.Branch('photonpz', photonpz, 'photonpz[nphoton]/F')
photone = array('f', 16*[-1.])
tree.Branch('photone', photone, 'photone[nphoton]/F')

metx = array('f', [-1])
tree.Branch('metx', metx, 'metx/F')
mety = array('f', [-1])
tree.Branch('mety', mety, 'mety/F')



for collision in collisions:
    jets,muons,electrons,photons,met = collision

    njet[0] = len(jets)
    for i,jet in enumerate(jets):
        energy,px,py,pz,btag = jet
        jete[i] = energy
        jetpx[i] = px
        jetpy[i] = py
        jetpz[i] = pz
        jetbtag[i] = btag

    nmuon[0] = len(muons)
    for i,muon in enumerate(muons):
        energy,px,py,pz,q = muon
        muone[i] = energy
        muonpx[i] = px
        muonpy[i] = py
        muonpz[i] = pz
        muonq[i] = q

    nelectron[0] = len(electrons)
    for i,electron in enumerate(electrons):
        energy,px,py,pz,q = electron
        electrone[i] = energy
        electronpx[i] = px
        electronpy[i] = py
        electronpz[i] = pz
        electronq[i] = q

    nphoton[0] = len(photons)
    for i,photon in enumerate(photons):
        energy,px,py,pz = photon
        photone[i] = energy
        photonpx[i] = px
        photonpy[i] = py
        photonpz[i] = pz

    metx[0],mety[0] = met

    tree.Fill()

f.cd()
f.Write()
f.Close()
