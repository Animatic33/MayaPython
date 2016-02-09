"""
Quick History Selection UI for Maya (ver 0.45)
Scripting Language: PYTHON
Development Environment: Maya 2011 x64

Author: Andrew Glisinski
First Release: Feb 5 2016

Updates:
February 5 2016 - Initial Release (0.1)
February 6 2016 - Cycle Feature (0.2)
February 7 2016 - Set Feature (0.3)
                - List Organization (0.4)
February 8 2016 - Sort by Type (0.45)

Readme: Readme.md
Install Guide: InstallGuide.txt
"""
import maya.cmds as cmds

def selectHistoryUI(mainSelDict):
    windowWidth = 300
    windowHeight = 350
    horizontalSpacing = int(windowHeight * 0.01)
    verticalSpacing = int(windowWidth * 0.02)
    
    if cmds.window("selectHistory", q=1, exists=True):
        cmds.deleteUI("selectHistory")
    
    selectHistoryWindow = cmds.window("selectHistory", title = "Selection History",
                                      w=windowWidth, h=windowHeight,
                                      mnb=True, mxb=False, sizeable=False)
    #layout
    mainLayout = cmds.columnLayout("selhisLayout", rowSpacing=horizontalSpacing, w=windowWidth, h=windowHeight)
    
    cmds.text(label="Selection History Recorded: ", parent=mainLayout, width=windowWidth, align="center")
    
    selectHistoryLst = cmds.textScrollList("selectHistoryList", 
                                           deleteKeyCommand=lambda *args: selectHistoryCommand(mainSelDict, command="remove"), 
                                           doubleClickCommand= lambda *args: selectHistoryCommand(mainSelDict, command="select"),
                                           annotation="Tip: 'Double-click' to Select or 'Delete' key to Remove Selected Entry ", 
                                           width=windowWidth, 
                                           numberOfRows=8, 
                                           parent=mainLayout)
    
    optionPopup = cmds.popupMenu(parent=selectHistoryLst)
    cmds.menuItem(label="Sort Ascending", command= lambda *args: selectHistoryOrganize(mainSelDict, order="alpha"))
    cmds.menuItem(label="Sort Descending", command= lambda *args: selectHistoryOrganize(mainSelDict, order="alpha_ZA"))
    cmds.menuItem(label="Sort by Added", command= lambda *args: selectHistoryOrganize(mainSelDict, order="added"))
    cmds.menuItem(label="Sort by Type", command= lambda *args: selectHistoryOrganize(mainSelDict, order="type"))
    
    if len( mainSelDict.keys() ) > 0:
        for key in mainSelDict.keys():
            cmds.textScrollList("selectHistoryList", e=1, append=key)
    
    cmds.text(label="Modify Current Selection in Scene: ", parent=mainLayout, width=windowWidth, align="center")
    cmds.radioButtonGrp("selectType", width=windowWidth, labelArray3=['Single', 'Add', 'Remove'], select=1, numberOfRadioButtons=3 )
    cmds.text(label="Comparitive Functions: ", parent=mainLayout, width=windowWidth, align="center")
    cmds.radioButtonGrp("setSpecific", width=windowWidth, labelArray3=['None', 'Common', 'Difference'], select=1, numberOfRadioButtons=3 )

    cmds.button("SelectButton", label="Select", 
                backgroundColor=[0.37993082404136658, 0.60194522142410278, 0.71764707565307617], 
                width=windowWidth, 
                c=lambda *args: selectHistoryCommand(mainSelDict, command="select"), 
                parent=mainLayout)
    
    cycleButtonLayout = cmds.rowLayout("cycButLayout", numberOfColumns=2, w=windowWidth, parent=mainLayout)
    cmds.button("cycBack", label="<< Cycle Backward", 
                backgroundColor=[0.58823531866073608, 0.57949936389923096, 0.48442909121513367], 
                width=windowWidth/2, 
                c=lambda *args: selectHistoryCommand(mainSelDict, command="cycle", iterDir="backward"), 
                parent=cycleButtonLayout)
    cmds.button("cycForward", label="Cycle Forward >>", 
                backgroundColor=[0.58823531866073608, 0.57949936389923096, 0.48442909121513367], 
                width=windowWidth/2, 
                c=lambda *args: selectHistoryCommand(mainSelDict, command="cycle"), 
                parent=cycleButtonLayout)
    
    
    cmds.separator(parent=mainLayout)
    
    cmds.text(label="Nickname (Alias) for Selection: ", parent=mainLayout, width=windowWidth, align="center")
    reqName = cmds.textField("selNickname", width=windowWidth, 
                             annotation="Tip: Keypad 'Enter' key to add entry", 
                             enterCommand=lambda *args: selectHistoryCommand(mainSelDict, command="add"), 
                             parent=mainLayout)
    
    cmds.button("AddSelection", label="Add Selection", 
                backgroundColor=[0.46045002341270447, 0.81176471710205078, 0.41065746545791626], 
                width=windowWidth, 
                c= lambda *args: selectHistoryCommand(mainSelDict, command="add"), 
                parent = mainLayout)
    
    cmds.showWindow(selectHistoryWindow)

