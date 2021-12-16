# Copyright 2020 by Hector Urendez. All Rights Reserved.

import maya.cmds as cmds
from functools import partial
import json
import os


actualPath=os.path.dirname(__file__)






#            ##########      The following functions are responsible for export and import      ##########
#            ##########       gears information, they are used on the UI's third TabLayout      ##########




def exportValues(fileName, filePath, *args):
    '''
    This function saves all the information of the gears attributes of the selected system and their controllers 
    position in a dictionary.
    '''
    fileName = cmds.textFieldGrp(fileName, q=1, tx=1)
    if fileName=='':
        cmds.error('please write a name for your system file')
    
    else:
        sel = cmds.ls(sl=True)
        if len(sel)==0:
            cmds.error('Nothing selected')
            
        elif len(sel)>1:
            cmds.error('Please select only one gear')
            
        elif len(sel)==1 and cmds.objExists('{}.externalRadius'.format(sel[0])):
            generalDic={}
            geoGroup = cmds.listRelatives(sel, p=1)
            #  A list with the gears in the system is created
            gearsGroup = cmds.listRelatives(geoGroup, c=1)
            for each in gearsGroup:
                firstShape = cmds.listRelatives(each, shapes=True)
                skinClusterExists = cmds.connectionInfo('{}.inMesh'.format(firstShape[0]), sfd=1)
                
                if skinClusterExists!='':
                    #  the gear controller is searched and its position in the space saved in a matrix
                    breakProcess=False
                    SkinClusterNode = skinClusterExists.split('.')
                    firstGearJointPlug = cmds.connectionInfo('{}.matrix[0]'.format(SkinClusterNode[0]), sfd=1)
                    firstGearJointNode = firstGearJointPlug.split('.')
                    firstGearJoint = firstGearJointNode[0]
                    firstGearJointPOS = cmds.listRelatives(firstGearJoint, p=1)
                    firstGearHierarchyJoint = cmds.listRelatives(firstGearJointPOS, p=1)
                    parentConstraintQuery = cmds.connectionInfo('{}.translate.translateX'.format(firstGearHierarchyJoint[0]), id=1)
                    if parentConstraintQuery==True:
                        parentConstraintPlug = cmds.connectionInfo('{}.translate.translateX'.format(firstGearHierarchyJoint[0]),
                        sfd=1)
                        parentConstraintNode = parentConstraintPlug.split('.')
                        controllerPlug = cmds.connectionInfo('{}.target[0].targetParentMatrix'.format(parentConstraintNode[0]),
                        sfd=1)
                        controllerNode = controllerPlug.split('.')
                        matrix = cmds.xform(controllerNode[0], q=1, matrix=True, worldSpace=0)
                        
                    else:
                        masterGearHierarchyJoint = cmds.listRelatives(firstGearHierarchyJoint, p=1)
                        parentConstraintPlug = cmds.connectionInfo('{}.translate.translateX'.format(masterGearHierarchyJoint[0]),
                        sfd=1)
                        parentConstraintNode = parentConstraintPlug.split('.')
                        controllerPlug = cmds.connectionInfo('{}.target[0].targetParentMatrix'.format(parentConstraintNode[0]),
                        sfd=1)
                        controllerNode = controllerPlug.split('.')
                        matrix = cmds.xform(controllerNode[0], q=1, matrix=True, worldSpace=0)
                        
                    #  the other atributes of the list and the position matrix are saved in a dictionary for each gear
                    individualDic={}
                    internalRadiusCheck = cmds.getAttr('{}.internalRadiusCheck'.format(each))
                    internalRadius = cmds.getAttr('{}.internalRadius'.format(each))
                    internalTeethCheck = cmds.getAttr('{}.internalTeethCheck'.format(each))
                    internalTeeth = cmds.getAttr('{}.internalTeeth'.format(each))
                    internalTeethLength = cmds.getAttr('{}.internalTeethLength'.format(each))
                    externalTeethCheck = cmds.getAttr('{}.externalTeethCheck'.format(each))
                    externalTeeth = cmds.getAttr('{}.externalTeeth'.format(each))
                    externalTeethLength = cmds.getAttr('{}.externalTeethLength'.format(each))
                    externalRadius = cmds.getAttr('{}.externalRadius'.format(each))
                    heightGear = cmds.getAttr('{}.heightGear'.format(each))
                    name = cmds.getAttr('{}.name'.format(each))
                    order = cmds.getAttr('{}.order'.format(each))
                    connectedBy = cmds.getAttr('{}.connectedBy'.format(each))
                    lastRotationCtrl = cmds.getAttr('{}.lastRotationCtrl'.format(each))
                    lastRotationValue = cmds.getAttr('{}.lastRotationValue'.format(each))
                    lastGear = cmds.getAttr('{}.lastGear'.format(each))
                    individualDic.update({'internalRadiusCheck':internalRadiusCheck})
                    individualDic.update({'internalRadius':internalRadius})
                    individualDic.update({'internalTeethCheck':internalTeethCheck})
                    individualDic.update({'internalTeeth':internalTeeth})
                    individualDic.update({'internalTeethLength':internalTeethLength})
                    individualDic.update({'externalTeethCheck':externalTeethCheck})
                    individualDic.update({'externalTeeth':externalTeeth})
                    individualDic.update({'externalTeethLength':externalTeethLength})
                    individualDic.update({'externalRadius':externalRadius})
                    individualDic.update({'heightGear':heightGear})
                    individualDic.update({'name':name})
                    individualDic.update({'order':order})
                    individualDic.update({'connectedBy':connectedBy})
                    individualDic.update({'lastRotationCtrl':lastRotationCtrl})
                    individualDic.update({'lastRotationValue':lastRotationValue})
                    individualDic.update({'lastGear':lastGear})
                    individualDic.update({'position':matrix})
                    individualDic.update({'controllerName':controllerNode[0]})
                    generalDic.update({order:individualDic})
                    
                else:
                    breakProcess=True
                    cmds.error('please select a gear in system')
            
            if breakProcess==False:
                actualPath = cmds.textFieldGrp(filePath, q=1, tx=1)
                storeSelectedSystem(dictionaryAttrs=generalDic, path=actualPath, filename=fileName)
        
        

def storeSelectedSystem(dictionaryAttrs={}, path='', filename=''):
    '''
    This function converts the created dictionary in a json format.
    '''
    attrsData = dictionaryAttrs
    jsonFormat = json.dumps(attrsData, separators=(',',':'), indent=4)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            
        except:
            cmds.warning('Directory {} cannot be found'.format(path))
            return
            
    saveFile(path, '{}.json'.format(filename), content=jsonFormat)
    


def saveFile(path, filename, content):
    '''
    This function saves the dictionary in a json file in the selected path.
    '''
    if not os.path.exists(path):
        cmds.error('ERROR:{} does not exist'.format(path))
        
    elif content is None:
        cmds.error('ERROR: content is empty')
        
    #  the file is created and the dictionary saved
    filePath = os.path.join(path, filename)
    with open(filePath, 'w') as file_out:
        file_out.write(content)
    
    #  a playblast of the gear system is created and the image saved with the json file
    cmds.setAttr("defaultRenderGlobals.imageFormat", 32)
    cmds.select(d=1)
    imageFile=os.path.splitext(filename)
    cmds.playblast( fr=[1], fmt="image", os=True, v=False, orn=False, wh=(300, 300), 
    cf=r'{0}\{1}.png'.format(path, imageFile[0]))
    
    cmds.warning('content was saved successfully')



