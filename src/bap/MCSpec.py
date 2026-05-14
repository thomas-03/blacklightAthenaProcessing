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

    def __init__(self,directory,nproc,nfreq=None,emin=None,emax=None,listName=None,nout=1,outPath=None,overwrite=False):
        '''Initialize the MCSpec object by loading the spectra from the specified directory.'''
        if emin == None:
            inputFile = glob.glob(os.path.join(directory,'athinput.*'))

            if len(inputFile)>1:
                raise UserWarning('Multiple input files detected: '+inputFile+' \n Please specify which you want to use')
            
            nfreq,emin,emax = self.read_inputFile(inputFile[0])
        
        if listName is None:
            listFiles = glob.glob(os.path.join(directory,'*.list'))
            
            fileNameFormat = listFiles[0].split('/')[-1].split('.')
            outIndex = fileNameFormat.index('out1')
            listName = '.'.join(fileNameFormat[:outIndex+1])

        if outPath is None:
            outfile = os.path.join(directory,listName+".list")
            specFile = os.path.join(directory,listName+".spec")
            txtFile = os.path.join(directory,listName+".txt")
        else:
            if not os.path.isdir(outPath):
                os.makedirs(outPath)
            outfile = os.path.join(outPath,listName+".list")
            specFile = os.path.join(outPath,listName+".spec")
            txtFile = os.path.join(outPath,listName+".txt")
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
        if not os.path.isfile(txtFile) or overwrite:
            txtArgs = {'infile':specFile,'imu':'sum','iphi':'ave','xscale':'log','xmin':emin,'xmax':emax,'yscale':'log','ymin':None,'ymax':None,'xunit':'kev','yunit':'nulnu','ploterr':True,'outfile':None,'bbtemp':None,'bbnorm':None}
            self.freq,self.lum,self.lum_err = spec2txt.main(**txtArgs)
            self.freq = np.array(self.freq).reshape((nfreq,))
            self.lum = np.array(self.lum).reshape((nfreq,))
            self.lum_err = np.array(self.lum_err).reshape((nfreq,))
        else:
            mcResults = np.loadtxt(txtFile)
            self.freq = mcResults[:,0]
            self.lum = mcResults[:,1]
            self.lum_err = mcResults[:,2]

    

    def read_inputFile(self,inputFile):
        nfreq = 50 #default number of frequency bins to use if there are none \
        emin = None
        emax = None
        multRanges = False

        with open(inputFile,'r') as file:
            for line in file:
                line_txt = line.strip()
                if line_txt[:4]=='emin':
                    if emin == None:     
                        emin = float(line_txt.split('=')[-1])
                elif line_txt[:4]=='emax':
                    if emax == None:
                        emax = float(line_txt.split('=')[-1])
                elif line_txt[:5]=='nfreq':
                    if nfreq == None:
                        nfreq = int(line_txt.split('=')[-1])
                elif line_txt[:7]=='nf_scat':
                    nfreq = int(line_txt.split('=')[-1])
        return nfreq,emin,emax




#temp = MCSpec('/PellaShared/kcu8rf/spherical_compton_1e7/',32,overwrite=True)
