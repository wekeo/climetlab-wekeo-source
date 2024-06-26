#!/usr/bin/env python
# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import io
import os

import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(file_path, encoding="utf-8").read()


version = "0.1.1"


setuptools.setup(
    name="climetlab-wekeo-source",
    version=version,
    description="WEkEO external source plugin",
    long_description=read("README.md"),
    author="Germano Guerrini",
    author_email="germano.guerrini@gmail.com",
    license="MIT License",
    url="https://github.com/wekeo/climetlab-wekeo-source",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["pyyaml", "climetlab", "hda"],
    zip_safe=True,
    entry_points={"climetlab.sources": ["wekeo = climetlab_wekeo_source:WekeoSource"]},
    keywords="meteorology",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
)