def importValues(fileName, filePath, *args):
    '''
    This function takes the name of the file and the name of the path from the UI.
    '''
    fileName = cmds.textFieldGrp(fileName, q=1, tx=1)
    actualPath = cmds.textFieldGrp(filePath, q=1, tx=1)
    createSelectedSystem(path=actualPath, filename=fileName)




def readFile(path, filename):
    '''
    This function reads the json file and return its information.
    '''
    actualPath = '{}\\{}.json'.format(path, filename)
    if not os.path.exists(actualPath):
        cmds.error('ERROR:{} no existe'.format(actualPath))
        return
    filePath = os.path.join(path, filename)
    
    with open(actualPath, 'r') as file_in:
        data = file_in.read()
        return data
        
        

def createSelectedSystem(path='', filename=''):
    '''
    This function convert the dictionaries in the json file in 'normal' dictionaries.
    '''
    data = readFile(path, filename)
    objAttrsData = json.loads(data)
    setGearAttrs(objAttrsData)
    
    

def setGearAttrs(object_data = {}):
    '''
    This function takes the information from the dictionary and recreate the gear system.
    '''
    list=[]
    for key in sorted(object_data):
        attributes = object_data[key]
        breakImport=False
        
        if attributes['name'] in cmds.ls():
            cmds.error('some names of the gears in the system you like to load are already in the scene')
            breakImport=True
            break
        #  gears are created with its attributes
        else:
            if key=='1.0':
                importedGear = gearCreation(radiusExt=attributes['externalRadius'],
                teethExtCheck=attributes['externalTeethCheck'], teethExt=attributes['externalTeeth'],
                radiusIntCheck=attributes['internalRadiusCheck'], radiusInt=attributes['internalRadius'],
                teethIntCheck=attributes['internalTeethCheck'], teethInt=attributes['internalTeeth'],
                heightGear=attributes['heightGear'], lengthExtTeeth=attributes['externalTeethLength'],
                lengthIntTeeth=attributes['internalTeethLength'], nameGear=attributes['name'], rotation=0)
                
            elif key=='2.0':
                lastGear = attributes['lastGear']
                cmds.select(lastGear)
                importedGear = rigConnections(externalSecondNumberRadius=attributes['externalRadius'], 
                internalSecondRadiusCheck=attributes['internalRadiusCheck'],
                internalSecondNumberRadius=attributes['internalRadius'],
                internalSecondTeethCheck=attributes['internalTeethCheck'],
                internalSecondNumberTeeth=attributes['internalTeeth'],
                optionTeeth=attributes['connectedBy'], numberSecondHeight=attributes['heightGear'],
                lengthSecondInternalTeeth=attributes['internalTeethLength'],
                lengthSecondExternalTeeth=attributes['externalTeethLength'], nameSecondGear=attributes['name'])
                
            else:
                lastGear = attributes['lastGear']
                cmds.select(lastGear)
                lastRotationCtrl = attributes['lastRotationCtrl']
                lastRotationValue = attributes['lastRotationValue']
                cmds.setAttr('{}.ry'.format(lastRotationCtrl), float(lastRotationValue))
                importedGear = rigConnections(externalSecondNumberRadius=attributes['externalRadius'], 
                internalSecondRadiusCheck=attributes['internalRadiusCheck'],
                internalSecondNumberRadius=attributes['internalRadius'],
                internalSecondTeethCheck=attributes['internalTeethCheck'],
                internalSecondNumberTeeth=attributes['internalTeeth'],
                optionTeeth=attributes['connectedBy'], numberSecondHeight=attributes['heightGear'], 
                lengthSecondInternalTeeth=attributes['internalTeethLength'],
                lengthSecondExternalTeeth=attributes['externalTeethLength'], nameSecondGear=attributes['name'])
    #  Position of the controllers is set
    if not breakImport==True:
        for gear, data  in object_data.items():
            cmds.xform(data['controllerName'], matrix = data['position'], ws=0)



def setLibrary(path, *args):
    '''
    This function takes the path from the UI.
    '''
    pathName = cmds.textFieldGrp(path, q=1, tx=1)
    loadLibrary(pathName)



def loadLibrary(path, *args):
    '''
    This function create a list with the json files in the path and send that information to the UI.
    '''
    ourPath=os.path.join(path)
    result=os.path.isdir(ourPath)
    systems=[]
    if result == True:
        for r, d, f in os.walk(ourPath):
            for files in f:
                if '.json' in files:
                    systems.append(files)
                    
    if len(systems)==0:
        cmds.warning('there are not library in {}'.format(path))
                    
    windowGearsFunction(libraryButtons=systems, libraryPath=ourPath)






#            ##########      The following functions are responsible for create the gear       ##########
#            ##########      specified by the UI, they are used on the UI's first TabLayout      ##########




def extrudeSides(teethNumber, objectSH, object, lengthTeeth, ExtInt, *args):
    '''
    This function extrudes faces of a cylinder according to the number of teeth.
    '''
    numberSubdivisions = 2*teethNumber
    translate = lengthTeeth/2
    cmds.setAttr('{}.subdivisionsAxis'.format(objectSH), numberSubdivisions)
    numberFaces = cmds.polyEvaluate(object, f=1)
    extrudeRange = numberFaces/3
    for x in range(extrudeRange):
        # Only even faces on the sides of the cylinder are extruded
        if x%2==0:
            # Internal teeth are more open so before extrude the faces are scaled
            if ExtInt=='Int':
                cmds.select('{}.f[{}]'.format(object, x))
                positions = cmds.xform( q=True, t=1 )
                positionX = (positions[3]-positions[0])/2+positions[0]
                positionY = positions[1]+positions[7]
                positionZ = (positions[2]-positions[5])/2+positions[5]
                cmds.scale(1.5, 1, 1.5, r=1, p=(positionX, positionY, positionZ))
                cmds.polyExtrudeFacet('{}.f[{}]'.format(object, x), ltz=translate, lsx=0.7)
                cmds.polyExtrudeFacet('{}.f[{}]'.format(object, x), ltz=translate, lsx=0.5)
            
            else:   
                cmds.polyExtrudeFacet('{}.f[{}]'.format(object, x), ltz=translate, lsx=0.9)
                cmds.polyExtrudeFacet('{}.f[{}]'.format(object, x), ltz=translate, lsx=0.5)
                
    cmds.select(object)
    
    

def attrCreation(attrName, attrNumber, gear, attrType, *args):
    '''
    This function creates attributes for the gear.
    '''
    if attrType=='float':
        cmds.addAttr(ln='{}'.format(attrName), at='float', min=attrNumber,dv=attrNumber)
        
    elif attrType=='string':
        cmds.addAttr(ln='{}'.format(attrName), dt='string')
        cmds.setAttr('{0}.{1}'.format(gear, attrName), attrNumber, type='string')
        
    elif attrType=='bool':
        cmds.addAttr(ln='{}'.format(attrName), at='bool')
        cmds.setAttr('{0}.{1}'.format(gear, attrName), attrNumber)
        
    cmds.setAttr('{0}.{1}'.format(gear, attrName), lock=True)



