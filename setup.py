#!/usr/bin/env python

#-----------------------------------------------------------------------------------------------------------------------
# INFO:
#-----------------------------------------------------------------------------------------------------------------------

"""
Author: Evan Hubinger
License: Apache 2.0
Description: Installer for the Coconut Programming Language.
"""

#-----------------------------------------------------------------------------------------------------------------------
# IMPORTS:
#-----------------------------------------------------------------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division

import setuptools

#-----------------------------------------------------------------------------------------------------------------------
# MAIN:
#-----------------------------------------------------------------------------------------------------------------------


setuptools.setup(
    name = "Event Display",
    version = 0.1,
    description = "Displayer a csv file containing an event, and the events vertieses.",
    author = "Fred Buchanan",
    author_email = "oscillator.b@gmail.com",
    install_requires = [
        "pyqtgraph"
        ],
    packages = setuptools.find_packages(),
    include_package_data = True,
    entry_points = {
        "console_scripts": [
            "event_display = EventDisplay.__main__:main"
            ],
        },
    )
