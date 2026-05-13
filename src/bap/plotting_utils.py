import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.colors as colors
from matplotlib.colors import LogNorm
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from mpl_toolkits.axes_grid1 import make_axes_locatable
from . import Units

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
            ax.plot(frequencies*Units.h_ev, L*frequencies, label=labels[i] if labels is not None else 'Blacklight Spectrum {0}'.format(i))
        else:
            ax.plot(frequencies, L*frequencies, label=labels[i] if labels is not None else 'Blacklight Spectrum {0}'.format(i))
    
    if plot_blackbody:
        if temperature is None:
            temperature = fit_blackbody(frequencies,L)
        bb_freq = np.logspace(np.log10(min(frequencies)), np.log10(max(frequencies)), 100)
        bb_flux = blackbody(bb_freq, temperature)
        
        #TO DO: add the frequency dependent switch here
        if freq_units == 'eV':
            ax.plot(bb_freq*Units.h_ev, bb_flux*bb_freq, label='Blackbody (T={0:.2e} K)'.format(temperature))
        else:
            ax.plot(bb_freq, bb_flux*bb_freq, label='Blackbody (T={0:.2e} K)'.format(temperature))
    
    
    if MC_spec != None:
        if not isinstance(MC_spec, list):
            MC_spec = [MC_spec]
        #if not isinstance(MC_spec[0],MCSpec):
        #    raise TypeError('The MC_spec you want to plot must be an MCSpec object')
        for i in range(len(MC_spec)):
            if freq_units =='eV':
                ax.errorbar(MC_spec[i].freq*1e3, MC_spec[i].lum,yerr=MC_spec[i].lum_err, label=MC_labels[i] if MC_labels is not None else 'MC Spectrum {0}'.format(i))
            else:
                ax.errorbar(MC_spec[i].freq*1e3/Units.h_ev, MC_spec[i].lum,yerr=MC_spec[i].lum_err, label=MC_labels[i] if MC_labels is not None else 'MC Spectrum {0}'.format(i))
    
    ax.legend()
    ax.set_xlabel('$\\nu$ ['+freq_units+']')
    ax.set_ylabel('$\\nu L_\\nu$ [erg/s]')
    return ax

def plot_image(image,image_name,freq=0,ax=None,axes='rg',logc=False,cmin=None,cmax=None,level=0):
    '''Plot an image'''
    if axes == 'rg' or (axes is None and image.mass_msun is None):
        half_width = 0.5 * image.width_rg
        scale_exponent = int('{0:24.16e}'.format(half_width).split('e')[1])
        if scale_exponent in (0, 1):
            scale = 1.0
            x_label = r'$x$ ($GM/c^2$)'
            y_label = r'$y$ ($GM/c^2$)'
        else:
            scale = 10.0 ** scale_exponent
            x_label = r'$x$ ($10^{' + repr(scale_exponent) + r'}\ GM/c^2$)'
            y_label = r'$y$ ($10^{' + repr(scale_exponent) + r'}\ GM/c^2$)'
        half_width /= scale
        extent = np.array((-half_width, half_width, -half_width, half_width))

    # Calculate root grid in cm
    elif axes == 'cm':
        rg = Units.gg_msun * image.mass_msun / Units.c ** 2
        half_width = 0.5 * image.width_rg * rg
        scale_exponent = int('{0:24.16e}'.format(half_width).split('e')[1])
        if scale_exponent in (0, 1):
            scale = 1.0
            x_label = r'$x$ ($\mathrm{cm}$)'
            y_label = r'$y$ ($\mathrm{cm}$)'
        else:
            scale = 10.0 ** scale_exponent
            x_label = r'$x$ ($10^{' + repr(scale_exponent) + r'}\ \mathrm{cm}$)'
            y_label = r'$y$ ($10^{' + repr(scale_exponent) + r'}\ \mathrm{cm}$)'
        half_width /= scale
        extent = np.array((-half_width, half_width, -half_width, half_width))

    # Calculate root grid in muas
    else:
        rg = Units.gg_msun * image.mass_msun / Units.c ** 2
        half_width = np.arctan(0.5 * image.width_rg / (self.distance)) / Units.muas
        scale_exponent = int('{0:24.16e}'.format(half_width).split('e')[1])
        if scale_exponent in (0, 1):
            scale = 1.0
            x_label = r'$x$ ($\mathrm{\mu as}$)'
            y_label = r'$y$ ($\mathrm{\mu as}$)'
        else:
            scale = 10.0 ** scale_exponent
            x_label = r'$x$ ($10^{' + repr(scale_exponent) + r'}\ \mathrm{\mu as}$)'
            y_label = r'$y$ ($10^{' + repr(scale_exponent) + r'}\ \mathrm{\mu as}$)'
        half_width /= scale
        extent = np.array((-half_width, half_width, -half_width, half_width))

    if image_name=='I':
        pic = image.get_I(level)
    elif image_name=='Q':
        pic = image.get_Q(level)
    elif image_name=='U':
        pic = image.get_U(level)
    elif image_name=='V':
        pic = image.get_V(level)
    else:
        pic = image.get_Alternate_Image(image_name,level)
    if(pic.ndim==3):
        pic = pic[freq,:,:]
    if ax is None:
        ax = plt.gca()
    if logc:
        colorpic = ax.imshow(pic,extent=extent,norm=colors.LogNorm(vmin=cmin,vmax=cmax))
    else:
        colorpic = ax.imshow(pic,extent=extent)
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    #TO DO: add implementation to include proper title
    return colorpic

def colorbar(ax: Axes, im: AxesImage):
    """
    Add a color bar aligned to `im` neater than `fig.colorbar(im)`.
    https://stackoverflow.com/a/39938019/8954109
    """

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    return ax.figure.colorbar(im, cax=cax, orientation="vertical")