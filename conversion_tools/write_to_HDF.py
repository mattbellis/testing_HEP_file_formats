import numpy as np
from hdf5_write import *

data = initialize()

create_entry(data,'jete',dtype=float,index='njet')
create_entry(data,'jetpx',dtype=float,index='njet')
create_entry(data,'jetpy',dtype=float,index='njet')
create_entry(data,'jetpz',dtype=float,index='njet')
create_entry(data,'njet',dtype=int)

event = create_single_event(data)

for i in range(0,1000):

    clear_event(event)

    njet = 5
    event['njet'] = njet

    for n in range(njet):
        event['jete'].append(np.random.random())
        event['jetpx'].append(np.random.random())
        event['jetpy'].append(np.random.random())
        event['jetpz'].append(np.random.random())

    fill(data,event)

hdfile = write_to_file('output.hdf5',data)