def selectHistoryOrganize(mainSelDict, order="alpha"): # organization is purely UI based. Do not touch the dictionary
    listOfSel = cmds.textScrollList("selectHistoryList", q=1, allItems=1)
    if "alpha" in order:
        if "_ZA" in order:
            listOfSel.sort(reverse=True)  # sort method returns none
        else:
            listOfSel.sort()
    elif order == "added":
        listOfSel = mainSelDict.keys()
    elif order == "type":
        tempTypeList = []
        for x in listOfSel: # get a list of [element, type]
            tempTypeList.append( [x, mainSelDict[x][2]] )
        tempTypeList.sort(key=lambda typeN: typeN[1])
        
        newSortedList = []
        for x in tempTypeList:
            newSortedList.append(x[0])
        
        listOfSel = newSortedList
    
    cmds.textScrollList("selectHistoryList", e=1, removeAll=1)
    cmds.textScrollList("selectHistoryList", e=1, append=listOfSel)
        
    
def selectHistoryCommand(mainSelDict, command="add", iterDir="forward"):
    
    # dictionary setup: {"listKey": [set( [objects] ), id]} -> where id is a pointer for cycle purposes, which entry should be accessed
    
    if command == "add":
        nickname = cmds.textField("selNickname", text=1, q=1)
        selection = cmds.ls(sl=1, fl=1)
        typeOfSel = cmds.nodeType(selection[0]) # rough idea of what type the selection is, can be mixed type with groups of things, but focus on the first element
        
        if len( selection ) == 0:
            cmds.error("Nothing selected.")
        
        if nickname == "":
            nickname = "[{0} : {1}]".format(selection[0], selection[-1])
        else:
            nickname += " [{0} : {1}]".format(selection[0], selection[-1])
        
        cmds.textScrollList("selectHistoryList", e=1, append=nickname)
        
        mainSelDict[nickname] = [set(selection), 0, typeOfSel]
        
    elif command == "remove":
        indexToRemove = cmds.textScrollList("selectHistoryList", q=1, selectIndexedItem=1)
        nameToRemove = cmds.textScrollList("selectHistoryList", q=1, selectItem=1)[0]
        cmds.textScrollList("selectHistoryList", e=1, removeIndexedItem=indexToRemove)
        try:
            del mainSelDict[nameToRemove]
        except:
            cmds.error("Looks like {0} doesn't exist in the global dictionary.".format(itemSelected))
        
    elif command == "select":
        if cmds.textScrollList("selectHistoryList", q=1, selectItem=True) == None:
            cmds.error("No Nicknames Selected.")
        
        enumSelect = cmds.radioButtonGrp("selectType", q=1, select=1)
        if   enumSelect <= 1:
             addV = 0
             remV = 0
        elif enumSelect == 2:
             addV = 1
             remV = 0
        elif enumSelect == 3:
             addV = 0
             remV = 1
        
        indexSelected = cmds.textScrollList("selectHistoryList", q=1, selectIndexedItem=True)[0]
        itemSelected = cmds.textScrollList("selectHistoryList", q=1, selectItem=1)[0]
        
        compareSelect = cmds.radioButtonGrp("setSpecific", q=1, select=1) # set-based comparative functions
        if compareSelect <= 1:
            selectionToMake = mainSelDict[itemSelected][0]
        elif compareSelect == 2: # if user wants to only get common elements
            selectionToMake = set(cmds.ls(sl=1, fl=1)) & mainSelDict[itemSelected][0]
        elif compareSelect == 3:
            selectionToMake = set(cmds.ls(sl=1, fl=1)) ^ mainSelDict[itemSelected][0]
        
        selectionToMake = list(selectionToMake)
        
        try:
            cmds.select( selectionToMake, add=addV, deselect= remV)
            mainSelDict[itemSelected][1] = 0 # reset the id to 0
        except:
            return None
            
    elif command == "cycle":
        if cmds.textScrollList("selectHistoryList", q=1, selectItem=True) == None:
            cmds.error("No Nicknames Selected.")
        
        enumSelect = cmds.radioButtonGrp("selectType", q=1, select=1)
        
        if   enumSelect <= 1:
             addV = 0
             remV = 0
        elif enumSelect == 2:
             addV = 1
             remV = 0
        elif enumSelect == 3:
             addV = 0
             remV = 1
        
        itemSelected = cmds.textScrollList("selectHistoryList", q=1, selectItem=1)[0]
        idPos = int( mainSelDict[itemSelected][1] )
        
        
        if iterDir == "forward":
            idPos += 1
        else:
            idPos -= 1
        
        if idPos > len( mainSelDict[itemSelected][0] ) -1: # make sure it doesn't go outside of the object range
            idPos = 0
        elif idPos < 0:
            idPos = len( mainSelDict[itemSelected][0] ) -1
        
                
        mainSelDict[itemSelected][1] = idPos
        
        cmds.select( list( mainSelDict[itemSelected][0] )[idPos], add=addV, deselect= remV ) # cast as a list first in order to use the idPos