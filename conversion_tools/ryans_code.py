import h5py as hp
import numpy as np
import sys
sys.path.append("tools/")
import cms_tools as cms
import time

#Tools used to convert different data sets to hdf5
file = ""
fileName = ""
numColl = 0
collisions = 0

def create_file(event_name):
    fileName = event_name +'.hdf5' 
    file =  hp.File(fileName, "w")
    return file

    #CMS conversion, infile is directory of the CMS data file
    #HDF5 file must be empty*****
def cms_conversion(infile_Name):


    #outfile = hdFile
    #infile = open(infile_Name)
    outfilename = infile_Name.split('.')[0]

    # Compression?
    comp_type = None; comp_opts=None; 
    #comp_type = "gzip"; comp_opts=9; 
    #comp_type = "gzip"; comp_opts=9; 
    #comp_type = "lzf"; comp_opts=None; 
    comp_tag = ""
    if comp_type is not None:
        comp_tag = "_comp_%s" % (comp_type)
        if comp_opts is not None:
            comp_tag = "%s_opts_%d" % (comp_tag,comp_opts)

    outfilename = "%s%s" % (outfilename,comp_tag)

    print(outfilename)

    outfile = create_file(outfilename)

    global collisions
    print("Reading in the input file...")
    collisions = cms.get_collisions_from_filename(infile_Name)
    print("Read in the input file...")
    global numColl 
    numColl = len(collisions)

    #Creates the groups for each particle type
    jets = outfile.create_group("Jets")
    muons = outfile.create_group("Muons")
    electrons = outfile.create_group("Electrons")
    photons = outfile.create_group("Photons")
    met = outfile.create_group("MET")

    #Datasets for number of particles in each event
    nj = np.zeros(numColl,dtype=int)
    nm = np.zeros(numColl,dtype=int)
    ne = np.zeros(numColl,dtype=int)
    nph = np.zeros(numColl,dtype=int)
    for i in range(0,numColl):
        if i%1000==0:
            print(i)
        nj[i] = len(collisions[i][0])
        nm[i] = len(collisions[i][1])
        ne[i] = len(collisions[i][2])
        nph[i] = len(collisions[i][3])
    nJets = outfile.create_dataset('Jets/num', data=nj,compression=comp_type, compression_opts=comp_opts)
    nMuons = outfile.create_dataset('Muons/num',data=nm,compression=comp_type, compression_opts=comp_opts)
    nElectrons = outfile.create_dataset('Electrons/num',data=ne,compression=comp_type, compression_opts=comp_opts)
    nPhotons = outfile.create_dataset('Photons/num',data=nph,compression=comp_type, compression_opts=comp_opts)
    #Loads these datasets
    #for i in range(0,numColl):
        #nJets[i] = len(collisions[i][0])
        #nMuons[i] = len(collisions[i][1])
        #nElectrons[i] = len(collisions[i][2])
        #nPhotons[i] = len(collisions[i][3])

    #Load the data drom CMS data into the HDF5 format
    #Creates the data set and loads the data user loader function
    ####Loader method worked, now to load the rest of the data
    ######JETS#######
    print("Converting jets...")
    JetEnergies = outfile.create_dataset('Jets/Energy', data = loader(0,0),compression=comp_type, compression_opts=comp_opts)
    jetPx = outfile.create_dataset('Jets/PX', data = loader(0,1),compression=comp_type, compression_opts=comp_opts)
    jetPy = outfile.create_dataset('Jets/PY', data = loader(0,2),compression=comp_type, compression_opts=comp_opts)
    jetPy = outfile.create_dataset('Jets/PZ', data = loader(0,3),compression=comp_type, compression_opts=comp_opts)
    jetBtag = outfile.create_dataset('Jets/bTag', data = loader(0,4),compression=comp_type, compression_opts=comp_opts)
    #####MUONS########
    print("Converting muons...")
    MuonEnergies = outfile.create_dataset('Muons/Energy', data = loader(1,0),compression=comp_type, compression_opts=comp_opts)
    MuonsPx = outfile.create_dataset('Muons/PX', data = loader(1,1),compression=comp_type, compression_opts=comp_opts)
    MuonsPy = outfile.create_dataset('Muons/PY', data = loader(1,2),compression=comp_type, compression_opts=comp_opts)
    MuonsPy = outfile.create_dataset('Muons/PZ', data = loader(1,3),compression=comp_type, compression_opts=comp_opts)
    MuonsQ = outfile.create_dataset('Muons/Q', data = loader(1,4),compression=comp_type, compression_opts=comp_opts)
    #####ELECTRONS####
    print("Converting electrons...")
    ElecEnergies = outfile.create_dataset('Electrons/Energy', data = loader(2,0),compression=comp_type, compression_opts=comp_opts)
    ElecPx = outfile.create_dataset('Electrons/PX', data = loader(2,1),compression=comp_type, compression_opts=comp_opts)
    ElecPy = outfile.create_dataset('Electrons/PY', data = loader(2,2),compression=comp_type, compression_opts=comp_opts)
    ElecPy = outfile.create_dataset('Electrons/PZ', data = loader(2,3),compression=comp_type, compression_opts=comp_opts)
    ElecQ = outfile.create_dataset('Electrons/Q', data = loader(2,4),compression=comp_type, compression_opts=comp_opts)
    #####PHOTONS######
    print("Converting photons...")
    PhoEnergies = outfile.create_dataset('Photons/Energy', data = loader(3,0),compression=comp_type, compression_opts=comp_opts)
    PhoPx = outfile.create_dataset('Photons/PX', data = loader(3,1),compression=comp_type, compression_opts=comp_opts)
    PhoPy = outfile.create_dataset('Photons/PY', data = loader(3,2),compression=comp_type, compression_opts=comp_opts)
    PhoPy = outfile.create_dataset('Photons/PZ', data = loader(3,3),compression=comp_type, compression_opts=comp_opts)

    outfile.close()

        

