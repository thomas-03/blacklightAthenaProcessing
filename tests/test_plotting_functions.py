import matplotlib
matplotlib.use('Agg')

import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.image import AxesImage
from bap import Image

from bap.plotting_utils import blackbody, fit_blackbody, plot_spectra, plot_image, colorbar
example_image_path = './example_data/exampleFile.npz'


def test_fit_blackbody_recovers_temperature():
    temperature = 2500.0
    freqs = np.logspace(13, 15, 8)
    luminosities = blackbody(freqs, temperature)

    fitted_temperature = fit_blackbody(freqs, luminosities)
    assert fitted_temperature == pytest.approx(temperature, rel=1e-3)

def test_fit_blackbody_recovers_temperature_from_real_image(example_image_path):
    img = Image(str(example_image_path))

    luminosities = img.get_luminosity()
    freqs = img.frequencies

    fitted_temperature = fit_blackbody(freqs, luminosities)
    assert fitted_temperature == pytest.approx(1e5, rel=1e-1)

def test_plot_spectra_with_real_image(example_image_path):
    img = Image(str(example_image_path))
    fig, ax = plt.subplots()
    plot_spectra(img, ax=ax, labels=['example'])

    assert len(ax.lines) == 1
    assert ax.lines[0].get_label() == 'example'


def test_plot_image_with_real_image(example_image_path):
    img = Image(str(example_image_path))
    fig, ax = plt.subplots()

    im = plot_image(img, 'I', ax=ax)
    assert hasattr(im, 'get_array')
    assert im.get_array().ndim == 2
    assert ax.get_xlabel() != ''
    assert ax.get_ylabel() != ''


test_fit_blackbody_recovers_temperature()
test_fit_blackbody_recovers_temperature_from_real_image(example_image_path)
test_plot_spectra_with_real_image(example_image_path)
test_plot_image_with_real_image(example_image_path)
test_plot_image_with_real_image(example_image_path)