def gearReady(radiusGear, externalTeeth, numberTeeth, internalRadius, internalRadiusGear, internalTeeth, 
internalNumberTeeth, heightGear, lengthTeeth, internalLengthTeeth, nameGear, *args):
    '''
    This function takes the attributes values from the UI.
    '''
    radiusExt = cmds.intSliderGrp(radiusGear, q=1, value=1)
    teethExt = cmds.intSliderGrp(numberTeeth, q=1, value=1)
    radiusInt = cmds.intSliderGrp(internalRadiusGear, q=1, value=1)
    teethInt = cmds.intSliderGrp(internalNumberTeeth, q=1, value=1)
    teethExtCheck = cmds.checkBoxGrp(externalTeeth, q=1, v1=1)
    teethIntCheck = cmds.checkBoxGrp(internalTeeth, q=1, v1=1)
    radiusIntCheck = cmds.checkBoxGrp(internalRadius, q=1, v1=1)
    heightGear = cmds.intSliderGrp(heightGear, q=1, value=1)
    lengthExtTeeth = cmds.floatSliderGrp(lengthTeeth, q=1, value=1)
    lengthIntTeeth = cmds.floatSliderGrp(internalLengthTeeth, q=1, value=1)
    nameGear = cmds.textFieldGrp(nameGear, q=1, tx=1)
    
    gearCreation(radiusExt, teethExtCheck, teethExt, radiusIntCheck, radiusInt, teethIntCheck, teethInt, heightGear,
    lengthExtTeeth, lengthIntTeeth, nameGear, 0)



def gearCreation(radiusExt, teethExtCheck, teethExt, radiusIntCheck, radiusInt, teethIntCheck, 
teethInt, heightGear, lengthExtTeeth, lengthIntTeeth, nameGear, rotation, *args):
    '''
    This function create the gear, only the geometry.
    '''
    # If the name is not written, another name will be assigned
    if nameGear=='':
        actualName='huGear'
        actualBoolName='huGear'
        
    else:
        actualName=nameGear
        actualBoolName=nameGear
        
    for x in range(100):
        if actualName in cmds.ls():
            actualName='huGear{}'.format(str(x+1))
            actualBoolName='huGear{}'.format(str(x+1))
            
        else:
            break
    
    # If the gear has internal radius another name will be assigned, because the real name will be assigned to the boolean
    if radiusIntCheck==True:
        actualName='huGear'
    
    # The cylinder that will be the gear is created    
    gearCreation, gearCreationSH = cmds.polyCylinder(n=actualName, sc=1, h=heightGear, r=radiusExt)
    cmds.select(gearCreation)
    # Cylinder is rotated if necessary to fit with annother
    cmds.setAttr('{}.ry'.format(gearCreation), rotation)
    cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)
    # If there must be external teeth, those teeth are created
    if teethExtCheck==True:
        extrudeSides(teethExt, gearCreationSH, gearCreation, lengthExtTeeth, 'Ext')
        
    # If there must be internal radius, annother cylinder is created according to the attributes of the internal radius
    if radiusIntCheck==True:
        if radiusInt<radiusExt and (radiusExt-radiusInt)>(lengthIntTeeth+((radiusExt-radiusInt)/5)):
            gearIntCreation, gearIntCreationSH = cmds.polyCylinder(sc=1, h=heightGear, r=radiusInt)
            
            if teethIntCheck==True:
                extrudeSides(teethInt, gearIntCreationSH, gearIntCreation, lengthIntTeeth, 'Int')
            # A boolean of the two cylinders is done to create the gear
            gearCreation, gearCreationSH = cmds.polyBoolOp(gearCreation, gearIntCreation, op=2, n=actualBoolName)
            
        elif radiusInt>radiusExt or radiusInt==radiusExt:
            cmds.delete(gearCreation)
            cmds.error('internal radius must be lower than external radius')
            
        elif (radiusExt-radiusInt)<(lengthIntTeeth+((radiusExt-radiusInt)/5)) or (radiusExt-radiusInt)==(lengthIntTeeth+((radiusExt-radiusInt)/5)):
            cmds.delete(gearCreation)
            cmds.error('length of internal teeth must be lower than the weitght of the gear')
            
    cmds.select(gearCreation)
    cmds.deleteHistoryAheadOfGeomCache(gearCreation)
    cmds.select(gearCreation)
    
    # The attributes with the information of the gear are created
    if teethExt%2==0:
        teethType='up'
        
    else:
        teethType='dawn'
    
    attrCreation(attrName="teethType", attrNumber=teethType, gear=gearCreation, attrType='string')
    attrCreation(attrName="rotationTeeth", attrNumber=False, gear=gearCreation, attrType='bool')
    attrCreation(attrName="internalRadiusCheck", attrNumber=radiusIntCheck, gear=gearCreation, attrType='bool')
    attrCreation(attrName="internalRadius", attrNumber=radiusInt, gear=gearCreation, attrType='float')
    attrCreation(attrName="internalTeethCheck", attrNumber=teethIntCheck, gear=gearCreation, attrType='bool')
    attrCreation(attrName="internalTeeth", attrNumber=teethInt, gear=gearCreation, attrType='float')
    attrCreation(attrName="internalTeethLength", attrNumber=lengthIntTeeth, gear=gearCreation, attrType='float')
    attrCreation(attrName="externalTeethCheck", attrNumber=teethExtCheck, gear=gearCreation, attrType='bool')
    attrCreation(attrName="externalTeeth", attrNumber=teethExt, gear=gearCreation, attrType='float')
    attrCreation(attrName="externalTeethLength", attrNumber=lengthExtTeeth, gear=gearCreation, attrType='float')
    attrCreation(attrName="externalRadius", attrNumber=radiusExt, gear=gearCreation, attrType='float')
    attrCreation(attrName="heightGear", attrNumber=heightGear, gear=gearCreation, attrType='float')
    if radiusIntCheck==True:
        attrCreation(attrName="name", attrNumber=actualBoolName, gear=gearCreation, attrType='string')
    else:
        attrCreation(attrName="name", attrNumber=actualName, gear=gearCreation, attrType='string')
    attrCreation(attrName="order", attrNumber=1, gear=gearCreation, attrType='float')
    attrCreation(attrName="connectedBy", attrNumber='None', gear=gearCreation, attrType='string')
    attrCreation(attrName="lastRotationCtrl", attrNumber='None', gear=gearCreation, attrType='string')
    attrCreation(attrName="lastRotationValue", attrNumber='None', gear=gearCreation, attrType='string')
    attrCreation(attrName="lastGear", attrNumber='None', gear=gearCreation, attrType='string')
    
    return gearCreation






#            ##########      The following functions are responsible for create the     ##########
#            ##########         gear specified by the UI and fit it with the one        ##########
#            ##########         selected, they are used on the UI's second TabLayout       ##########




