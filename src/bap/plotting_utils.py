import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as cons
from scipy.optimize import curve_fit
eV_2_erg = 1.60218e-12
h_ev = 4.135667662e-15
h_erg = 6.626e-27
kB=cons.k_B.cgs.value
c = 2.99792458e10
gg_msun = 1.32712440018e26

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


def plot_spectra(image, ax=None, labels=None, plot_blackbody=False, temperature=None, MC_spec=None, MC_labels=None,freq_units='eV'):
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
    if not isinstance(image, list):
        image = [image]
    
    if labels is not None and not isinstance(labels, list):
        raise TypeError("labels must be a list of strings, not a single string")
    
    if labels is not None and len(labels) != len(image):
        raise ValueError(f"labels must have same length as image list ({len(labels)} != {len(image)})")

    for i in range(len(image)):
        frequencies = image[i].frequencies
        L = image[i].get_luminosity()
        if (ax is None) and i==0:
             ax = plt.gca()
        if freq_units == 'eV':
            ax.plot(frequencies*h_ev, L*frequencies, label=labels[i] if labels is not None else None)
        else:
            ax.plot(frequencies, L*frequencies, label=labels[i] if labels is not None else None)
    
    if plot_blackbody:
        if temperature is None:
            temperature = fit_blackbody(frequencies,L)
        bb_freq = np.logspace(np.log10(min(frequencies)), np.log10(max(frequencies)), 100)
        bb_flux = blackbody(bb_freq, temperature)
        ax.plot(bb_freq, bb_flux*bb_freq, label='Blackbody (T={0:.2e} K)'.format(temperature))
    
    if MC_spec != None:
        if not isinstance(MC_spec, list):
            MC_spec = [MC_spec]
        #if not isinstance(MC_spec[0],MCSpec):
        #    raise TypeError('The MC_spec you want to plot must be an MCSpec object')
        for i in range(len(MC_spec)):
            if freq_units =='eV':
                ax.errorbar(MC_spec[i].freq*1e3, MC_spec[i].lum*MC_spec[i].freq,yerr=MC_spec[i].lum_err, label=MC_labels[i] if MC_labels is not None else 'MC Spectrum {0}'.format(i))
            else:
                ax.errorbar(MC_spec[i].freq*1e3/h_ev, MC_spec[i].lum*MC_spec[i].freq,yerr=MC_spec[i].lum_err, label=MC_labels[i] if MC_labels is not None else 'MC Spectrum {0}'.format(i))
    
    return ax

def plot_image(image,image_name,ax=None,axes='rg'):
    '''Plot an image'''