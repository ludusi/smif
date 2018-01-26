#!/bin/bash
# This script is meant to be called by the "install" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.
#
# This script is taken from Scikit-Learn (http://scikit-learn.org/)
#
# THIS SCRIPT IS SUPPOSED TO BE AN EXAMPLE. MODIFY IT ACCORDING TO YOUR NEEDS!

set -e

if [[ "$DISTRIB" == "conda" ]]; then
    # Deactivate the travis-provided virtual environment and setup a
    # conda-based environment instead
    deactivate

    # Use the miniconda installer for faster download / install of conda
    # itself
    wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh \
        -O miniconda.sh
    chmod +x miniconda.sh && ./miniconda.sh -b -p $HOME/miniconda -f
    export PATH=$HOME/miniconda/bin:$PATH
    rm miniconda.sh -f
    conda update --yes conda

    # Configure the conda environment and put it in the path using the
    # provided versions
    conda config --add channels conda-forge
    conda create -n testenv --yes python=3.6 \
        fiona \
        flask \
        isodate \
        networkx \
        numpy \
        pint \
        python-dateutil \
        pyyaml \
        rtree \
        scikit-optimize \
        shapely
    source activate testenv

    if [[ "$COVERAGE" == "true" ]]; then
        conda install pytest pytest-cov codecov
    fi
fi
