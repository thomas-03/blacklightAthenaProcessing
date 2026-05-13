from . import Image
import numpy as np

class MultiImageStruct:
    '''A structure that contains multiple Image objects for easy comparison'''

    def __init__(self,files,label_cat=None):
        raise UserWarning('Note that the MultiImageStruct is still being developed!')
        self.file_list = files
        self.nfiles = len(files)
        self.images = []
        for file in self.file_list:
            self.images.append(Image(file))

        self.label_cat = label_cat
        #determine what feature, if any, the distinguishing labels should be based on
        if self.label_cat=='inc':
            #TO DO!
            inc_sub = '_i'
            index = self.file_list[0].find(inc_sub)
            #this method of converting to an np array won't work so I should instead try a different method 
            self.labels = np.array(self.file_list)[:,index+2:]
