#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymel.core as pm
import maya.cmds as cmds

import config
reload(config)

import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(config._logging_level)

def _get_shaders():
    """
    Return the shaders from the current maya scene
    """
    filters = ('aiStandardSurface', 'aiStandardHair', 'lambert', 'aiFlat')
    shaders_list = pm.ls(type=filters)
    return shaders_list


def _get_current_shader(item):
    """
    Return the selected shader name from the table selection
    """
    index = item.selectionModel().currentIndex()
    value = index.data()
    return value

def _applySHD(item):
    """
    Apply thr selected shader to the selected geometry in the viewport
    """
    shader = _get_current_shader(item)

    selection = pm.ls(sl=True)
    pm.hyperShade(a=shader)
    _logger.debug("Apply '{}' to : {}".format(shader, selection))

def _selObj(shader):
    """
    Return the objects with shader selection
    """
    selected = pm.selected()
    pm.select(cl=1)
    pm.select(shader)
    sel = pm.selected()
    pm.hyperShade(objects="")
    object_list = pm.selected()
    if object_list:
        if object_list != sel:
            object_list = object_list
        else:
            object_list = False
    else:
        object_list = False
    pm.select(selected)
    return object_list

def _selShader(item):
    """
    Select the selected shader
    """
    shader = _get_current_shader(item)
    return pm.select(shader)

def graphShader(item):
    """
    Open the HyperShade with selected shader
    """
    shader = _get_current_shader(item)

    import maya.mel as mel
    pm.select(shader)
    ### open the hypershade ###
    cmds.HypershadeWindow()
    ### get the hypershade windows panel name or id ###
    hyPanel = cmds.getPanel(withFocus=True)
    ### graph the shader on the hypershade graph ###
    mel.eval("hyperShadePanelGraphCommand(\"{}\", \"addSelected\")".format(hyPanel))

def renameShader(item, newName):
    """
    Rename selected shader
    """
    shader = _get_current_shader(item)
    pm.rename(shader, newName)
    _logger.debug("'{}' changed name to '{}'".format(shader, newName))