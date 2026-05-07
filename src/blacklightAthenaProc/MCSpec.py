import numpy as np
import os
import glob
import sys

# append the path of the
# parent directory
sys.path.append("..")
from montecarlo import joinlists
from montecarlo import make_spectrum
from montecarlo import spec2txt

class MCSpec:
    '''Class to store Monte Carlo spectra (including error bars).'''

    def __init__(self,directory,nproc,nfreq,emin,emax,listName=None,nout=1,outPath=None,overwrite=False):
        '''Initialize the MCSpec object by loading the spectra from the specified directory.'''
        if listName is None:
            listFiles = glob.glob(os.path.join(directory,'*.list'))
            
            fileNameFormat = listFiles[0].split('/')[-1].split('.')
            outIndex = fileNameFormat.index('out1')
            listName = '.'.join(fileNameFormat[:outIndex+1])

        if outPath is None:
            outfile = os.path.join(directory,listName+".list")
            specFile = os.path.join(directory,listName+".spec")
        else:
            if not os.isdir(outPath):
                os.makedirs(outPath)
            outfile = os.path.join(outPath,listName+".list")
            specFile = os.path.join(outPath,listName+".spec")
        if not os.path.isfile(outfile) or overwrite:
            if nout == 1:
                listArgs = {'basename': os.path.join(directory,listName), 'nproc': nproc, 'start': 0, 'end': 0, 'skip': True,'multi_out': False, 'outfile': outfile, 'skip': False, 'rm': False}
            else:
                listArgs = {'basename': os.path.join(directory,listName), 'nproc': nproc, 'start': 0, 'end': nout-1, 'skip': True,'multi_out': False, 'outfile': outfile, 'skip': False, 'rm': False}
            joinlists.main(**listArgs)

        if not os.path.isfile(specFile) or overwrite:
            #go from list file to spec file
            specArgs = {'infile':outfile,'nx':nfreq,'xmin':emin,'xmax':emax,'nmu':1,'mumin':0,'mumax':1,'phimin':0,'phimax':2*np.pi,'anglebin':'cartesian','xaxis':'ev','linearx':False,'calclum':False,'screen':'no_screen','outfile':None,'yerror':True}
            make_spectrum.main(**specArgs)

        #now go from spec file to txt file
        txtArgs = {'infile':specFile,'imu':'sum','iphi':'ave','xscale':'log','xmin':emin,'xmax':emax,'yscale':'log','ymin':None,'ymax':None,'xunit':'kev','yunit':'nulnu','ploterr':True,'outfile':None,'bbtemp':None,'bbnorm':None}
        spec2txt.main(**txtArgs)

temp = MCSpec('/home/tegan/Research/blacklightAthenaProcessing/example_data/',32,50,1,1000,outPath='/home/tegan/Research/blacklightAthenaProcessing/example_output/')