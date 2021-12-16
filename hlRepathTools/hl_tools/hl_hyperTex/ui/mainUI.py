#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import sys

import os

import maya.cmds as cmds

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya.OpenMayaUI as omui

import hlHypUI
reload(hlHypUI)

import customTabWdg
reload(customTabWdg)

import hlHypOut
reload(hlHypOut)


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class UI(QtWidgets.QWidget):

    WINDOW_TITLE = "RP_Hyper"
    UI_NAME = "RP_Hyper"
    label = WINDOW_TITLE

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)

        width = 900
        height = 250

        self.setWindowTitle(self.WINDOW_TITLE)
        # self.setFixedSize(width, height)
        self.setMinimumSize(width, height)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.setIcon()

    def setIcon(self):
        """
        Function to add a icon to the window top left
        """
        path, lastFolder = os.path.split(os.path.dirname(__file__))
        srcPath = os.path.join(path, 'src', 'icon')

        appIcon = QtGui.QIcon(os.path.join( srcPath, 'window_icon.png'))
        self.setWindowIcon(appIcon)


    def create_widgets(self):
        """
        Create all the widgets for the window
        """

        self.save_wdg = hlHypUI.HyperShadeUI()
        self.hypout_ui = hlHypOut.HlHypOutUI()

        self.tab_widget = customTabWdg.CustomTabWidget()
        self.tab_widget.addTab(self.save_wdg, "Hyper")
        self.tab_widget.addTab(self.hypout_ui, "Library")


    def create_layouts(self):
        """
        Create all the layouts for the window
        """
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.tab_widget)


        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(button_layout)

    def showUI(self):
        global win

        try:
            win.close() # pylint: disable=E0601
            win.deleteLater()
        except:
            pass

        win = UI()
        win.show()

