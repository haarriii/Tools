# Autor Harriet Landa Gil 2020

import maya.cmds as mc
from functools import partial
import os
import subprocess


def activesetting(program, subsformat, subsframe, *args):
    '''
    Get enable the optionMenu of this prog to change the format to send
    '''
    prog = mc.optionMenu(program, q=1, v=1)
    if prog == 'Substance Painter':
        mc.frameLayout(subsframe, e=1, collapse=0)
        mc.optionMenu(subsformat, e=1, enable=1)
    else:
        mc.warning('SELECIONE UN PROGRAMA')


def renameOutliner(newname, *args):
    
    select = mc.ls(sl=1)
    textonombre = mc.textField(newname, q=1, text=1)
    mc.rename(select[0], textonombre)
    mc.deleteUI("confirmacion")


def si_renamer():

    if mc.window("confirmacion", exists=True, sizeable=True):
        mc.deleteUI("confirmacion")

    myWindow = mc.window('confirmacion', title='Renamer',
                         w=20, h=30, sizeable=True)
    mc.columnLayout(adj=1)
    mc.text(l='Rename')
    mc.separator(h=20, w=370)
    newname = mc.textField()
    mc.separator(h=20)
    mc.button(l='Rename', c=partial(renameOutliner, newname))

    mc.showWindow(myWindow)


def sendExp(program, subsformat, substancepath, *args):
    '''
    Depends on the program selected in the exporterUI function , send the selected object to it
    '''
    projectpath = mc.workspace(q=True, act=True)
    prog = mc.optionMenu(program, q=1, v=1)
    select = mc.ls(sl=1)
    if prog == 'Substance Painter':  # SUBSTANCEE###
        fileformat = mc.optionMenu(subsformat, q=1, v=1)
        # print(fileformat)
        if len(select) > 0:
            conf = mc.confirmDialog(title='Confirm', message='El nombre del archivo sera el nombre del Outliner, quieres cambiarlo?', button=[
                                    'Si', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No', icon='question')
            if conf == 'Si':
                si_renamer()
            elif conf == 'No':
                if fileformat == '.obj':
                    exportpath = '{}//exports//mayatosubs//{}'.format(
                        projectpath, str(select[0] + '.obj'))
                    expPath = os.path.join(
                        projectpath, 'exports', 'mayatosubs')
                    if not os.path.exists(expPath):
                        os.makedirs(expPath)
                    mc.file(exportpath, force=True, typ="OBJexport", es=1,
                            op="groups=0; ptgroups=0; materials=0; smoothing=0; normals=0")
                    ### Substance Exe path###
                    programPath = mc.textFieldButtonGrp(substancepath, q=1, text=1)
                    print('Object send to {}'.format(expPath))
                    sendcode = '"{}" --mesh {} --split-by-udim'.format(programPath, exportpath)
                    subprocess.Popen(sendcode)
                else:
                    exportpath = '{}//exports//mayatosubs//{}'.format(
                        projectpath, str(select[0] + '.fbx'))
                    expPath = os.path.join(
                        projectpath, 'exports', 'mayatosubs')
                    if not os.path.exists(expPath):
                        os.makedirs(expPath)
                    mc.FBXExport('-file', exportpath, '-s')
                    ### Substance Exe path###
                    programPath = mc.textFieldButtonGrp(substancepath, q=1, text=1)
                    print('Object send to {}'.format(expPath))
                    sendcode = '"{}" --mesh {} --split-by-udim'.format(programPath, exportpath)
                    subprocess.Popen(sendcode)
        else:
            mc.warning('SELECCIONA ALGOO!!')
def changeexepath(substancepath, *args):
    '''
    Open a dialog to change the exe path of the prigram selected
    '''
    basicFilter = "*.exe"
    pathtochange = mc.fileDialog2(fileFilter=basicFilter, dialogStyle=2, okCaption='Change')[0]
    print('Your path change to :'.format(pathtochange))
    mc.textFieldButtonGrp(substancepath, e=1, text=pathtochange)
     

def exporterUI():
    '''
    The main function to create the UI
    '''
    if mc.window("exporterr", exists=True, sizeable=True):
        mc.deleteUI("exporterr")

    projectpath = mc.workspace(q=True, act=True)
    myWindow = mc.window('exporterr', title='Export Window',
                         w=20, h=30, sizeable=True)
    mc.columnLayout(adj=1)
    mc.textField(it='current proj:  ' + projectpath, editable=False)
    mc.text(l='Select the program you want to export')
    mc.separator(h=20, w=370)
    program = mc.optionMenu(label='Program')
    mc.menuItem(label='None')
    mc.menuItem(label='Substance Painter')

    mc.separator(h=20)
    send = mc.button(l='Send/Export')
    mc.separator(h=20, style='none')
    mc.text(l='The object will be exported to the exports folder in your current project')
    mc.separator(h=20, style='none')
    subsframe = mc.frameLayout(
        l='Substance Painter Settings', collapsable=1, collapse=1)
    progpath = r"C:\Program Files\Allegorithmic\Substance Painter\Substance Painter.exe"
    substancepath = mc.textFieldButtonGrp(l='exe path:' , it=progpath, bl='Change Path')
    mc.textFieldButtonGrp(substancepath, e=1, bc=partial(changeexepath, substancepath))
    subsformat = mc.optionMenu(label='Format', enable=0)
    mc.menuItem(label='.obj')
    mc.menuItem(label='.fbx')
    mc.setParent('..')
    mc.button(send, e=1, c=partial(sendExp, program, subsformat, substancepath))
    mc.optionMenu(program, e=1, cc=partial(activesetting, program, subsformat, subsframe))
    mc.showWindow(myWindow)


