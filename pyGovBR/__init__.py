# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:17:40 2018

@author: Lucas
"""


# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("pandas", "requests", "json","dateutil","bs4","requests")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError(
        "Missing required dependencies {0}".format(missing_dependencies))
del hard_dependencies, dependency, missing_dependencies

from pyGovBR.core.uasg import *
from pyGovBR.core.fornecedor import *