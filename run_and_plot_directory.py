#!/usr/bin/python
from src import bap
import argparse

def main(**kwargs):
    if kwargs['pylauncher']:
        from bap import run_pylauncher
        output=run_pylauncher(kwargs['blacklight_path'],kwargs['base_input_file'],kwargs['directory'],kwargs['ncores'])
    else:
        output = bap.produce_jobfile(kwargs['blacklight_path'],kwargs['base_input_file'],kwargs['directory'])
        bap.run_from_jobfile('./jobfile')
    
    bap.plot_manytimes_spectra(output, './time_series_spectra.png')
    
    

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('base_input_file',help='the name of the input file that you wish to use with blacklight')
    parser.add_argument('directory',help='the directory containing the .athdf or .phdf files you wish to image')
    parser.add_argument('-n','--ncores',type=int,default=4,help='number of cores to run this on')
    parser.add_argument('-p','--pylauncher',action='store_true',help='whether or not you want to use PyLauncher')
    parser.add_argument('--blacklight_path',default='./blacklight/bin/blacklight',help='path to the version of blacklight you wish to use')
    args=parser.parse_args()
    main(**vars(args))
    