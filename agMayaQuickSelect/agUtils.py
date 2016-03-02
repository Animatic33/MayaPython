# utils.py [part 1/4]
import json
import maya.cmds as cmds

def writeJsonFile(dataToWrite, fileName):
    if ".json" not in fileName:
        fileName += ".json"

    print "> write to json file is seeing: {0}".format(fileName)

    with open(fileName, "w") as jsonFile:
        json.dump(dataToWrite, jsonFile, indent=2)

    print "Data was successfully written to {0}".format(fileName)

    return fileName
    
# utils.py - [part 2/4]
def readJsonFile(fileName):
    try:
      with open(fileName, 'r') as jsonFile:
          return json.load(jsonFile)
    except:
        cmds.error("Could not read {0}".format(fileName))

#utils.py [part 3/4]
def geoInfo(vtx=0, geo=0, shape=0, skinC=0): # Returns a list of requested object strings
    returnValues = []
    
    selVTX = [x for x in cmds.ls(sl=1, fl=1) if ".vtx" in x]
    
    if len(selVTX) == 0:
        # geo can be of bool/int type or of string type.
        if type(geo) == int or type(geo) == bool:
            selGEO = cmds.ls(sl=1, objectsOnly=1)[0]
            
        elif type(geo) == str or type(geo) == unicode:
            selGEO = geo
            
        geoShape = cmds.listRelatives(selGEO, shapes=1)[0]
        
        # Deformed shapes occur when reference geometry has a deformer applied to it that is then cached
        # the additional section will take out the namespace of the shapefile (if it exists) and try to
        # apply the deform syntax on it.
        if ":" in geoShape: # the colon : deliminates namespace references
            deformShape = geoShape.partition(":")[2] + "Deformed"
            if len(cmds.ls(deformShape)) != 0:
                geoShape = deformShape
                print "deformed shape found: " + geoShape
    
    else:
        geoShape = selVTX[0].partition(".")[0] + "Shape"
        deformTest = geoShape.partition(":")[2] + "Deformed"
        if len(deformTest) != 0:
            geoShape = deformTest
            print "deformed shape found on selected vertices: " + geoShape
            
            # because the deformed shape is the object listed in the JSON file,
            # the word "Deformed" needs to be injected in the vertex name
            # and the namespace needs to be stripped out, because a deformed Shape is part of the local namespace
            for x in range( len(selVTX) ):
                selVTX[x] = ( selVTX[x].replace(".","ShapeDeformed.") ).partition(":")[2]
            
        selGEO = cmds.listRelatives(geoShape, p=1)[0]
        print geoShape + " | " + selGEO
    
    
    if vtx == 1:
        if len(selVTX) != 0: # if vertices are already selected, then we can take that list whole-sale.
            returnValues.append(selVTX)
        else:
            vtxIndexList = ["{0}.vtx[{1}]".format(geoShape, x) for x in cmds.getAttr ( geoShape + ".vrts", multiIndices=True)]
            returnValues.append(vtxIndexList)
    
    
    if geo == 1 or geo == True or type(geo) == str or type(geo) == unicode: 
        returnValues.append(selGEO)
    
    
    if shape == 1:
        returnValues.append(geoShape)
    
    
    if skinC == 1:
        skinClusterNM = [x for x in cmds.listHistory(geoShape) if cmds.nodeType(x) == "skinCluster" ][0]
        returnValues.append(skinClusterNM)
        
    return returnValues
    
#utils.py - [part 4/4]
def getVertexWeights(vertexList=[], skinCluster="", thresholdValue=0.001):
    if len(vertexList) != 0 and skinCluster != "":
        verticeDict = {}
        
        for vtx in vertexList:
            influenceVals = cmds.skinPercent(skinCluster, vtx, 
                                             q=1, v=1, ib=thresholdValue)
            
            influenceNames = cmds.skinPercent(skinCluster, vtx, 
                                              transform=None, q=1, 
                                              ib=thresholdValue) 
                        
            verticeDict[vtx] = zip(influenceNames, influenceVals)
        
        return verticeDict
    else:
        cmds.error("No Vertices or SkinCluster passed.")
