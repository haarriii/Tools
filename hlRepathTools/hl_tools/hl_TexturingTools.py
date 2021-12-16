# Autor Harriet Landa Gil 2020

import maya.cmds as mc
from functools import partial

def listSH(scroll, *args):
    '''
    Append all the aiStandardSurface, aiStandardHair and lambert to the scroll
    '''
    filters = ('aiStandardSurface', 'aiStandardHair', 'lambert')
    sel = mc.ls(type=filters)
    mc.textScrollList( scroll, e=1, ra=1)
    mc.textScrollList( scroll, e=1, append=sel)
    


def selObj(scroll, *args):
    '''
    Select the object with the selected shader
    '''
    scrollVal = mc.textScrollList( scroll, q=1, si=True)
    mc.select(scrollVal[0])
    mc.hyperShade(objects="")
    
def renameSH(scroll, *args):
    '''
    Create the UI for the renamer
    '''
    scrollVal = mc.textScrollList( scroll, q=1, si=True)
    if mc.window("renamer", exists=True, sizeable=True):
        mc.deleteUI("renamer")
    myWindow = mc.window("renamer", t="Shader Manager", w=300, h=300)
    mc.columnLayout()
    renamer = mc.textField()
    mc.button(l='Rename', c=partial(renameSHDS, scrollVal[0], renamer, scroll, myWindow))
    mc.showWindow(myWindow)

def renameSHDS(scrollVal, renamer, scroll, myWindow, *args):    
    '''
    Rename the Shader and close que renamer window
    '''
    newname = mc.textField(renamer, q=1, text=1)
    mc.rename(scrollVal, newname)
    filters = ('aiStandardSurface', 'aiStandardHair', 'lambert')
    sel = mc.ls(type=filters)
    mc.textScrollList( scroll, e=1, ra=1)
    mc.textScrollList( scroll, e=1, append=sel)
    mc.deleteUI(myWindow)
     
def selectSH(scroll, *args):
    '''
    Select the shader
    '''
    scrollVal = mc.textScrollList( scroll, q=1, si=True)
    mc.select(scrollVal[0])

def applySHD(scroll, *args):
    '''
    Apply the shader selected to the object selected
    '''
    selection = mc.ls(sl=True)
    scrollVal = mc.textScrollList( scroll, q=1, si=True)
    mc.hyperShade(a=scrollVal[0])

def createShader(scroll, *args):
    '''
    Create a new AiStandard Surface
    '''
    mc.shadingNode('aiStandardSurface', asShader=True)
    listSH(scroll)
def shaderManagerUI():
    '''
    Create the UI
    '''
    if mc.window("shader", exists=True, sizeable=True):
        mc.deleteUI("shader")

    myWindow = mc.window("shader", t="Shader Manager", w=300, h=300)
    layout = mc.rowColumnLayout(nc=2)
    lisbtn = mc.button(l='List Shaders')
    create = mc.button(l='Create Shader')
    scroll = mc.textScrollList(allowMultiSelection=False)
    mc.button(lisbtn, e=1, c=partial(listSH, scroll))
    mc.separator(style='none')
    lisbtn = mc.button(l='Select', c=partial(selectSH, scroll))
    lisbtn = mc.button(l='Rename', c=partial(renameSH, scroll))
    mc.button(l='Select the object with this material', c=partial(selObj, scroll))
    mc.button(l='Apply material to the selected object/s', c=partial(applySHD, scroll))
    mc.button(create, e=1, c=partial(createShader, scroll))
    mc.showWindow(myWindow)



  