from setuptools import setup, find_packages
from os import path

_dir = path.dirname(__file__)

with open(path.join(_dir, 'photofitt', 'version.py'), encoding="utf-8") as f:
    exec(f.read())

with open(path.join(_dir,'README.md'), encoding="utf-8") as f:
    long_description = f.read()

# parse_requirements() returns generator of pip.req.InstallRequirement objects

setup(
    name='photofitt',
    packages=find_packages(include=['photofitt', 'photofitt.*']),
    version=__version__,
    license='BSD 3-Clause License',
    description='PhotoFiTT: Phototoxicity Fitness Time Trial. Python package to measure cell arrestment and assess the temporal footprint of phototoxicity.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="M. del Rosario, E. Gomez-de-Mariscal, L. Morgado, G. Jacquemet, P.M. Pereira, R. Henriques",
    author_email='mrosario@igc.gulbenkian.pt, egomez@igc.gulbenkian.pt, rjhenriques@igc.gulbenkian.pt',
    url='https://github.com/HenriquesLab/photofitt',
    download_url='https://github.com/HenriquesLab/photofitt/archive/refs/tags/v1.0.0.tar.gz',
    keywords=['phototoxicity', 'cell arrestment', 'bioimage analysis', 'cell mitosis'],
    python_requires='>=3.11.9',
    install_requires=[
        'dask',
        'czifile==2019.7.2',
        'jupyter',
        'imageio==2.13.3',
        'matplotlib==3.5.1',
        'nd2==0.1.6',
        'numpy==1.22.4',
        'opencv-python==4.7.0.72',
        'pyyaml==6.0',
        'pandas==1.5.2',
        'pillow==8.4.0',
        'scipy==1.7.3',
        'scikit-image==0.19.1',
        'scikit-learn==1.2.1',
        'seaborn==0.12.2',
        'tifffile==2021.10.12',
        'toolz==0.11.2',
        'statsmodels'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
)