def rigConnectionsReady(radiusSecondGear, internalSecondRadiusCheck, internalSecondRadiusGear, 
internalSecondTeethCheck, internalSecondNumberTeeth, optionTeeth, heightSecondGear, lengthSecondInternalTeeth, 
lengthSecondExternalTeeth, nameSecondGear, *args):
    '''
    This function takes the attributes values from the UI.
    '''
    numberSecondRadius = cmds.intSliderGrp(radiusSecondGear, q=1, value=1)
    internalSecondRadiusCheck=cmds.checkBoxGrp(internalSecondRadiusCheck, q=1, v1=1)
    numberSecondInternalRadius = cmds.intSliderGrp(internalSecondRadiusGear, q=1, value=1)
    internalSecondTeethCheck=cmds.checkBoxGrp(internalSecondTeethCheck, q=1, v1=1)
    numberSecondInternalTeeth = cmds.intSliderGrp(internalSecondNumberTeeth, q=1, value=1)
    optionMenuIntExt = cmds.optionMenu(optionTeeth, q=1, v=1)
    numberSecondHeight = cmds.intSliderGrp(heightSecondGear, q=1, value=1)
    lengthSecondInternalTeeth = cmds.floatSliderGrp(lengthSecondInternalTeeth, q=1, value=1)
    lengthSecondExternalTeeth = cmds.floatSliderGrp(lengthSecondExternalTeeth, q=1, value=1)
    nameSecondGear = cmds.textFieldGrp(nameSecondGear, q=1, tx=1)
    
    rigConnections(numberSecondRadius, internalSecondRadiusCheck, numberSecondInternalRadius, internalSecondTeethCheck, 
    numberSecondInternalTeeth, optionMenuIntExt, numberSecondHeight, lengthSecondInternalTeeth, lengthSecondExternalTeeth, 
    nameSecondGear)
        
        

