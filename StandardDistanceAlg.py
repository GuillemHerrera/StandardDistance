# -*- coding: utf-8 -*-

from PyQt5.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsFields,
                       QgsField,
                       QgsFeature,
                       QgsGeometry,
                       QgsPointXY)
import os
#import processing

from StandardDistance.SDUtils import *

pluginPath = os.path.split(os.path.dirname(__file__))[0]

class StandardDistance(QgsProcessingAlgorithm):
    
    INPUT = 'INPUT'
    GBYFIELD = 'GBYFIELD'
    WFIELD = 'WFIELD'
    OUTPUT = 'OUTPUT'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'StandardDistance', 'icon_StandardDistance.svg'))
    
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return StandardDistance()

    def name(self):
        return 'standarddistance'

    def displayName(self):
        return self.tr('Standard Distance')

    def group(self):
        return self.tr('Standard Distance')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'vector'


    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
    
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT,
												              self.tr('Input layer'),
												              [QgsProcessing.TypeVectorPoint, QgsProcessing.TypeVectorPolygon]))
        self.addParameter(QgsProcessingParameterField(self.GBYFIELD,
									                  self.tr('Group_by field'), 
									                  parentLayerParameterName=self.INPUT, type=QgsProcessingParameterField.String,optional=True))
        self.addParameter(QgsProcessingParameterField(self.WFIELD,
									                  self.tr('Weight field'), 
									                  parentLayerParameterName=self.INPUT, type=QgsProcessingParameterField.Numeric,optional=True))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT,
        									                self.tr('Output layer')))

    def processAlgorithm(self, parameters, context, feedback):
    
        source = self.parameterAsSource(parameters,self.INPUT,context)
        gByField = self.parameterAsString(parameters,self.GBYFIELD,context)
        wField = self.parameterAsString(parameters,self.WFIELD,context)
      
        groupb = -1
        if gByField:
            groupb = source.fields().indexFromName(gByField)
        weight = -1
        if wField:
            weight = source.fields().indexFromName(wField)
        
        outFields = QgsFields()
        if groupb > -1:	
        	outFields.append(QgsField("Category", QVariant.String))
        outFields.append(QgsField("X", QVariant.Double))
        outFields.append(QgsField("Y",  QVariant.Double))
        outFields.append(QgsField("Standard_Distance", QVariant.Double))
        
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            outFields,
            source.wkbType(),
            source.sourceCrs()
        )
        
        if groupb < 0 and weight < 0:
            r = StandDistance(source)
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(r[0],r[1])).buffer(r[2],25))
            fet.setAttributes([r[0], r[1], r[2]])
            sink.addFeature(fet, QgsFeatureSink.FastInsert)

        if groupb > -1 and weight <0 :
            distResult = G_StandDistance(source, groupb)
        
            for k, v in distResult.items():
                fet = QgsFeature()
                fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(v[0],v[1])).buffer(v[2],25))
                fet.setAttributes([k, v[0], v[1], v[2]])
                sink.addFeature(fet, QgsFeatureSink.FastInsert)

        if groupb < 0 and weight > 0:
            w = W_StandDistance(source,weight)
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(w[0],w[1])).buffer(w[2],25))
            fet.setAttributes([w[0], w[1], w[2]])
            sink.addFeature(fet, QgsFeatureSink.FastInsert)

        if groupb > -1 and weight > -1:
            distResult = W_G_StandDistance(source, groupb, weight)
        
            for k, v in distResult.items():
                fet = QgsFeature()
                fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(v[0],v[1])).buffer(v[2],25))
                fet.setAttributes([k, v[0], v[1], v[2]])
                sink.addFeature(fet, QgsFeatureSink.FastInsert)
        
        return {self.OUTPUT:dest_id}
        
        
        

