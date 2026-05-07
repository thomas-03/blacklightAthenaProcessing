import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as cons
from scipy.optimize import curve_fit

def blackbody(frequency,temperature):
    '''Calculate the blackbody spectrum for a given frequency and temperature.'''
    h = cons.h.cgs.value
    kB = cons.k_B.cgs.value
    c = cons.c.cgs.value
    return (2*h*frequency**3/c**2) / (np.exp(h*frequency/(kB*temperature)) - 1)

def fit_blackbody(freqs,luminosities):
    '''Fit a blackbody to the given spectra.'''
    fit_temp, fit_cov = curve_fit(blackbody,freqs,luminosities)
    return fit_temp


def plot_spectra(image, ax=None, labels=None, plot_blackbody=False, temperature=None, plot_MC=False, MC_spec=None, MC_labels=None):
    '''Plot the spectra from one or multiple Image objects. Optionally also plot a blackbody spectrum and/or Monte Carlo spectra with error bars.
    
    Inputs:
    - image: an Image object or list of Image objects to plot
    - ax: a matplotlib axis to plot on (optional)
    - labels: a list of labels for the Image spectra (optional)
    - plot_blackbody: whether to plot a blackbody spectrum (optional)
    - temperature: the temperature to use for the blackbody spectrum (required if plot_blackbody is True)
    - plot_MC: whether to plot Monte Carlo spectra with error bars (optional)
    - MC_spec: a list of MCSpec objects to plot (required if plot_MC is True)
    - MC_labels: a list of labels for the MC spectra (optional)

    Output:
    - im: a list of matplotlib line objects for the Image spectra
    '''
    if not isinstance(image,list):
        image = [image]

    im = []
    for i in range(len(image)):
        frequencies = image[i].frequencies
        L = image[i].get_luminosity()
        if (ax is None) and i==0:
             ax = plt.gca()
            
        im.append(ax.plot(frequencies, L*frequencies,label=labels[i] if labels is not None else None))
    
    if plot_blackbody:
        if temperature is None:
            temperature = fit_blackbody(frequencies,L)
        bb_freq = np.logspace(np.log10(min(frequencies)), np.log10(max(frequencies)), 100)
        bb_flux = blackbody(bb_freq, temperature)
        ax.plot(bb_freq, bb_flux*bb_freq, label='Blackbody (T={0} K)'.format(temperature))
    
    if plot_MC:
        if not isinstance(MC_spec, list):
            MC_spec = [MC_spec]
        for i in range(len(MC_spec)):
            ax.errorbar(MC_spec[i][0], MC_spec[i][1]*MC_spec[i][0],yerr=MC_spec[i][2]*MC_spec[i][0], label=MC_labels[i] if MC_labels is not None else 'MC Spectrum {0}'.format(i))
    
    return im
