# Autor Harriet Landa Gil 2020

import maya.cmds as mc
from functools import partial
import os

def set_project(*args):
    '''
    This funcion find the workspace file to set the project
    ''' 
    proj = mc.fileDialog2(cap='Set Project', dialogStyle=2, fm=3)
    project = str(proj[0])
    mc.workspace(project, o=True)


def open_asset(prjNameOP, assnameOP, prodStepOP, vesionOP, *args):
    '''
    This funcion open a scene with the UI parameters , this scene opens directly from the project path without search it
    ''' 
    projectpath = mc.workspace(q=True, rd=True)
    ### Seach for the assets folder and if it don't exists, create ###
    if os.path.exists(projectpath + 'assets/'):
        assetpath = projectpath + 'assets/'
    else:
        os.makedirs(projectpath + 'assets/')
        assetpath = projectpath + 'assets/'
    
    projectName = mc.optionMenu(prjNameOP, q=1, v=1)
    stepName = mc.optionMenu(prodStepOP, q=1, v=1) 
    versionNumber = mc.optionMenu(vesionOP, q=1, v=1) 
    assetName = mc.textField(assnameOP, q=True, text=True)
    sceneFile_name = assetpath + projectName + '_' + assetName + '_' + stepName + '_' + versionNumber + '.ma'
    ### Open scene ###
    try:
        mc.file(sceneFile_name, o=True, force=True)
    except:
        mc.warning(r"{} file don't exists".format(sceneFile_name))


def open_scene(projSC, shotSC, prodStepSC, verSC, *args):
    '''
    This funcion open a scene with the UI parameters , this scene opens directly from the project path without search it
    '''
    projectpath = mc.workspace(q=True, rd=True)
    projectName = mc.optionMenu(projSC, q=1, v=1)
    stepName = mc.optionMenu(prodStepSC, q=1, v=1) 
    versionNumber = mc.optionMenu(verSC, q=1, v=1) 
    shotNumber = mc.optionMenu(shotSC, q=1, v=1) 
    sceneFile_name = projectpath + 'scenes/' + projectName + '_' + shotNumber + '_' + stepName + '_' + versionNumber + '.ma'
    ### Open scene ###
    try:
        mc.file(sceneFile_name, o=True, force=True)
    except:
        mc.warning(r"{} file don't exists".format(sceneFile_name))


def scene_asset(project, assname, prodStep, version, *args):
    '''
    This funcion save a scene with the UI parameters for the naming, this scene saves directly in the assets folfer from the project path
    ''' 
    stepName = mc.optionMenu(prodStep, q=1, v=1) 
    projectpath = mc.workspace(q=True, rd=True)
    ### Seach for the assets folder and if it don't exists, create ###
    if os.path.exists(projectpath + 'assets/'):
        assetpath = projectpath + 'assets/'
    else:
        os.makedirs(projectpath + 'assets/')
        assetpath = projectpath + 'assets/'
    projectName = mc.textField(project, q=True, text=True)
    assetName = mc.textField(assname, q=True, text=True)
    versionVAlue = mc.textField(version, q=True, text=True)
    sceneFile_name = projectName + '_' + assetName + '_' + stepName + '_v0' + versionVAlue
    finalexport = assetpath + sceneFile_name + '.ma'
    ### Reaname the scene file with UI parameters ###
    mc.file(rename=finalexport)
    ### Save the file in mayaAscii ###
    mc.file(save=True, type='mayaAscii')
    ### Printing to know where the scene has been saved ###
    print('Scene save in {}'.format(finalexport))


def scene_name(projectu, shotv, prodStepScene, versionS, *args):
    '''
    This funcion save a scene with the UI parameters for the naming, this scene saves directly in the assets folfer from the project path
    ''' 
    projectpath = mc.workspace(q=True, rd=True)
    exportPath = mc.fileDialog2(fm=3, okc='Save Scene', cap='Save the Scene', dir=projectpath + '/scenes/')[0]
    prodStep = mc.optionMenu(prodStepScene, q=1, v=1) 
    projectName = mc.textField(projectu, q=True, text=True)
    shotNumber = mc.textField(shotv, q=True, text=True)
    versionNumber = mc.textField(versionS, q=True, text=True)
    sceneFile_name = projectName + '_' + 's0' + shotNumber + '_' + prodStep + '_' + 'v0' + versionNumber
    finalexport = exportPath + sceneFile_name + '.ma'
    ### Reaname the scene file with UI parameters ###
    mc.file(rename=exportPath + '/' + sceneFile_name)
    ### Save the file in mayaAscii ###
    mc.file(save=True, type='mayaAscii')
    ### Printing to know where the scene has been saved ###
    print('Scene save in {}'.format(finalexport))

