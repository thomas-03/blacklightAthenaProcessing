import numpy as np
import astropy.constants as cons

class Image:
    
    '''Class for loading and manipulating images from .npz files.'''
    h_ev = 4.135667662e-15
    eV_2_erg = 1.60218e-12 #check this!!
    h_erg = 6.626e-27
    kB=cons.k_B.cgs.value
    c = 2.99792458e10
    gg_msun = 1.32712440018e26


    def __init__(self,filename):
        '''Initialize the Image object by loading the .npz file and reading metadata.'''
        self.filename = filename
        if self.filename[-4:]=='.npz':
            try:
                self.file = np.load(self.filename)
            except:
                raise RuntimeError('File not found or otherwise unable to be read by numpy.')
        else:
            raise NotImplementedError('File format not supported yet. Sorry!')
        
        self.frequencies = self.file['frequency'][:]
        self.mass_msun = self.file['mass_msun'][0]
        self.width_rg = self.file['width'][0]
        self.distance = self.file['distance'][0]
        try:
            self.file['Q_nu']
            self.polarization = True
        except KeyError:
            self.polarization = False
        

        self.adaptive_num_levels = self.file['adaptive_num_levels'][0]
        
        if self.adaptive_num_levels > 0:
            self.adaptive_num_blocks = {}
            self.block_locs = {}
            self.adaptive_num_blocks[0] = self.file['adaptive_num_blocks'][0]
            
            for level in range(1, self.adaptive_num_levels + 1):
                self.adaptive_num_blocks[level] = self.file['adaptive_num_blocks'][level]
                self.block_locs[level] = self.file['adaptive_block_locs_{0}'.format(level)][:]
        self.image = None
        
        
    def load_image(self):
        '''Load the stokes parameters from the .npz file and store them in a dictionary.'''
        if self.image is not None:
            return self.image
        self.image = {}
        if self.adaptive_num_levels > 0:
            for level in range(1, self.adaptive_num_levels + 1):
                if self.polarization:
                    key_i = 'adaptive_I_nu_{0}'.format(level)
                    key_q = 'adaptive_Q_nu_{0}'.format(level)
                    key_u = 'adaptive_U_nu_{0}'.format(level)
                    key_v = 'adaptive_V_nu_{0}'.format(level)
                    i_nu = self.file[key_i][:]
                    q_nu = self.file[key_q][:]
                    u_nu = self.file[key_u][:]
                    v_nu = self.file[key_v][:]
                    self.image[level] = np.vstack((i_nu[None,:,:,:], q_nu[None,:,:,:], u_nu[None,:,:,:], v_nu[None,:,:,:]))
                else:
                    key_i = 'adaptive_I_nu_{0}'.format(level)
                    i_nu = self.file[key_i][:]
                    q_nu = np.zeros(i_nu.shape)*np.nan
                    u_nu = np.zeros(i_nu.shape)*np.nan
                    v_nu = np.zeros(i_nu.shape)*np.nan
                    self.image[level] = np.vstack((i_nu[None,:,:,:], q_nu[None,:,:,:], u_nu[None,:,:,:], v_nu[None,:,:,:]))
        else:
            if self.polarization:
                i_nu = self.file['I_nu'][:]
                q_nu = self.file['Q_nu'][:]
                u_nu = self.file['U_nu'][:]
                v_nu = self.file['V_nu'][:]
                self.image[0] = np.vstack((i_nu[None,:,:], q_nu[None,:,:], u_nu[None,:,:], v_nu[None,:,:]))
            else:
                i_nu = self.file['I_nu'][:]
                q_nu = np.zeros(i_nu.shape)*np.nan
                u_nu = np.zeros(i_nu.shape)*np.nan
                v_nu = np.zeros(i_nu.shape)*np.nan
                self.image[0] = np.vstack((i_nu[None,:,:], q_nu[None,:,:], u_nu[None,:,:], v_nu[None,:,:]))
                #print("in this loop",self.image[0])
        
                

    
    def get_I(self, level=0):
        '''Get the intensity image for a given level. If the image has not been loaded yet, it will be loaded first.'''
        self.load_image()
        return self.image[level][0,:,:,:]

    def get_Q(self, level=0):
        '''Get the Q Stokes parameter for a given level. If the image has not been loaded yet, it will be loaded first.'''
        image = self.load_image()
        if self.polarization:
            return image[level][1,:,:,:]
        else:
            raise RuntimeError('No polarization data in file.')
    
    def get_U(self, level=0):
        '''Get the U Stokes parameter for a given level. If the image has not been loaded yet, it will be loaded first.'''
        image = self.load_image()
        if self.polarization:
            return image[level][2,:,:,:]
        else:
            raise RuntimeError('No polarization data in file.')
    
    def get_V(self, level=0):
        '''Get the V Stokes parameter for a given level. If the image has not been loaded yet, it will be loaded first.'''
        image = self.load_image()
        if self.polarization:
            return image[level][3,:,:,:]
        else:
            raise RuntimeError('No polarization data in file.')
    
    def get_Alternate_Image(self, image_name, level=0):
        '''Get an alternate image (e.g. optical depth) for a given level.'''
        try:
            alt_image = {}
            if self.adaptive_num_levels > 0:
                for level in range(1, self.adaptive_num_levels + 1):
                    key = '{0}_{1}'.format(image_name, level)
                    alt_image[level] = self.file[key][:]
            else:
                key = '{0}_0'.format(image_name)
                alt_image[0] = self.file[key][:]
            return alt_image
        except:
            raise RuntimeError('{0} not found in file.'.format(image_name))
    
    def get_flux(self):
        '''Calculate the spatially-averaged flux from the image.
        
        Inputs: 
        - distance: distance to the source in gravitational radii
        Outputs:
        - flux in erg/s/cm^2/Hz
        '''
        if self.adaptive_num_levels>0:
            raise NotImplementedError('Flux calculation not implemented for adaptive images yet.')
        else:
            image = self.get_I()
            image_width =  2*np.arctan(0.5*self.width_rg /(self.distance))
            flux = np.array([])
            for freq in range(len(self.frequencies)):
                tempImage = np.copy(image[freq,:,:])
                flux = np.append(flux, (np.nanmean(tempImage[np.isfinite(tempImage)])*image_width**2))
            
        return flux

    def get_luminosity(self):
        '''Calculate the luminosity from the flux and distance.

        Inputs: 
        - distance: distance to the source in gravitational radii
        Outputs:
        - luminosity in erg/s/Hz
        '''
        flux = self.get_flux()
        rg = self.gg_msun * self.mass_msun / (self.c ** 2)
        luminosity = 2*((rg*self.distance)**2)*flux
        return luminosity


        
        

        
        
