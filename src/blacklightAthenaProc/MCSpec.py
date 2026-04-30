import numpy as np
import os
import glob
from montecarlo import joinlists

class MCSpec:
    '''Class to store Monte Carlo spectra (including error bars).'''

    def __init__(self,directory,nproc,nfreq,emin,emax,listName=None,nout=1):
        '''Initialize the MCSpec object by loading the spectra from the specified directory.'''
        if listName is None:
            listFiles = glob.glob(os.path.join(directory,'*.list'))
            
            fileNameFormat = listFiles[0].split('/')[-1].split('.')
            outIndex = fileNameFormat.index('out1')
            listName = '.'.join(fileNameFormat[:outIndex+1])
        
        if nout == 1:
            listArgs = {'basename': os.path.join(directory,listName), 'nproc': nproc, 'start': 0, 'end': 0, 'skip': True,'multi_out': False, 'outfile': None, 'skip': False, 'rm': False}
        else:
            listArgs = {'basename': os.path.join(directory,listName), 'nproc': nproc, 'start': 0, 'end': nout-1, 'skip': True,'multi_out': False, 'outfile': None, 'skip': False, 'rm': False}
        joinlists.main(listArgs)

        #TO DO: add second half that goes from list to spec file and then final part that goes from spec to txt

temp = MCSpec('/home/tegan/Research/blacklightAthenaProcessing/example_data/',50,1,1000)