def sceneEditor():
    '''
    The main funcion who creates the UI whit all the parameters and tabs
    '''
    if mc.workspaceControl("scenewin", exists=True):
        mc.deleteUI('scenewin', layout=True)
        mc.workspaceControlState('scenewin', remove=True)

    ### Find the AttrubuteEditor window to parent in the same place the windows and collapse for open it at the click###    
    myWindow = mc.workspaceControl('scenewin', tabToControl=('AttributeEditor', -1), label='Scene Setup', collapse=False)


    form = mc.formLayout()
    tabs = mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    mc.formLayout(form, edit=True,
                  attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))

    ### Tabs with the same first button to set the project ###   
    ### Each tab do something differents , 1 - save asset, 2 - save shot, 3 - open asset, 4 - open shot ###
    
    child1 = mc.columnLayout(adj=True)
    mc.button(h=30, l="Set Project", c=partial(set_project))
    mc.separator()

    mc.text(l='Project Name')
    project = mc.textField('Project', editable=True, it='Repath')
    mc.text(l='Asset Name')
    assname = mc.textField('assname', editable=True)
    prodStep = mc.optionMenu(label='Production Step')
    mc.menuItem(label='baseMesh')
    mc.menuItem(label='retopo')
    mc.menuItem(label='rig')
    mc.menuItem(label='texture')
    mc.menuItem(label='publish')
    mc.text(l='Scene Version')
    version = mc.textField('Version', editable=True)
    
    mc.separator()

    mc.button(h=30, l="Scene Name and Save Asset", c=partial(scene_asset, project, assname, prodStep, version))
    mc.separator(h=2, style='none')
    projectpath = mc.workspace(q=True, rd=True)
    mc.textField(it=projectpath, editable=0) 
    
    mc.setParent('..')

    child2 = mc.columnLayout(adj=True)
    mc.button(h=30, l="Set Project", c=partial(set_project))
    mc.text(l='Project Name')
    projectu = mc.textField('Project', editable=True, it='Repath')
    mc.text(l='Shot Number')
    shotv = mc.textField('Shot', editable=True)
    prodStepScene = mc.optionMenu(label='Production Step')
    mc.menuItem(label='blocking')
    mc.menuItem(label='renderProxy')
    mc.menuItem(label='lighting')
    mc.menuItem(label='texturing')
    mc.menuItem(label='lookDev')
    mc.text(l='Scene Version')
    versionS = mc.textField('Version', editable=True)

    mc.button(h=30, l="Scene Name and Save Scene", c=partial(scene_name, projectu, shotv, prodStepScene, versionS))
    mc.separator(h=2, style='none')
    projectpath = mc.workspace(q=True, rd=True)
    mc.textField(it=projectpath, editable=0)

    mc.setParent('..')

    child3 = mc.columnLayout(adj=True)
    mc.button(h=30, l="Set Project", c=partial(set_project))
    
    mc.separator()

    prjNameOP = mc.optionMenu(label='Project Name')
    mc.menuItem(label='Repath')

    mc.text(l='Asset Name')
    assnameOP = mc.textField('assname', editable=True)

    prodStepOP = mc.optionMenu(label='Production Step')
    mc.menuItem(label='baseMesh')
    mc.menuItem(label='retopo')
    mc.menuItem(label='rig')
    mc.menuItem(label='texture')
    mc.menuItem(label='publish')

    vesionOP = mc.optionMenu(label='Version')
    for x in range(120):
        mc.menuItem(label='v0{}'.format(x+1))
        

    mc.button(h=30, l="Open Asset", c=partial(open_asset, prjNameOP, assnameOP, prodStepOP, vesionOP))
    mc.separator(h=2, style='none')
    projectpath = mc.workspace(q=True, rd=True)
    mc.textField(it=projectpath, editable=0)
    mc.setParent('..')

    child4 = mc.columnLayout(adj=True)
    mc.button(h=30, l="Set Project", c=partial(set_project))
    
    mc.separator()

    projSC = mc.optionMenu(label='Project Name')
    mc.menuItem(label='None')
    mc.menuItem(label='Repath')

    shotSC = mc.optionMenu(label='Shot')
    for x in range(20):
        mc.menuItem(label='s0{}'.format(x+1))
        

    prodStepSC = mc.optionMenu(label='Production Step')
    mc.menuItem(label='renderProxy')
    mc.menuItem(label='lighting')
    mc.menuItem(label='texturing')
    mc.menuItem(label='lookDev')
    mc.menuItem(label='publish')

    
    
    verSC = mc.optionMenu(label='Version')
    for x in range(120):
        mc.menuItem(label='v0{}'.format(x+1))


    mc.button(h=30, l="Open Scene", c=partial(open_scene, projSC, shotSC, prodStepSC, verSC))
    mc.separator(h=2, style='none')
    projectpath = mc.workspace(q=True, rd=True)
    mc.textField(it=projectpath, editable=0)
    mc.setParent('..')
    
    ### Rename all the tabs dependening in their functions ###
    mc.tabLayout(tabs, edit=True,
                 tabLabel=(
                     (child1, 'Save Asset'), (child2, 'Save Shot'), (child3, 'Open Asset'), (child4, 'Open Scene')))


