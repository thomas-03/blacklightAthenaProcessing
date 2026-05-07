import os
import numpy as np

def run_mult_inclinations(blacklight_path,base_input_file,base_output_name,ninc):
    i = np.linspace(0.0,180,ninc)

    for j in range(ninc):
        output_name= base_output_name+"_i{0}.npz".format(i[j])
        command = blacklight_path + " " + base_input_file + " --output_file="+output_name+" --camera_th={0}".format(i[j])
        os.system(command)


def produce_jobfile(blacklight_path):
    '''Produce a job file that runs multiple snapshots through blacklight with the same base input file'''
    #TO DO!!!!