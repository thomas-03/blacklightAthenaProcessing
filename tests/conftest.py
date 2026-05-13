from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def repo_root():
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope='session')
def example_image_path(repo_root):
    path = repo_root / 'example_data' / 'ff_comp_tegan_T1e6_i0.npz'
    if not path.exists():
        raise FileNotFoundError(f"Required example image not found: {path}")
    return path
