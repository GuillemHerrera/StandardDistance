# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QNEAT3 - Qgis Network Analysis Toolbox 3
 A QGIS processing provider for network analysis
 
 Qneat3Provider.py
 
-------------------
        begin                : 2018-01-15
        copyright            : (C) 2018 by Clemens Raffler
        email                : clemens.raffler@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from StandardDistance.StandardDistanceAlg import StandardDistance  

pluginPath = os.path.split(os.path.dirname(__file__))[0]

class StandardDistanceProvider(QgsProcessingProvider):
    def __init__(self):
        super().__init__()
        self.alglist = [
            StandardDistance()
        ]
                    
    def id(self, *args, **kwargs):
        return 'sdistance'

    def name(self, *args, **kwargs):
        return 'Standard Distance'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'StandardDistance', 'icon_StandardDistance.svg'))

    def loadAlgorithms(self, *args, **kwargs):
        for alg in self.alglist:
            self.addAlgorithm(alg)