def rigConnections(externalSecondNumberRadius, internalSecondRadiusCheck, internalSecondNumberRadius, 
internalSecondTeethCheck, internalSecondNumberTeeth, optionTeeth, numberSecondHeight, lengthSecondInternalTeeth, 
lengthSecondExternalTeeth, nameSecondGear, *args):
    '''
    This function connect a gear with annother and create its rig system.
    '''
    sel = cmds.ls(sl=True)
    if len(sel)==0:
        cmds.error('Nothing selected')
        
    elif len(sel)>1:
        cmds.error('Please select only one gear')
        
    elif len(sel)==1:
        def CreateRigConnections(numberSecondRadius, radiusAttr, teethAttr, lenghtAttr, sign, ExtInt, *args):
            if cmds.objExists('{0}.{1}'.format(sel[0], radiusAttr)) and cmds.objExists('{0}.{1}'.format(sel[0], teethAttr)):
                numberFatherRadius = cmds.getAttr('{0}.{1}'.format(sel[0], radiusAttr))
                numberFatherTeeth = cmds.getAttr('{0}.{1}'.format(sel[0], teethAttr))
                numberFatherTeethLenght = cmds.getAttr('{0}.{1}'.format(sel[0], lenghtAttr))
                numberFatherHeight = cmds.getAttr('{}.heightGear'.format(sel[0]))
                teethSecond = int(numberSecondRadius*(float(numberFatherTeeth)/float(numberFatherRadius)))
                
                if ExtInt=='Int' and numberFatherRadius<externalSecondNumberRadius:
                    cmds.error('the radius of the new gear must be lower than the internal radius of the selection')
                    
                else:
                    # second gear is created
                    secondGearCreation = gearCreation(radiusExt=numberSecondRadius, teethExtCheck=True,
                    teethExt=teethSecond, radiusIntCheck=internalSecondRadiusCheck, radiusInt=internalSecondNumberRadius,
                    teethIntCheck=internalSecondTeethCheck, teethInt=internalSecondNumberTeeth,
                    heightGear=numberSecondHeight, lengthExtTeeth=lengthSecondExternalTeeth,
                    lengthIntTeeth=lengthSecondInternalTeeth, nameGear=nameSecondGear, rotation=0)    
                    
                    # the gear is recreated but well rotated
                    firstTeethRotation = cmds.getAttr('{}.rotationTeeth'.format(sel[0]))
                    secondTeethType = cmds.getAttr('{}.teethType'.format(secondGearCreation))
                    secondExternalTeeth = cmds.getAttr('{}.externalTeeth'.format(secondGearCreation))
                    if ExtInt=='Ext':
                        rotationAngle = 360/(secondExternalTeeth*2)
                        
                        if firstTeethRotation==False and secondTeethType=='dawn' or firstTeethRotation==True and secondTeethType=='up':
                            cmds.delete(secondGearCreation)
                            secondGearCreation = gearCreation(radiusExt=numberSecondRadius, teethExtCheck=True,
                            teethExt=teethSecond, radiusIntCheck=internalSecondRadiusCheck,
                            radiusInt=internalSecondNumberRadius, teethIntCheck=internalSecondTeethCheck,
                            teethInt=internalSecondNumberTeeth, heightGear=numberSecondHeight,
                            lengthExtTeeth=lengthSecondExternalTeeth, lengthIntTeeth=lengthSecondInternalTeeth,
                            nameGear=nameSecondGear, rotation=rotationAngle)
                            cmds.setAttr('{0}.rotationTeeth'.format(secondGearCreation), lock=False)
                            cmds.setAttr('{}.rotationTeeth'.format(secondGearCreation), True)
                            cmds.setAttr('{0}.rotationTeeth'.format(secondGearCreation), lock=True)
                    
                    # the position of the selected gear is taken
                    firstShape = cmds.listRelatives(sel[0], shapes=True)
                    SkinClusterNode = 0
                    for sh in firstShape:
                        rels = cmds.listHistory(sh)
                        
                        for input in rels:
                            if cmds.nodeType(input)=='skinCluster':
                                SkinClusterNode = input
                    
                    if SkinClusterNode==0:
                        positionFirstX = cmds.getAttr('{}.tx'.format(sel[0]))
                        positionFirstY = cmds.getAttr('{}.ty'.format(sel[0]))
                        positionFirstZ = cmds.getAttr('{}.tz'.format(sel[0]))
                        
                    else:
                        firstGearJointPlug = cmds.connectionInfo('{}.matrix[0]'.format(SkinClusterNode), sfd=1)
                        firstGearJointNode = firstGearJointPlug.split('.')
                        firstGearJoint = firstGearJointNode[0]
                        firstGearJointPOS = cmds.listRelatives(firstGearJoint, p=1)
                        firstGearHierarchyJoint = cmds.listRelatives(firstGearJointPOS, p=1)
                        positionFirst = cmds.xform(firstGearHierarchyJoint, q=1, ws=1, t=1)
                        positionFirstX = positionFirst[0]
                        positionFirstY = positionFirst[1]
                        positionFirstZ = positionFirst[2]
                    
                    # the separation of the gears is taken
                    if ExtInt=='Int':
                        if (numberFatherTeethLenght-lengthSecondExternalTeeth)<0:
                            teethDistance = numberFatherTeethLenght-lengthSecondExternalTeeth
                            
                        else:
                            teethDistance = 0
                            
                    if ExtInt=='Ext':
                        if numberFatherTeethLenght>lengthSecondExternalTeeth:
                            teethDistance = numberFatherTeethLenght
                            
                        else:
                            teethDistance = lengthSecondExternalTeeth
                    
                    # the position of the second gear is set
                    positionSecond = numberFatherRadius+(sign*numberSecondRadius)+teethDistance
                    cmds.setAttr('{}.tx'.format(secondGearCreation), positionFirstX+positionSecond)
                    cmds.setAttr('{}.ty'.format(secondGearCreation), positionFirstY)
                    cmds.setAttr('{}.tz'.format(secondGearCreation), positionFirstZ)
                    
                    # the rig system is created if necessary
                    # Naming variables
                    ctrl = '_CTRL'
                    grp = '_GRP'
                    pos = '_POS'
                    jnt = '_JNT'
                    if cmds.connectionInfo('{}.inMesh'.format(firstShape[0]), sfd=1)=='':
                        # principal groups are created
                        geometryGroup = cmds.group(n='geometry_{0}{1}'.format(sel[0], grp))
                        rigGroup = cmds.group(n='GearSystem_{0}_Rig{1}'.format(sel[0], grp))
                        cmds.parent(sel[0], geometryGroup)
                        
                        # general controller of the system is created
                        generalController, generalControllerSH = cmds.circle(n='GearSystem_{0}{1}'.format(sel[0], ctrl))
                        cmds.select('{}.cv[0:7]'.format(generalController))
                        cmds.rotate('90deg', 0, 0, r=True)
                        cmds.scale(numberFatherRadius, 1, numberFatherRadius)
                        cmds.move(0, numberFatherHeight/2+3, 0, r=1, os=1, wd=1)
                        cmds.select('{}.cv[1]'.format(generalController), '{}.cv[3]'.format(generalController), 
                        '{}.cv[5]'.format(generalController), '{}.cv[7]'.format(generalController))
                        cmds.scale(2, 1, 2)
                        cmds.setAttr('{}.tx'.format(generalController), positionFirstX)
                        cmds.setAttr('{}.ty'.format(generalController), positionFirstY)
                        cmds.setAttr('{}.tz'.format(generalController), positionFirstZ)
                        cmds.select(generalController)
                        cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)
                        generalControllerOffset = cmds.group(n='{0}{1}'.format(generalController, pos))
                        controllersGroup = cmds.group(n='controllers_{0}{1}'.format(sel[0], grp))
                        cmds.select(d=True)
                        
                        # the rotation controller is created
                        rotationController, rotationControllerSH = cmds.circle(n='rotation_{0}{1}'.format(sel[0], ctrl))
                        cmds.select('{}.cv[0:7]'.format(rotationController))
                        cmds.rotate('90deg', 0, 0, r=True)
                        cmds.scale(numberFatherRadius, 1, numberFatherRadius)
                        cmds.move(0, numberFatherHeight/2+2, 0, r=1, os=1, wd=1)
                        cmds.setAttr('{}.tx'.format(rotationController), positionFirstX)
                        cmds.setAttr('{}.ty'.format(rotationController), positionFirstY)
                        cmds.setAttr('{}.tz'.format(rotationController), positionFirstZ)
                        cmds.select(rotationController)
                        cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)
                        rotationControllerOffset = cmds.group(n='{0}{1}'.format(rotationController, pos))
                        cmds.parent(rotationControllerOffset, generalController)
                        cmds.parent(controllersGroup, rigGroup)
                        rotationAttrs=['tx', 'ty', 'tz', 'rx', 'rz', 'sx', 'sy', 'sz', 'visibility']
                        for attrs in rotationAttrs:
                            cmds.setAttr('{0}.{1}'.format(rotationController, attrs), lock=True, k=False)
                            
                        # the joint that will be skinned with the first gear is created
                        firstGearPosition = cmds.getAttr('{}.t'.format(sel[0]))
                        firstGearJoint = cmds.joint(n='{0}Rotate{1}'.format(sel[0], jnt), p=firstGearPosition[0])
                        cmds.parent(w=True)
                        firstGearJointOffset = cmds.group(n='{0}Rotate{1}'.format(sel[0], pos))
                        cmds.select(firstGearJoint)
                        cmds.skinCluster( firstGearJoint, sel[0], tsb=True)
                        cmds.connectAttr('{}.ry'.format(rotationController), '{}.ry'.format(firstGearJoint))
                        
                        # the joint father of the hierarchy is created
                        firstGearFatherHierarchyJoint = cmds.joint(n='gearSystem_{0}{1}'.format(sel[0], pos), p=firstGearPosition[0])
                        cmds.parent(w=True)
                        jointsGroup = cmds.group(n='joints_{0}{1}'.format(sel[0], grp))
                        
                        # the joint father of the first gear is created
                        firstGearHierarchyJoint = cmds.joint(n='{0}{1}'.format(sel[0], jnt), p=firstGearPosition[0])
                        cmds.parent(w=True)
                        cmds.parent(firstGearHierarchyJoint, firstGearFatherHierarchyJoint)
                        cmds.parent(firstGearJointOffset, firstGearHierarchyJoint)
                        cmds.parent(jointsGroup, rigGroup)
                        cmds.parentConstraint(generalController, firstGearFatherHierarchyJoint, mo=1)
                        cmds.scaleConstraint(generalController, jointsGroup, mo=1)
                        cmds.setAttr('{}.visibility'.format(jointsGroup), 0)
                    
                    # If there are a system already created, the variables that we need as the controller of the selected gear are searched
                    else:
                        firstParentConstrain = cmds.connectionInfo('{}.translate.translateX'.format(firstGearHierarchyJoint[0]), sfd=1)
                        if firstParentConstrain == '':
                            firstJointPlug = cmds.connectionInfo('{}.inverseScale'.format(firstGearHierarchyJoint[0]), sfd=1)
                            firstGearHierarchyJoint = firstJointPlug.split('.')
                            firstGearHierarchyJoint = firstGearHierarchyJoint[0]
                            firstParentConstrain = cmds.connectionInfo('{}.translate.translateX'.format(firstGearHierarchyJoint), sfd=1)
                        firstParentConstrainNode = firstParentConstrain.split('.')
                        generalControllerPlug = cmds.connectionInfo('{}.target[0].targetParentMatrix'.format(firstParentConstrainNode[0]), sfd=1)
                        generalControllerNode = generalControllerPlug.split('.')
                        
                        generalController = generalControllerNode[0]
                        geometryGroup = cmds.listRelatives(sel[0], p=1)
                        cmds.parent(secondGearCreation, geometryGroup)

                    # joints of the second gear are created
                    SecondGearPosition = cmds.getAttr('{}.t'.format(secondGearCreation))
                    SecondGearJoint = cmds.joint(n='{0}Rotate{1}'.format(secondGearCreation, jnt), p=SecondGearPosition[0])
                    cmds.parent(w=True)
                    secondGearJointOffset = cmds.group(n='{0}Rotate{1}'.format(secondGearCreation, pos))
                    SecondGearHierarchyJoint = cmds.joint(n='{0}{1}'.format(secondGearCreation, jnt), p=SecondGearPosition[0])
                    cmds.parent(w=True)
                    cmds.parent(secondGearJointOffset, SecondGearHierarchyJoint)
                    cmds.select(SecondGearJoint)
                    cmds.skinCluster(SecondGearJoint, secondGearCreation, tsb=True)
                    cmds.parent(SecondGearHierarchyJoint, firstGearHierarchyJoint)
                    
                    # second gear controller is created
                    SecondGearHeight = cmds.getAttr('{}.heightGear'.format(secondGearCreation))
                    secondGearController, secondGearControllerSH = cmds.circle(n='{0}{1}'.format(secondGearCreation, ctrl),
                    s=secondExternalTeeth*2)
                    cmds.select('{0}.cv[0:{1}]'.format(secondGearController, secondExternalTeeth*2-1))
                    cmds.rotate('90deg', 0, 0, r=True)
                    cmds.scale(numberSecondRadius, 1, numberSecondRadius)
                    cmds.move(0, SecondGearHeight/2+3, 0, r=1, os=1, wd=1)
                    vertexList=[]
                    for vertex in range(int(secondExternalTeeth*2)):
                        if vertex%2==0:
                            selectedVtx='{0}.cv[{1}]'.format(secondGearController, vertex)
                            vertexList.append(selectedVtx)
                    cmds.select(vertexList)
                    cmds.scale(0.5, 1, 0.5)
                    cmds.setAttr('{}.tx'.format(secondGearController), positionFirstX+positionSecond)
                    cmds.setAttr('{}.ty'.format(secondGearController), positionFirstY)
                    cmds.setAttr('{}.tz'.format(secondGearController), positionFirstZ)
                    cmds.select(secondGearController)
                    cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)
                    secondGearControllerOffset = cmds.group(n='{0}{1}'.format(secondGearCreation, pos))
                    cmds.parent(secondGearControllerOffset, generalController)
                    cmds.select(d=True)
                    secondCtrlAttrs=['rx', 'sx', 'sy', 'sz', 'visibility']
                    for attrs in secondCtrlAttrs:
                        cmds.setAttr('{0}.{1}'.format(secondGearController, attrs), lock=True, k=False)
                    # rotation Y from gears is connected following the power transmission
                    multiplyDivideNode = cmds.shadingNode('multiplyDivide', au=True)
                    multiplyRelation = sign*-(float(numberFatherTeeth)/float(teethSecond))
                    cmds.setAttr("{}.input2X".format(multiplyDivideNode), multiplyRelation)
                    cmds.connectAttr('{}.ry'.format(firstGearJoint), '{}.input1X'.format(multiplyDivideNode))
                    cmds.connectAttr('{}.outputX'.format(multiplyDivideNode), '{}.ry'.format(SecondGearJoint))
                    
                    cmds.parentConstraint(secondGearController, SecondGearHierarchyJoint, mo=1, skipRotate=('y', 'x'))
                    cmds.select(secondGearCreation)
                    
                    # attributes of the second gear are edited
                    father = cmds.listRelatives(sel[0], p=1)
                    childrens = cmds.listRelatives(father, c=1)
                    numberOfGears = len(childrens)
                    positionController = cmds.getAttr('{}.ry'.format(generalController))
                    
                    def changeAttrs(attr, value, *args):
                        cmds.setAttr('{0}.{1}'.format(secondGearCreation, attr), lock=False)
                        cmds.setAttr('{0}.{1}'.format(secondGearCreation, attr), value, type='string')
                        cmds.setAttr('{0}.{1}'.format(secondGearCreation, attr), lock=True)
                        
                    changeAttrs('connectedBy', teethAttr, *args)
                    changeAttrs('lastRotationCtrl', generalController, *args)
                    changeAttrs('lastRotationValue', positionController, *args)
                    changeAttrs('lastGear', sel[0], *args)
                    cmds.setAttr('{0}.order'.format(secondGearCreation), lock=False)
                    cmds.setAttr('{0}.order'.format(secondGearCreation), numberOfGears)
                    cmds.setAttr('{0}.order'.format(secondGearCreation), lock=True)
                    
            else:
                cmds.error('Selected object is not suitable for your attributes')
                
            return(secondGearCreation)
            
            
        # we execute the function 'CreateRigConnections' with different arguments depending on whether the gear will 
        # be connected by internal or external teeth
        numberFatherExtTeethCheck = cmds.getAttr('{}.externalTeethCheck'.format(sel[0]))
        numberFatherIntTeethCheck = cmds.getAttr('{}.internalTeethCheck'.format(sel[0]))
        if optionTeeth == 'externalTeeth' and numberFatherExtTeethCheck==True:
            secondGear = CreateRigConnections(externalSecondNumberRadius, 'externalRadius', 'externalTeeth',
            'externalTeethLength', +1, 'Ext')
            
        elif optionTeeth == 'internalTeeth' and numberFatherIntTeethCheck==True:
            secondGear = CreateRigConnections(externalSecondNumberRadius, 'internalRadius', 'internalTeeth',
            'internalTeethLength', -1, 'Int')
            
        else:
            cmds.error('Selected object is not suitable for your attributes')
        
        cmds.select(secondGear)
        return(secondGear)



