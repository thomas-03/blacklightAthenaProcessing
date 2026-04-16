import numpy as np

class Image:
    def __init__(self,filename):
        self.filename = filename
        if self.filename[-4:]=='.npz':
            self.file = np.load(self.filename)
        else:
            #put here how we should read in other file formats
            raise NotImplementedError('File format not supported yet. Sorry!')
        self.frequencies = self.file['frequency'][:]
        #if(len(self.frequencies)>1):
        self.mass_msun = self.file['mass_msun'][0]
        self.width_rg = self.file['width_rg'][0]
        #else:
        #    self.mass_msun = self.file['mass_msun']
        #    self.width_rg = self.file['width_rg']
        self.adaptive_num_levels = self.file['adaptive_num_levels'][0]
        self.adaptive_num_blocks = self.file['adaptive_num_blocks'][0]
        
