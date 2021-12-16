# Autor Harriet Landa Gil 2020

import maya.cmds as mc
import xgenm as xg
import maya.mel as mel
from functools import partial
import os
import xgenm as xg
import xgenm.xgGlobal as xgg
import pymel.util



### Some functions to convert the XGen guides to curves and to export them as abc ###
def curvtoguides(*args):
    '''
    Function to convert the guides to a curves at the same position
    '''
    countvertex = 10
    mc.select('xg*')
    numGuides = len(mc.ls(sl=True, tr=True, flatten=True))
    guides = mc.ls(sl=True, tr=True, flatten=True)
    mc.select(clear=True)
    vertexlist_names = []
    vertexlist_names[:] = []


    for each in guides:
        for i in range(countvertex):
            countV = '{}.vtx[{}]'.format(each, i)
            cvposi = mc.pointPosition(countV)
            vertexlist_names.append(cvposi)
            

    
    curves_list = []
    curves_list[:] = []

    for x in range(numGuides):
        curve = mc.curve(p=vertexlist_names[x*10:x+10+(x*9)], n='xguide{}'.format(guides[x]))
        curves_list.append(curve)


def exportCurvesAbc(*args):
    '''
    Function to export the guiedes converted guides to a path as ABC 
    '''
    projectpath = mc.workspace(q=True, act=True)
    path = mc.fileDialog2(okCaption='Export', fileMode=2, dir=projectpath)
    command = "-frameRange " + str(0) + " " + str(0) +" -uvWrite -worldSpace " + " -file " + '{}/xgen_curves.abc'.format(path[0])
    mc.AbcExport ( j = command )

### Some functions to export collections to a path  ###
def exportCollectiontopath(collectname, exportpath, *args):
    '''
    Function to export the selected collection to a path that the user selects
    '''
    xgenCollection = xgg.xgen.palettes()[0]
    path = mc.textFieldButtonGrp(exportpath, q=1, text=1)
    colname = mc.textFieldGrp(collectname, q=1, text=1)
    print('Exporting Collection to {}//{}.xgen'.format(path, colname))
    xgg.xgen.exportPalette(xgenCollection, '{}//{}.xgen'.format(path, colname))

def exportCollec(exportpath, collectname, *args):
    '''
    Function to get the path to export the XGen collection
    '''
    path = mc.fileDialog2(okCaption='Export', fileMode=2)
    mc.textFieldButtonGrp(exportpath, e=1, it=path[0])   

### Some functions to export description to a path  ###
def exportDesctopath(descname, exportDescpath, palcname, *args):
    '''
    Function to export the selected description to a path that the user selects
    '''
    xgenDescription = mc.optionMenu(descname, q=1, v=1)
    xgenPal = mc.optionMenu(palcname, q=1, v=1)
    path = mc.textFieldButtonGrp(exportDescpath, q=1, text=1)
    print('Exporting Description to {}//{}.xdsc'.format(path, xgenDescription))
    xgg.xgen.exportDescription(str(xgenPal), str(xgenDescription), '{}//{}.xdsc'.format(path, xgenDescription))

def exportDesc(exportDescpath, descname, *args):

    '''
    Function to get the path to export the XGen description
    '''
    path = mc.fileDialog2(okCaption='Export', fileMode=2)
    mc.textFieldButtonGrp(exportDescpath, e=1, it=path[0])   

 ### Some functions with the tools most used when working in Xgen, we execute a mel comand with the maya.mel.eval comand  ###   
def xToggleGuideDisplay(*args):
     mel.eval('python("xgen.toggleGuideDisplay(xgui.createDescriptionEditor(False).currentDescription())");')    

def xToggleGuideReference(*args):
     mel.eval('python("xgen.toggleGuideReference(xgui.createDescriptionEditor(False).currentDescription())");')    

def xgGuideTool(*args):
    mel.eval('XgGuideTool')

def xgMirrorTool(*args):
    mel.eval('xgmFlipGuides( python("xgui.createDescriptionEditor(False).currentDescription()") );')
    mc.delete('xgGroom')

def xgSculptTool(*args):
    mel.eval('python("xgui.createDescriptionEditor(False).guideSculptContext(False)");')

def rebuildGuides(*args):
    countV = 10
    mel.eval('xgmChangeCVCount({});'.format(countV))