###Returns data in the format of python arrays#######
###        Format: data[particle][event][collision][attribute]
def getData(Hdata):
    final = [] #The final array of all data
    #Unload Jets
    final.append(unLoader(0,Hdata))
    final.append(unLoader(1,Hdata))
    final.append(unLoader(2,Hdata))         
    final.append(unLoader(3,Hdata))
    return final


########Loader/Unloader Functions#############
#Loads or Unloads data from collisions array into a specific data set
##PARAMETERS##
#dataset - the dataset you want to load into
#particle - the particle you are targeting:
                                        # 0 - Jets
                                        # 1 - Muons
                                        # 2 - Electrons
                                        # 3 - Photons
#data - the data you are loading:
                              # 0 - Energy
                              # 1 - px
                              # 2 - py
                              # 3 - pz
                              # 4 - btag/q
def loader(particle, data):
    temp = []
    for i in range (0,numColl):
        nColl = len(collisions[i][particle])
        for k in range(0, nColl):
            temp.append(collisions[i][particle][k][data])
       
    return temp

def unLoader(particle, data):
    start = time.time()
    print("Getting things ready")
    final = []
    loc = 0
    event = 0
    p = ''
    if particle == 0:
        p = 'Jets'
    elif particle == 1:
        p = 'Muons'
    elif particle == 2:
        p = 'Electrons'
    elif particle == 3:
        p = 'Photons'
    dataset = data[p]
    collPerEvent = dataset['num']
    E = dataset['Energy']
    PX = dataset['PX']
    PY = dataset['PY']
    PZ = dataset['PZ']
    if particle == 0:
        bTagQ = dataset['bTag']
    elif particle == 1 or particle == 2:
        bTagQ = dataset['Q']
    end = time.time()
    print(("Time to run %f seconds" % (end-start)))
    print("Start of While loop")
    start = time.time()
    nevents = collPerEvent.size
    print(nevents)
    while event < nevents:
        temp = []
        numColl = collPerEvent[event]
        for i in range(0,numColl):
            temp2 = []
            temp2.append(E[loc])
            temp2.append(PX[loc])
            temp2.append(PY[loc])
            temp2.append(PZ[loc])
            if particle != 3:
                temp2.append(bTagQ[loc])
            temp.append(temp2)
            loc = loc+1    
        final.append(temp)
        event = event +1
    end = time.time()
    print("End of Loops")
    print(("Time to run %f seconds" % (end-start)))
    return final

#####SUM FUNCTION#####################
#Function that calculates the sum of a dataset of integers to index n
def totalSum (A,n):
    return A[0:n].sum()
    #Sum = 0;
    #for i in range(0, n):
    #    Sum += A[i]
    #return Sum


def getEvent (n, data):
    jetPos = totalSum(data['Jets/num'], n)
    muonPos = totalSum(data['Muons/num'],n)
    elecPos = totalSum(data['Electrons/num'], n)
    phoPos = totalSum(data['Photons/num'], n)
    
    jetData = []
    muonData = []
    elecData = []
    phoData = []
    
    for i in range(jetPos,jetPos+data['Jets/num'][n]):
        jetData.append(getParticle(0,i,data['Jets']))
    for i in range(muonPos,muonPos+data['Muons/num'][n]):
        muonData.append(getParticle(1,i,data['Muons']))
    for i in range(elecPos,elecPos+data['Electrons/num'][n]):
        elecData.append(getParticle(2,i,data['Electrons']))                   
    for i in range(phoPos,phoPos+data['Photons/num'][n]):
        phoData.append(getParticle(3,i,data['Photons']))
                       
    l = {'Jets':jetData, 'Muons':muonData, 'Electrons': elecData, 'Photons':phoData}
    return l                       
                           
                         
    
    
    
    
    
    
    
