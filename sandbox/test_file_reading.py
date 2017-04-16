import h5py as h5
import numpy as np

import matplotlib.pylab as plt

import time

from hep_hdf5_tools import hd5events,get_event

import sys

filename = sys.argv[1]

data,event = hd5events(filename,verbose=True)

nevents = 100000

energies = []

#x = data['Jets/Energy']

#'''
for i in range(0,nevents):

    if i%1000==0:
        print(i)

    get_event(event,data,n=i)

    energy = event['Jets/Energy']

    for e in energy:
        energies.append(e)

#'''