def hotkeyimport(hotcket_text, *args):
    '''
    This function create a hotkey for the Create Guides tool in the maya hotkeys path
    '''
    hotkeyq = mc.textField(hotcket_text, q=1, text=1)
    username = os.environ['USERNAME']
    prefsDir = mc.internalVar(upd=True)
    outFile = r'{}hotkeys/Xgen.mhk'.format(prefsDir)
    hotkeyl = str(hotkeyq)
    if os.path.exists(outFile):
        pass
    else:
        with open(outFile, 'w') as file_out:
            file_out.write('//Maya Preference 2018 (Release 1) \n// \n// \n// \n// The runtime commands referenced by the hotkeys \n// \n// \n// The name commands referenced by the hotkeys \n// \nnameCommand \n    -annotation "XgGuideToolNameCommand" \n    -sourceType "mel" \n    -command ("XgGuideTool") \n    XgGuideToolNameCommand; \n// \n// The user hotkeys \n// \n// \n// The hotkey set \n// \nhotkeySet -source "Maya_Default" -current Xgen; \n// \n// The hotkey contexts and hotkeys \n// \nhotkey -keyShortcut "Space" -releaseName (""); \nhotkey -keyShortcut "Space" -name (""); \nhotkey -keyShortcut "{}" -releaseName (""); \nhotkey -keyShortcut "{}" -name ("XgGuideToolNameCommand"); \nhotkey -keyShortcut "{}" -sht -name (""); \nhotkeyCtx -type "Editor" -addClient "hyperShadePanel"; \nhotkeyCtx -type "Editor" -addClient "graphEditor"; \nhotkeyCtx -type "Editor" -addClient "posePanel"; \nhotkeyCtx -type "Editor" -addClient "nodeEditorPanel"; \nhotkeyCtx -type "Editor" -addClient "timeEditorPanel"; \nhotkeyCtx -type "Editor" -addClient "polyTexturePlacementPanel"; \nhotkeyCtx -type "Editor" -addClient "hyperGraphPanel"; \nhotkeyCtx -type "Editor" -addClient "profilerPanel"; \nhotkeyCtx -type "Editor" -addClient "shapePanel"; \nhotkeyCtx -type "Editor" -addClient "outlinerPanel"; \nhotkeyCtx -type "Tool" -addClient "xgmIGBrush"; \nhotkeyCtx -type "Tool" -addClient "texSculptCacheContext"; \nhotkeyCtx -type "Tool" -addClient "SymmetrizeUVBrush"; \nhotkeyCtx -type "Tool" -addClient "polyCutUV"; \nhotkeyCtx -type "Tool" -addClient "texCutContext"; \nhotkeyCtx -type "Tool" -addClient "Unfold3DBrush"; \nhotkeyCtx -type "Tool" -addClient "sculptMeshCache";'.format(hotkeyl, hotkeyl, hotkeyl))
        mc.hotkeySet(e=1, ip=outFile) 
    os.remove(outFile)


def selectallGuides(*args):
    mc.select('xg*')

def edithotk(hotcket_text, lockhot, *args):
    mc.textField(hotcket_text, e=1, editable=1)
    mc.checkBox(lockhot, e=1, v=0)

def lockhotk(hotcket_text, edithot, *args):
    mc.textField(hotcket_text, e=1, editable=0)
    mc.checkBox(edithot, e=1, v=0)

def createDescp(*args):
    mel.eval('XgCreateDescription()')


