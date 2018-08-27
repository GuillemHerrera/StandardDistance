
import statistics as s
import math 

def StandDistance(source):

    n=source.featureCount()
    meanXY=[0,0]

    for feat in source.getFeatures():
        meanXY[0] += feat.geometry().centroid().asPoint().x()
        meanXY[1] += feat.geometry().centroid().asPoint().y()

    meanXY[0]=meanXY[0]/n
    meanXY[1]=meanXY[1]/n
    #Standard Distance
    meanDistXY=[0,0]
    for feat in source.getFeatures():
        meanDistXY[0] += (feat.geometry().centroid().asPoint().x()-meanXY[0])**2
        meanDistXY[1] += (feat.geometry().centroid().asPoint().y()-meanXY[1])**2
   
    distResult=[meanXY[0],
                meanXY[1],
                math.sqrt((meanDistXY[0]/n)+(meanDistXY[1]/n))] 
    return distResult

def G_StandDistance(source, groupb):
    values = {}
    for feat in source.getFeatures():
        attrs = feat.attributes()
        try:        
            cat = unicode(attrs[groupb])
            cnt = 1
            if cat not in values:
                values[cat] = []
            values[cat].append(cnt)
        except:
            pass
    valuesDict={}
    for (cat, v) in values.items():
        valuesDict[cat]=[len(v)]
    #MEAN CENTER
    meanXY={n:[0,0] for n in valuesDict.keys()}

    for feat in source.getFeatures():
        gb=feat.attribute(groupb)
        meanXY[gb][0] += feat.geometry().centroid().asPoint().x()
        meanXY[gb][1] += feat.geometry().centroid().asPoint().y()
    
    for key, values in meanXY.items():
        values[0]=values[0]/valuesDict[key][0]
        values[1]=values[1]/valuesDict[key][0]

   #Standard Distance
    meanDistXY={n:[0,0] for n in valuesDict.keys()}
    for feat in source.getFeatures():
        gb=feat.attribute(groupb)
        meanDistXY[gb][0] += (feat.geometry().centroid().asPoint().x()-meanXY[gb][0])**2
        meanDistXY[gb][1] += (feat.geometry().centroid().asPoint().y()-meanXY[gb][1])**2
        
    DistResult={n:[0,0,0] for n in valuesDict.keys()}
    for key, values in DistResult.items():
        values[0]=meanXY[key][0]
        values[1]=meanXY[key][1]
        values[2]=math.sqrt((meanDistXY[key][0]/valuesDict[key][0])+(meanDistXY[key][1]/valuesDict[key][0]))

    return DistResult

def W_StandDistance(source, weight):
    meanWXY=[0,0,0]
    for feat in source.getFeatures():
        we=feat.attribute(weight)
        meanWXY[0] += feat.geometry().centroid().asPoint().x()*we
        meanWXY[1] += feat.geometry().centroid().asPoint().y()*we
        meanWXY[2] += we
    meanWXY[0]=meanWXY[0]/meanWXY[2]
    meanWXY[1]=meanWXY[1]/meanWXY[2]
    
    meanDistWXY=[0,0]
    for feat in source.getFeatures():
        we=feat.attribute(weight)
        meanDistWXY[0] += we*(feat.geometry().centroid().asPoint().x()-meanWXY[0])**2
        meanDistWXY[1] += we*(feat.geometry().centroid().asPoint().y()-meanWXY[1])**2
        
    DistWResult=[meanWXY[0],meanWXY[1],0]
    DistWResult[2]=math.sqrt((meanDistWXY[0]/meanWXY[2])+(meanDistWXY[1]/meanWXY[2]))
    return DistWResult

def W_G_StandDistance(source, groupb, weight):
       
    valuesDict=source.uniqueValues(groupb)

    #Mean WEIGHT Center
    meanWXY={n:[0,0,0] for n in valuesDict}
    for feat in source.getFeatures():
        gb=feat.attribute(groupb)
        we=feat.attribute(weight)
        meanWXY[gb][0] += feat.geometry().centroid().asPoint().x()*we
        meanWXY[gb][1] += feat.geometry().centroid().asPoint().y()*we
        meanWXY[gb][2] += we
    for key, values in meanWXY.items():
        values[0]=values[0]/values[2]
        values[1]=values[1]/values[2]
   
   #Standard Weighted Distance
    meanDistWXY={n:[0,0,0] for n in valuesDict}
    for feat in source.getFeatures():
        gb=feat.attribute(groupb)
        we=feat.attribute(weight)
        meanDistWXY[gb][0] += we*(feat.geometry().centroid().asPoint().x()-meanWXY[gb][0])**2
        meanDistWXY[gb][1] += we*(feat.geometry().centroid().asPoint().y()-meanWXY[gb][1])**2
        meanDistWXY[gb][2] += we
    DistWResult={n:[0,0,0] for n in valuesDict}
    for key, values in DistWResult.items():
        values[0]=meanWXY[key][0]
        values[1]=meanWXY[key][1]
        values[2]=math.sqrt((meanDistWXY[key][0]/meanDistWXY[key][2])+(meanDistWXY[key][1]/meanDistWXY[key][2]))
    return DistWResult