def deleteFunction(*args):
    '''
    This function delete a gear and its joints and controller
    '''
    sel = cmds.ls(sl=True)
    if len(sel)==0:
        cmds.error('Nothing selected')
        
    elif len(sel)>1:
        cmds.error('Please select only one gear')
        
    elif len(sel)==1 and cmds.objExists('{}.externalRadius'.format(sel[0])):
        firstShape = cmds.listRelatives(sel[0], shapes=True)
        
        SkinClusterNode = 0
        
        for sh in firstShape:
            rels = cmds.listHistory(sh)
            
            for input in rels:
                if cmds.nodeType(input)=='skinCluster':
                    SkinClusterNode = input
        
        # gear joints and controller are searched
        if SkinClusterNode!=0:
            firstGearJointPlug = cmds.connectionInfo('{}.matrix[0]'.format(SkinClusterNode), sfd=1)
            firstGearJointNode = firstGearJointPlug.split('.')
            firstGearJoint = firstGearJointNode[0]
            firstGearJointPOS = cmds.listRelatives(firstGearJoint, p=1)
            firstGearHierarchyJoint = cmds.listRelatives(firstGearJointPOS, p=1)
            parentConstraintQuery = cmds.connectionInfo('{}.translate.translateX'.format(firstGearHierarchyJoint[0]),
            id=1)
            
            if parentConstraintQuery==True:
                parentConstraintPlug = cmds.connectionInfo('{}.translate.translateX'.format(firstGearHierarchyJoint[0]),
                sfd=1)
                parentConstraintNode = parentConstraintPlug.split('.')
                controllerPlug = cmds.connectionInfo('{}.target[0].targetParentMatrix'.format(parentConstraintNode[0]),
                sfd=1)
                controllerNode = controllerPlug.split('.')
                controllerPos = cmds.listRelatives(controllerNode[0], p=1)
                child = cmds.listRelatives(controllerNode[0], c=1)
                
                # gear joints and controller are deleted
                if len(child)!=2:
                    cmds.delete(controllerPos[0])
                    cmds.delete(sel[0])
                    cmds.delete(firstGearHierarchyJoint[0])
                    
                else:
                    cmds.error('This is not the last gear')
                    
            else:
                cmds.error('This is not the last gear')
                
        else:
            cmds.error('This is not the last gear')
        
    else:
        cmds.error('Selected object is not suitable')
    
        
        
