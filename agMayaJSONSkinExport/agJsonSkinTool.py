#jsonSkinTool.py [part 1/4]
import maya.cmds as cmds
import agUtils as utils
reload(utils)

def jsonWeightsUI(*args):
    if cmds.window("JSONWeightUI", q=1, exists=1) == True:
        cmds.deleteUI("JSONWeightUI")
    
    cmds.window("JSONWeightUI", width=500, 
                height=200, mxb=False, mnb=True)
    cmds.columnLayout("JSONWeightMainLayout", 
                      width=500, height=200, 
                      parent="JSONWeightUI")
    cmds.text(label="Import/Export File", 
              width=500, height=50, align="center")
    cmds.textFieldButtonGrp("FileNameDisplay", columnWidth=[[1,0],[2,350]], 
                            width=500, height=25, label="File: ", 
                            buttonLabel="Open", buttonCommand=jsonGetFileName )
    cmds.rowLayout("JSONWeightBtnLayout", numberOfColumns=2, 
                   width=500, height=100, parent="JSONWeightUI")
    cmds.button("ExportJSONButton", width=250, 
                label="Export JSON Weights", 
                command=exportWeightsJSON, 
                parent="JSONWeightBtnLayout")
    cmds.button("ImportJSONButton", 
                width=250, label="Import JSON Weights", 
                command=importWeightsJSON, 
                parent="JSONWeightBtnLayout")
    cmds.showWindow("JSONWeightUI")

#jsonSkinTools.py [part 2/4]
def jsonGetFileName(*args):
    jsonFilter = "*.json"
    fileNameDir = cmds.fileDialog2(fileFilter=jsonFilter, dialogStyle=2)[0]
    if fileNameDir != "":
        cmds.textFieldButtonGrp("FileNameDisplay", e=1, text=fileNameDir)
        
# jsonSkinTool.py [part 3/4]

def exportWeightsJSON(*args): # returns the filename that was written
    geoData = utils.geoInfo(vtx=1, geo=1, skinC=1)
    selVTX = geoData[0]
    selGEO = geoData[1]
    skinClusterNM = geoData[2]
    thV = 0.001

    vtxListFileName = cmds.textFieldButtonGrp("FileNameDisplay",
                                              q=1, text=1)

    # dictionary to hold all the vertice & relationships
    verticeDict = utils.getVertexWeights(vertexList=selVTX,
                                            skinCluster=skinClusterNM,
                                            thresholdValue=thV)

    if len(verticeDict) >= 1:
        utils.writeJsonFile(dataToWrite=verticeDict,
                                fileName=vtxListFileName)

        print "{0} vertices info was written to JSON file".format(len(verticeDict))
        return vtxListFileName

    else:
        cmds.error("No vertices selected to write to JSON")
        
# jsonSkinTool.py [part 4/4]
def importWeightsJSON(*args):
    importFile = cmds.textFieldButtonGrp("FileNameDisplay", q=1, text=1)
    print "Accessing {0}".format(importFile)
    
    selectGeoData = utils.geoInfo(geo=1, skinC=1)
    geoName = selectGeoData[0]
    skinClusterNM = selectGeoData[1]
    
    vertData = utils.readJsonFile(importFile)   
    
    if len(vertData) > 0:
        
        for key in vertData.keys():
            try:
                cmds.skinPercent(skinClusterNM, key, tv=vertData[key], zri=1)
            except:
                cmds.error("Something went wrong with the skinning")
        print "{0} vertices were set to specificed values.".format(len(vertData.keys())) ##
    else:
        cmds.error("JSON File was empty ")