def getParticle(particle, n, dataset):
    if particle == 0:
        p = 'Jets'
    elif particle == 1:
        p = 'Muons'
    elif particle == 2:
        p = 'Electrons'
    elif particle == 3:
        p = 'Photons'
    E = dataset['Energy'][n]
    PX = dataset['PX'][n]
    PY = dataset['PY'][n]
    PZ = dataset['PZ'][n]
    if particle == 0:
        bTagQ = dataset['bTag'][n]
        l = {'Energy':E,'px':PX,'py':PY,'pz':PZ, 'btag':bTagQ}
    elif particle == 1 or particle == 2:
        bTagQ = dataset['Q'][n]
        l = {'Energy':E,'px':PX,'py':PY,'pz':PZ, 'Q':bTagQ}
    else:   
        l = {'Energy':E,'px':PX,'py':PY,'pz':PZ}
        
    return l
    
    
    
    
    
    
def getEventSimple(n, data):
    jetPos = totalSum(data['Jets/num'], n)
    muonPos = totalSum(data['Muons/num'],n)
    elecPos = totalSum(data['Electrons/num'], n)
    phoPos = totalSum(data['Photons/num'], n)
    
    jetData = [[],[],[],[],[]]
    muonData = [[],[],[],[],[]]
    elecData = [[],[],[],[],[]]
    phoData = [[],[],[],[]]
   
    
    for i in range(jetPos,jetPos+data['Jets/num'][n]):
        retData = getParticleSimple(0,i,data['Jets'])
        jetData[0].append(retData[0])
        jetData[1].append(retData[1])
        jetData[2].append(retData[2])
        jetData[3].append(retData[3])
        jetData[4].append(retData[4])                      
    for i in range(muonPos,muonPos+data['Muons/num'][n]):
        retData = getParticleSimple(1,i,data['Muons'])
        muonData[0].append(retData[0])
        muonData[1].append(retData[1])
        muonData[2].append(retData[2])
        muonData[3].append(retData[3])
        muonData[4].append(retData[4])
    for i in range(elecPos,elecPos+data['Electrons/num'][n]):
        retData = getParticleSimple(2,i,data['Electrons'])
        elecData[0].append(retData[0])
        elecData[1].append(retData[1])
        elecData[2].append(retData[2])
        elecData[3].append(retData[3])
        elecData[4].append(retData[4])
    for i in range(phoPos,phoPos+data['Photons/num'][n]):
        retData = getParticleSimple(3,i,data['Photons'])
        phoData[0].append(retData[0])
        phoData[1].append(retData[0])
        phoData[2].append(retData[0])
        phoData[3].append(retData[0])
    jetDataL = {'E':jetData[0], 'PX':jetData[1], 'PY':jetData[2], 'PZ':jetData[3], 'bTag':jetData[4]}
    muonDataL = {'E':muonData[0], 'PX':muonData[1], 'PY':muonData[2], 'PZ':muonData[3], 'Q':muonData[4]}
    elecDataL = {'E':elecData[0], 'PX':elecData[1], 'PY':elecData[2], 'PZ':elecData[3], 'Q':elecData[4]}
    phoDataL = {'E':phoData[0], 'PX':phoData[1], 'PY':phoData[2], 'PZ':phoData[3]}
    l = {'Jets':jetDataL, 'Muons':muonDataL, 'Electrons': elecDataL, 'Photons':phoDataL}
    return l         
    
def getParticleSimple(particle, n, dataset):
    if particle == 0:
        p = 'Jets'
    elif particle == 1:
        p = 'Muons'
    elif particle == 2:
        p = 'Electrons'
    elif particle == 3:
        p = 'Photons'
    E = dataset['Energy'][n]
    PX = dataset['PX'][n]
    PY = dataset['PY'][n]
    PZ = dataset['PZ'][n]
    if particle == 0:
        bTagQ = dataset['bTag'][n]
        l = [E, PX, PY, PZ, bTagQ]
    elif particle == 1 or particle == 2:
        bTagQ = dataset['Q'][n]
        l = [E, PX, PY, PZ, bTagQ]
    else:   
        l = [E, PX, PY, PZ]
        
    return l
    
    
    
    
    
    
    
    