def copyGearAttrs(radius, lengthExternalTeeth, internalRadiusCheck, internalRadius, 
internalTeethCheck, internalNumberTeeth, lengthInternalTeeth, height, create, externalTeethCheck, externalNumberTeeth, *attrs):
    '''
    This function copy attributes from selected gear and apply them to the sliders on the UI to create an equal gear easier
    '''
    sel = cmds.ls(sl=True)
    if len(sel)==0:
        cmds.error('Nothing selected')
        
    elif len(sel)>1:
        cmds.error('Please select only one gear')
        
    elif len(sel)==1 and cmds.objExists('{}.externalRadius'.format(sel[0])):
        # attributes are taken
        internalRadiusCheckAttr = cmds.getAttr('{}.internalRadiusCheck'.format(sel[0]))
        internalRadiusAttr = cmds.getAttr('{}.internalRadius'.format(sel[0]))
        internalTeethCheckAttr = cmds.getAttr('{}.internalTeethCheck'.format(sel[0]))
        internalTeethAttr = cmds.getAttr('{}.internalTeeth'.format(sel[0]))
        internalTeethLengthAttr = cmds.getAttr('{}.internalTeethLength'.format(sel[0]))
        externalTeethLengthAttr = cmds.getAttr('{}.externalTeethLength'.format(sel[0]))
        externalRadiusAttr = cmds.getAttr('{}.externalRadius'.format(sel[0]))
        heightGearAttr = cmds.getAttr('{}.heightGear'.format(sel[0]))
        
        # sliders are edited with the new parameters
        cmds.intSliderGrp(radius, e=1, v=externalRadiusAttr)
        cmds.floatSliderGrp(lengthExternalTeeth, e=1, v=externalTeethLengthAttr)
        cmds.checkBoxGrp(internalRadiusCheck, e=1, v1=internalRadiusCheckAttr)
        cmds.intSliderGrp(internalRadius, e=1, v=internalRadiusAttr)
        cmds.checkBoxGrp(internalTeethCheck, e=1, v1=internalTeethCheckAttr)
        cmds.intSliderGrp(internalNumberTeeth, e=1, v=internalTeethAttr)
        cmds.floatSliderGrp(lengthInternalTeeth, e=1, v=internalTeethLengthAttr)
        cmds.intSliderGrp(height, e=1, v=heightGearAttr)
        
        # copying a gear in the first layout we copy two extra attributes
        if create==True:
            externalTeethCheckAttr = cmds.getAttr('{}.externalTeethCheck'.format(sel[0]))
            externalNumberTeethAttr = cmds.getAttr('{}.externalTeeth'.format(sel[0]))
            cmds.checkBoxGrp(externalTeethCheck, e=1, v1=externalTeethCheckAttr)
            cmds.intSliderGrp(externalNumberTeeth, e=1, v=externalNumberTeethAttr)
    
    else:
        cmds.error('Selected object is not suitable')






#            ##########      The following functions are responsible for changing the     ##########
#            ##########          sliders and checkBoxes as appropriate in the UI         ##########




def checkTeeth(teeth, teethNumber, lengthTeeth, *args):
    '''
    This function blocks some sliders according to the state of the checker box
    '''
    resultTeeth = cmds.checkBoxGrp(teeth, q=1, v1=1)
    cmds.intSliderGrp(teethNumber, e=1, en=resultTeeth)
    cmds.floatSliderGrp(lengthTeeth, e=1, en=resultTeeth)



def checkIntR(internalRadius, internalRadiusGear, internalTeeth, internalNumberTeeth, internalLengthTeeth, *args):
    '''
    This function blocks annother sliders according to the state of the checker box
    '''
    resultIntR = cmds.checkBoxGrp(internalRadius, q=1, v1=1)
    if resultIntR==False:
        cmds.intSliderGrp(internalRadiusGear, e=1, en=0)
        cmds.checkBoxGrp(internalTeeth, e=1, en=0, v1=0)
        cmds.intSliderGrp(internalNumberTeeth, e=1, en=0)
        cmds.floatSliderGrp(internalLengthTeeth, e=1, en=0)
        
    else:
        cmds.intSliderGrp(internalRadiusGear, e=1, en=1)
        cmds.checkBoxGrp(internalTeeth, e=1, en=1, v1=0)






#            ##########      The following function is responsible for creating the UI       ##########




