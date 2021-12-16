# Autor Harriet Landa Gil 2020

import pymel.core as pm
import maya.cmds as mc
import sys
import json
import os
import getpass

print('Loading Repath Tools')

### All this scripts works on Windows and Mac ###

### Get the root path ###
root = os.path.dirname(__file__)
if 'hl_menu' in root:
    root = root.replace('hl_menu', '')

p = r'{}/hl_json'.format(root)

toolsPath = r'{}/hl_tools'.format(root)

### Insert sctrips folder in the sys.path ###
if not toolsPath in sys.path:
    sys.path.insert(0, toolsPath)

print(root)

if r'P:\VFX_Project_17\Repath\tools\hlRepathTools\hl_tools\studiolibrary\src' not in sys.path:
    sys.path.insert(0, r'P:\VFX_Project_17\Repath\tools\hlRepathTools\hl_tools\studiolibrary\src')

def read_json():
    '''
    This functions return all the json file text as a dict
    '''
    with open(r'{}\hl_ToolsInfo.json'.format(p), 'r') as f:
        data2 = json.load(f)
    return data2


def get_key(ky):
    '''
    Function to get the value giving the key argument
    '''
    for key, value in read_json().items():
        if ky == key:
            return value

### A funcion to get each dict in the general dict from the read_json function ###

def scene_dicts():
    read_json()
    scenemenu_dict = get_key('Scenemenu')
    return scenemenu_dict


def uv_dicts():
    read_json()
    uv_dict = get_key('UVmenu')
    return uv_dict


def model_dicts():
    read_json()
    model_dict = get_key('Modelingmenu')
    return model_dict


def ld_dicts():
    read_json()
    ld_dict = get_key('LookDevmenu')
    return ld_dict


def tx_dicts():
    read_json()
    tx_dict = get_key('Texturingmenu')
    return tx_dict

def rnd_dicts():
    read_json()
    rnd_dict = get_key('Rendermenu')
    return rnd_dict

def xgen_dicts():
    read_json()
    xgen_dict = get_key('XGenmenu')
    return xgen_dict

def rig_dicts():
    read_json()
    rig_dict = get_key('Rigmenu')
    return rig_dict

def gear_dicts():
    read_json()
    gear_dict = get_key('Gearsmenu')
    return gear_dict

def sl_dicts():
    read_json()
    sl_dict = get_key('StudioLibrary')
    return sl_dict


def main_Menu():
    '''
    The main funcion , create a menu with some menuentries in the top of the maya's workspace
    '''
    ### a dict to put all the diferents menus and menuentries ###
    menu_tools = {}
    ### the menu name label depends from the username of the user ###
    winUsername = 'Repath_' + getpass.getuser()

    if mc.menu(winUsername, exists=True):
        mc.deleteUI(winUsername)

    MainMayaWindow = pm.language.melGlobals['gMainWindow']

    menu_tools['MENU'] = mc.menu(winUsername, to=True, parent=(MainMayaWindow))
    menu_tools['Scenes'] = mc.menuItem(subMenu=True, to=True, label='Scenes')
    menu_tools['Scenes.scenesEditor'] = mc.menuItem(label=str(
        scene_dicts()[0]['label']), to=True, c=str(scene_dicts()[0]['python']))
    menu_tools['Scenes.exporter'] = mc.menuItem(label=str(
        scene_dicts()[1]['label']), to=True, c=str(scene_dicts()[1]['python']))
    mc.setParent('..', menu=True)
    menu_tools['Modeling.Modeling'] = mc.menuItem(
        subMenu=True, to=True, label='Modeling')
    menu_tools['Modeling.hardEdges'] = mc.menuItem(label=str(
        model_dicts()[0]['label']), to=True, c=str(model_dicts()[0]['python']))
    menu_tools['Modeling.modelingtools'] = mc.menuItem(label=str(
        model_dicts()[1]['label']), to=True, c=str(model_dicts()[1]['python']))
    menu_tools['Modeling.cableTool'] = mc.menuItem(label=str(
        model_dicts()[2]['label']), to=True, c=str(model_dicts()[2]['python']))
    mc.setParent('..', menu=True)
    menu_tools['Gear'] = mc.menuItem(subMenu=True, to=True, label='Gears')
    menu_tools['Gear.gearstool'] = mc.menuItem(
        label=str(gear_dicts()[0]['label']), to=True, c=str(gear_dicts()[0]['python']))
    mc.setParent('..', menu=True)
    menu_tools['Rig'] = mc.menuItem(subMenu=True, to=True, label='Rigging')
    menu_tools['Rig.rigtools'] = mc.menuItem(
        label=str(rig_dicts()[0]['label']), to=True, c=str(rig_dicts()[0]['python']))
    mc.setParent('..', menu=True)
    menu_tools['UV'] = mc.menuItem(subMenu=True, to=True, label='UV')
    menu_tools['UV.uvtoolkit'] = mc.menuItem(
        label=str(uv_dicts()[0]['label']), to=True, c=str(uv_dicts()[0]['python']))
    mc.setParent('..', menu=True)
    menu_tools['Texturing'] = mc.menuItem(
        subMenu=True, to=True, label='Texturing')
    menu_tools['Texturing.shadermanger'] = mc.menuItem(
        label=str(tx_dicts()[0]['label']), to=True, c=str(tx_dicts()[0]['python']))
    menu_tools['Texturing.autoshader'] = mc.menuItem(
        label=str(tx_dicts()[1]['label']), to=True, c=str(tx_dicts()[1]['python']))
    mc.setParent('..', menu=True)
    menu_tools['LookDev'] = mc.menuItem(subMenu=True, to=True, label='LookDev')
    menu_tools['LookDev.autolookdev'] = mc.menuItem(
        label=str(ld_dicts()[0]['label']), to=True, c=str(ld_dicts()[0]['python']))
    mc.setParent('..', menu=True)
    menu_tools['XGen'] = mc.menuItem(subMenu=True, to=True, label='XGen')
    menu_tools['XGen.xgentool'] = mc.menuItem(
        label=str(xgen_dicts()[0]['label']), to=True, c=str(xgen_dicts()[0]['python']))
    mc.setParent('..', menu=True)
    menu_tools['Rendering'] = mc.menuItem(
        subMenu=True, to=True, label='Rendering')
    menu_tools['Rendering.renderOP'] = mc.menuItem(
        label=str(rnd_dicts()[0]['label']), to=True, c=str(rnd_dicts()[0]['python']))
    mc.setParent('..', menu=True)
    menu_tools['StudioLibrary'] = mc.menuItem(
        subMenu=True, to=True, label='StudioLibrary')
    menu_tools['StudioLibrary.tool'] = mc.menuItem(
        label=str(sl_dicts()[0]['label']), to=True, c=str(sl_dicts()[0]['python']))
    mc.setParent('..', menu=True)
    


print('Repath Tools loaded')


