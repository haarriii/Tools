#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui


def Dock(Widget, width=2, show=True):

    name = Widget.__name__
    label = getattr(Widget, "label", name)

    try:
        cmds.deleteUI(name)
    except RuntimeError:
        print("UI could not be deleted")

    dockControl = cmds.workspaceControl(name,
            # minimumWidth = True,
            # initialWidth = width,
            retain=True,
            label = label,
            # tabToControl=['AttributeEditor', -1]
            )

    dockPtr = omui.MQtUtil.findControl(dockControl)
    dockWidget = wrapInstance(long(dockPtr), QtWidgets.QWidget)
    dockWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    myInstance = Widget(parent=dockWidget)
    dockWidget.layout().addWidget(myInstance)

    if show:
        cmds.evalDeferred(lambda *args: cmds.workspaceControl(
            dockControl, e=1, restore=1, retain=1))
            # tabToControl=['AttributeEditor', -1]

    return myInstance