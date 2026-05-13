import numpy as np

class Geodesics:

    def __init__(self,file_name,nfreqs,npix):
        self.file_name = file_name
        self.nfreqs = nfreqs
        self.npix = npix
        self.data = self.load_geodesics(self.file_name,self.nfreqs,self.npix)
        self.data['sample_pos'] = np.array(self.data['sample_pos']).reshape((self.npix,self.data['geodesic_num_steps'][0],4))
        self.data['sample_dir'] = np.array(self.data['sample_dir']).reshape((self.npix,self.data['geodesic_num_steps'][0],4))

    def load_geodesics(self,file_path,nfreqs,npix):
        data = {}
        
        try:
            with open(file_path, 'rb') as f:
                # 1. Read Camera Data 
                data['cam_x'] = np.fromfile(f, dtype='f8', count=4)
                data['u_con'] = np.fromfile(f, dtype='f8', count=4)
                data['u_cov'] = np.fromfile(f, dtype='f8', count=4) 
                data['norm_con'] = np.fromfile(f, dtype='f8', count=4) 
                data['norm_con_c'] = np.fromfile(f, dtype='f8', count=4)
                data['hor_con_c'] = np.fromfile(f, dtype='f8', count=4)
                data['vert_con_c'] = np.fromfile(f, dtype='f8', count=4) 


                data['camera_pos_n'] = np.fromfile(f, dtype='i4', count=5)
                data['camera_pos'] = np.fromfile(f, dtype='f8', count=4*npix) 
                data['camera_dir_n'] = np.fromfile(f, dtype='i4', count=5)
                data['camera_dir'] = np.fromfile(f, dtype='f8', count=4*npix)

                # 2. Read Image Data
                data['image_freq_n'] = np.fromfile(f, dtype='i4', count=5)
                data['image_frequencies'] = np.fromfile(f, dtype='f8', count=nfreqs)
                data['momentum_factors_n'] = np.fromfile(f,dtype='i4',count=5)
                data['momentum_factors'] = np.fromfile(f, dtype='f8', count=npix)

                # 3. Read Geodesic Steps
                data['geodesic_num_steps'] = np.fromfile(f, dtype='i4',count=1) 

                # 4. Read Sample Data
                data['sample_flags_n'] = np.fromfile(f,dtype='i4',count=5)
                data['sample_flags'] = np.fromfile(f, dtype='?',count=npix)    # '?' for bool/char
                
                data['sample_num_n'] = np.fromfile(f,dtype='i4',count=5)
                data['sample_num'] = np.fromfile(f, dtype='i4',count=npix)
                
                data['sample_pos_n'] = np.fromfile(f,dtype='i4',count=5)
                data['sample_pos'] = np.fromfile(f, dtype='f8',count=4*npix*data['geodesic_num_steps'][0])
                data['sample_dir_n'] = np.fromfile(f,dtype='i4',count=5)
                data['sample_dir'] = np.fromfile(f, dtype='f8',count=4*npix*data['geodesic_num_steps'][0])

                data['sample_len_n'] = np.fromfile(f,dtype='i4',count=5)
                data['sample_len'] = np.fromfile(f, dtype='i4',count=npix*data['geodesic_num_steps'][0])
                
                return data

        except FileNotFoundError:
            print(f"Error: Could not open {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
