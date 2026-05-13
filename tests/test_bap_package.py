import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import bap
from bap import Image, plot_spectra, plot_image


def test_bap_package_imports():
    assert hasattr(bap, 'Image')
    assert hasattr(bap, 'MCSpec')
    assert hasattr(bap, 'plot_spectra')
    assert hasattr(bap, 'h_ev')
    assert hasattr(bap, 'gg_msun')
    assert isinstance(bap.h_ev, float)
    assert isinstance(bap.c, float)
    assert bap.c > 0


def test_image_loads_example_file(example_image_path):
    img = Image(str(example_image_path))
    assert img.frequencies.ndim == 1
    assert img.frequencies.size > 0
    assert img.mass_msun > 0
    assert img.width_rg > 0
    assert img.distance > 0

    I = img.get_I()
    assert isinstance(I, np.ndarray)
    assert I.ndim == 3
    assert I.shape[0] == img.frequencies.size
    assert np.isfinite(I).any()