def xGenToolkitUI(*args):
    '''
    This is the main function that creates the UI
    '''
    if mc.window("xgen", exists=True, sizeable=True):
        mc.deleteUI("xgen")

    myWindow = mc.window("xgen", t="XGen Toolkit", w=300, h=300)
    mc.columnLayout(adj=True)
    mc.rowColumnLayout(nc=9)
    mc.separator(w=80, style='none')
    mc.button(l='Select All Guides', bgc=(.2,0,.4), c=partial(selectallGuides))
    mc.separator(w=80, style='none')
    mc.button(l='Create Description', bgc=(.2,.8,.4), c=partial(createDescp))
    mc.separator(w=80, style='none')
    mc.button(l='REFRESH', bgc=(.2,0,0), c=partial(xGenToolkitUI))
    
    mc.setParent('..')
    
    mc.separator(h=10, style='none')
    
    tabs = mc.tabLayout()
    child1 = mc.rowColumnLayout(nc=7)
    mc.separator(w=200, style='none')
    mc.iconTextButton( style='iconOnly', image1='{}/xgGuideContext.png'.format(pymel.util.getEnv("XBMLANGPATH").split(';')[0]), label='xgGuideTool', c=partial(xgGuideTool))
    mc.separator(w=40, style='none')
    mc.iconTextButton( style='iconOnly', image1='{}/xgFlipGuides.png'.format(pymel.util.getEnv("XBMLANGPATH").split(';')[0]), label='xgMirrorTool', c=partial(xgMirrorTool))
    mc.separator(w=40, style='none')
    mc.iconTextButton( style='iconOnly', image1='{}/xgGuideSculptTool.png'.format(pymel.util.getEnv("XBMLANGPATH").split(';')[0]), label='xgGuideTool', c=partial(xgSculptTool))
    mc.separator(w=40, style='none')
    
    mc.separator( h=40, style='none')
    mc.separator( style='none')
    mc.separator(style='none')
    mc.separator( style='none')
    mc.separator(style='none')
    mc.separator(style='none')
    mc.separator(style='none')

    mc.separator(w=200, style='none')
    mc.iconTextButton( style='iconOnly', image1='{}/xgToggleGuide.png'.format(pymel.util.getEnv("XBMLANGPATH").split(';')[0]), label='xgGuideTool', c=partial(xToggleGuideDisplay))
    mc.separator(w=40, style='none')
    mc.iconTextButton( style='iconOnly', image1='{}/xgToggleGuideReference.png'.format(pymel.util.getEnv("XBMLANGPATH").split(';')[0]), label='xgMirrorTool', c=partial(xToggleGuideReference))
    mc.separator(w=40, style='none')
    mc.iconTextButton( style='iconOnly', image1='rebuildCurve.png', label='xgGuideTool', c=partial(rebuildGuides))
    mc.separator(w=40, style='none')
    
    mc.setParent('..')

    child2 = mc.columnLayout(adj=True)
    mc.separator(h=10, style='none')
    mc.text(l='Enter the hotkey that you want to Guide Create Tool')
    mc.separator(h=10, style='none')
    edithot = mc.checkBox(l='Edit')
    lockhot = mc.checkBox(l='Lock', v=1)
    hotcket_text = mc.textField(it='l', editable=0)
    mc.separator(h=10, style='none')
    mc.button(l='Import Hotkeys', c=partial(hotkeyimport, hotcket_text))
    mc.checkBox(edithot, e=1, cc=partial(edithotk, hotcket_text, lockhot))
    mc.checkBox(lockhot, e=1, cc=partial(lockhotk, hotcket_text, edithot))
    mc.setParent('..')
    
    projectpath = mc.workspace(q=True, rd=True)
    try:
        xgenCollection = xgg.xgen.palettes()[0]
    except:
        xgenCollection = 0
    child3 = mc.rowColumnLayout()
    mc.separator(h=10, style='none')
    mc.text(l='Project Path is {}'.format(projectpath))
    mc.separator(h=10, style='none')
    collectname = mc.textFieldGrp(l='Collection', it=xgenCollection)
    exportpath = mc.textFieldButtonGrp(l='Path')
    mc.textFieldButtonGrp(exportpath, e=1, bc=partial(exportCollec, exportpath, collectname))
    mc.button(l='Export Collection', c=partial(exportCollectiontopath, collectname, exportpath))
    mc.setParent('..')

    child4 = mc.rowColumnLayout()
    mc.separator(h=10, style='none')
    mc.text(l='Project Path is {}'.format(projectpath))
    mc.separator(h=10, style='none')
    palcname = mc.optionMenu(l='Collection')
    try:
        pal = xgg.xgen.palettes()
        for x in range(int(len(pal))):
            mc.menuItem(label=pal[x])
        descname = mc.optionMenu(l='Description')
        desc = xgg.xgen.descriptions()
        for x in range(int(len(desc))):
            mc.menuItem(label=desc[x])
    except:
        pass
    exportDescpath = mc.textFieldButtonGrp(l='Path')
    mc.textFieldButtonGrp(exportDescpath, e=1, bc=partial(exportDesc, exportDescpath, descname))
    mc.button(l='Export Desciption', c=partial(exportDesctopath, descname, exportDescpath, palcname))
    mc.setParent('..')

    child5 = mc.rowColumnLayout(nc=3)
    mc.separator(h=10,w=200, style='none')
    mc.text(l='Set the number of CV in guides')
    mc.separator(h=10,w=200, style='none')
    mc.separator(h=10,w=200, style='none')
    mc.button(l='Convert Guides to Curves', c=partial(curvtoguides))
    mc.separator(h=10,w=200, style='none')
    mc.separator(h=10,w=200, style='none')
    mc.button(l='Export Curves as Abc', c=partial(exportCurvesAbc))
    mc.separator(h=10,w=200, style='none')
    mc.setParent('..')

    mc.tabLayout(tabs, edit=True, tabLabel=((child1, 'Buttons'), (child2, 'Hotkey'), (child3, 'Export Collections'), (child4, 'Export Descriptions'), (child5, 'Guides to Curves')))
    mc.setParent('..')
    mc.rowColumnLayout(nc=3)
    mc.separator(w=200, style='none')
    mc.text(l='If nothing appears click the REFRESH button', bgc=(.2,.3,.9))
    mc.separator(h=30, style='none')
    mc.setParent('..')

    mc.showWindow(myWindow)