def windowGearsFunction(libraryButtons=[], libraryPath=''):
    '''
    This function creates the UI
    
    In the layout 'Create Gears' you can create gears.
    Select the parameters of the gear you like to create.
    When you have your parameters click on the button 'Create gear'.
    You can also copy the parameters of an already created gear selecting that gear and clicking on the 
    button 'copy attributes from selected gear'.
    It is advisable to write a specific name for your gear, but if you dont write anything, the name 'huGear' will be set
    
    
    In the layout 'Rig Gears' you can create a gear connected to the selected gear.
    Select if your new gear will be connected by the external or internal teeth from your selected gear.
    Select the parameters of the gear you like to create.
    When you have your parameters check that you have a gear selected and click on the button 'Create gear Chain'.
    You can also copy the parameters of an already created gear selecting that gear and clicking on the 
    button 'copy attributes from selected gear'.
    If you do not like your new gear you can click on the button 'Delete your last gear from chain' to delete that gear and 
    try different parameters.
    It is advisable to write a specific name for your new gear, but if you dont write anything, the name 'huGear' will be set
    
    
    In the layout 'Gallery' you can export systems of gears created by you and import another systems, you can also load a library of systems.
    To export systems, select the geometry of a gear in the system you like to export and write a name for the file, then click on the button
    'Export System', a json file with the information of your system and an image of the system will be saved. The image will be a playblast from 
    your viewer so check the angle of the camera before click the export button to have a better image.
    To import systems, write the name of the file and click 'Import System', be careful and check that there are no gears in the scene with the 
    same name as in the system you like to load.
    The path where the files will be saved and opened is the path where this script is saved, in the folder 'systemsFolder'
    When the UI is created all the systems in the folder 'systemsFolder' will be shown, but if you export more systems you can click on the button 
    'load gear library in path' to reload the UI with the new systems.
    
    '''
    winId = 'CreateGears'
    
    if cmds.window(winId, exists=True):
        cmds.deleteUI(winId)
        
    cmds.window(winId, title='Create Gears')
    
    
    ##  Creation layout
    windowsLayout = cmds.tabLayout()
    createMainLayout = cmds.columnLayout(adj=True)
    cmds.text('\n select attributes for your gear \n')
    copyGearAttrsButton = cmds.button(l='copy attributes from selected gear')
    cmds.text('\n')
    radiusGear = cmds.intSliderGrp(field=True, label='Radius', minValue=1, maxValue=20, fmn=1, fmx=100, v=4)
    ## firstCheck
    externalTeeth = cmds.checkBoxGrp(numberOfCheckBoxes=1, label='External Teeth', v1=True)
    numberTeeth = cmds.intSliderGrp(field=True, en=1, label='Number of teeth', minValue=3, maxValue=40, fmn=1, fmx=100,
    v=10)
    lengthTeeth = cmds.floatSliderGrp(field=True, en=1, label='Length of teeth', minValue=0, maxValue=2, fmn=0, fmx=10,
    v=1)
    cmds.checkBoxGrp(externalTeeth, e=1, cc=partial(checkTeeth, externalTeeth, numberTeeth, lengthTeeth))
    ##  Internal layout
    internalLayout = cmds.frameLayout(label='Internal teeth', cll=1, cl=0)
    ## secondCheck
    internalRadius = cmds.checkBoxGrp(numberOfCheckBoxes=1, label='Internal Radius', v1=False)
    internalRadiusGear = cmds.intSliderGrp(field=True, en=0, label='Internal Radius', minValue=1, maxValue=20, fmn=1, fmx=100,
    v=2)
    ## thirdCheck
    internalTeeth = cmds.checkBoxGrp(numberOfCheckBoxes=1, label='Internal Teeth', en=0, v1=False)
    internalNumberTeeth = cmds.intSliderGrp(field=True, en=0, label='Number of teeth', minValue=3, maxValue=60, fmn=1,
    fmx=100, v=10)
    internalLengthTeeth = cmds.floatSliderGrp(field=True, en=0, label='length of teeth', minValue=0, maxValue=2, fmn=0,
    fmx=10, v=1)
    cmds.text('\n')
    cmds.checkBoxGrp(internalTeeth, e=1, cc=partial(checkTeeth, internalTeeth, internalNumberTeeth, internalLengthTeeth))
    cmds.checkBoxGrp(internalRadius, e=1, cc=partial(checkIntR, internalRadius, internalRadiusGear, internalTeeth, 
    internalNumberTeeth, internalLengthTeeth))
    cmds.setParent('..')
    heightGear = cmds.intSliderGrp(field=True, en=1, label='Height', minValue=1, maxValue=20, fmn=1, fmx=100, v=1)
    nameGear = cmds.textFieldGrp(label='Gear Name')
    cmds.text('\n')
    ## execute
    cmds.button(copyGearAttrsButton, e=1, c=partial(copyGearAttrs, radiusGear, lengthTeeth, internalRadius, internalRadiusGear, 
    internalTeeth, internalNumberTeeth, internalLengthTeeth, heightGear, True, externalTeeth, numberTeeth))
    createGearButton = cmds.button(l='Create gear', c=partial(gearReady, radiusGear, externalTeeth, numberTeeth,
    internalRadius, internalRadiusGear, internalTeeth, internalNumberTeeth, heightGear, lengthTeeth, internalLengthTeeth,
    nameGear))
    cmds.setParent('..')
    
    
    ##  Rig Layout
    rigMainLayout = cmds.columnLayout(adj=True)
    cmds.text('\n select a gear with which to fit the next one \n')
    copyGearAttrsButton2 = cmds.button(l='copy attributes from selected gear')
    cmds.text('\n')
    optionTeeth = cmds.optionMenu( label='Connect by')
    cmds.menuItem( label='externalTeeth' )
    cmds.menuItem( label='internalTeeth' )
    radiusSecondGear = cmds.intSliderGrp(field=True, label='radius', minValue=1, maxValue=20, fmn=1, fmx=100, v=4)
    lengthSecondExternalTeeth = cmds.floatSliderGrp(field=True, en=1, label='Length of tooth', minValue=0, maxValue=2,
    fmn=0, fmx=10, v=1)
    internalSecondLayout = cmds.frameLayout(label='Internal teeth', cll=1, cl=0)
    internalSecondRadiusCheck = cmds.checkBoxGrp(numberOfCheckBoxes=1, label='Internal Radius', v1=False)
    internalSecondRadiusGear = cmds.intSliderGrp(field=True, en=0, label='Internal Radius', minValue=1, maxValue=20,
    fmn=1, fmx=100, v=2)
    internalSecondTeethCheck = cmds.checkBoxGrp(numberOfCheckBoxes=1, vis=1, label='Internal Teeth', en=0, v1=False)
    internalSecondNumberTeeth = cmds.intSliderGrp(field=True, en=0, vis=1, label='Number of teeth', minValue=3,
    maxValue=40, fmn=1, fmx=100, v=10)
    lengthSecondInternalTeeth = cmds.floatSliderGrp(field=True, en=0, label='Length of teeth', minValue=0, maxValue=2,
    fmn=0, fmx=10, v=1)
    cmds.text('\n')
    cmds.checkBoxGrp(internalSecondTeethCheck, e=1, cc=partial(checkTeeth, internalSecondTeethCheck,
    internalSecondNumberTeeth, lengthSecondInternalTeeth))
    cmds.checkBoxGrp(internalSecondRadiusCheck, e=1, cc=partial(checkIntR, internalSecondRadiusCheck,
    internalSecondRadiusGear, internalSecondTeethCheck, internalSecondNumberTeeth, lengthSecondInternalTeeth))
    cmds.setParent('..')
    heightSecondGear = cmds.intSliderGrp(field=True, en=1, label='Height', minValue=1, maxValue=20, fmn=1, fmx=100, v=1)
    nameSecondGear = cmds.textFieldGrp(label='Gear Name')
    cmds.text('\n')
    # execute
    rigGearButton = cmds.button(l='Create gear Chain', c=partial(rigConnectionsReady, radiusSecondGear,
    internalSecondRadiusCheck, internalSecondRadiusGear, internalSecondTeethCheck, internalSecondNumberTeeth, optionTeeth,
    heightSecondGear, lengthSecondInternalTeeth, lengthSecondExternalTeeth, nameSecondGear))
    cmds.text('\n')
    deleteGearButton = cmds.button(l='Delete your last gear from chain', c=partial(deleteFunction))
    cmds.button(copyGearAttrsButton2, e=1, c=partial(copyGearAttrs, radiusSecondGear, lengthSecondExternalTeeth, 
    internalSecondRadiusCheck, internalSecondRadiusGear, internalSecondTeethCheck, internalSecondNumberTeeth,
    lengthSecondInternalTeeth, heightSecondGear, False, None, None))
    cmds.setParent('..')
    
    
    ##  Gallery layout
    galleryMainLayout = cmds.columnLayout(adj=True)
    libraryLayout = cmds.rowColumnLayout(nc=8)
    for buttons in libraryButtons:
        systemFile=os.path.splitext(buttons)
        cmds.iconTextButton(style='iconAndTextVertical', l=systemFile[0], al='center',
        image=r'{0}\{1}.png'.format(libraryPath, systemFile[0]), c=partial(createSelectedSystem, libraryPath, systemFile[0]))
        cmds.separator(st='single')
    cmds.setParent('..')
    cmds.separator()
    cmds.text('\n \n')
    filePath = cmds.textFieldGrp(label='File Path', ed=0, tx=r'{}\systemsFolder'.format(actualPath))
    cmds.text('\n ')
    loadPath = cmds.button(l='load gear library in path', c=partial(setLibrary, filePath))
    cmds.text('\n Write the name of the file you want to save or open \n')
    fileName = cmds.textFieldGrp(label='File Name')
    cmds.text('\n Please select the geometry of a gear of your system to export that system \n')
    exportProperties = cmds.button(l='Export System', c=partial(exportValues, fileName, filePath))
    cmds.text('\n Please check that there are no gears in the scene with the same name as in the system you like to load \n')
    importProperties = cmds.button(l='Import System', c=partial(importValues, fileName, filePath))
    cmds.tabLayout(windowsLayout, edit=True, tabLabel=((createMainLayout, 'Create Gears'), (rigMainLayout, 'Rig Gears'),
    (galleryMainLayout, 'Gallery')))
    
    cmds.showWindow()
    


loadLibrary(r'{}\systemsFolder'.format(actualPath))