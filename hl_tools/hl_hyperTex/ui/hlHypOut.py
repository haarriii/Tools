#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import json
from functools import partial
import os

import pymel.core as pm

import maya.cmds as cmds
import maya.OpenMayaUI as omui

import config
reload(config)

import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(config._logging_level)

import hlHypUI
reload(hlHypUI)

import hlHypLib as hypLib
reload(hypLib)
hyp_lib = hypLib.HypLibrary()

### get the data folder directory ###
DIR = hyp_lib._get_directory()


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class HlHypOutUI(QtWidgets.QWidget):

    def __init__(self, parent=maya_main_window()):
        super(HlHypOutUI, self).__init__(parent)

        self.init_ui()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def init_ui(self):
        """
        Import and apply the ui file to the maya window
        """
        p = os.path.join(os.path.dirname(__file__), 'ui')
        f = QtCore.QFile(r"{}\data_ui.ui".format(p))
        f.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()

        self.ui = loader.load(f, parentWidget=None)

        f.close()
    def create_widgets(self):
        """
        Create all the widgets for the window
        """
        self.ui.export_btn.setText('Export Selected Shader')

        self.ui.search_line.setPlaceholderText('Type for search')
        self.ui.search_line.setStyleSheet('font-size: 10px; height: 20px;')
        self.ui.type_lbl.setText('Filter Shader By')

        self.add_items_combobox()

        self.ui.type_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.data_list_wdg.setViewMode(QtWidgets.QListWidget.IconMode)
        self.ui.data_list_wdg.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.ui.data_list_wdg.setIconSize(QtCore.QSize(20, 20))
        self.ui.data_list_wdg.setMovement(QtWidgets.QListWidget.Static)
        self.ui.data_list_wdg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.data_list_wdg.customContextMenuRequested.connect(self.on_right_click)

        self.populate()

    def create_layout(self):
        """
        Create all the layouts for the window
        """
        main_layout = QtWidgets.QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.ui)

    def create_connections(self):
        """
        Create all the connections for the widgets
        """
        self.ui.export_btn.clicked.connect(self.exportShader)
        self.ui.type_cb.currentTextChanged.connect(self.on_combobox_changed)
        self.ui.search_line.textChanged.connect(self.on_search)

    def add_items_combobox(self):
        """
        Populate the comboBox
        """
        ### clear the comboBox ###
        self.ui.type_cb.clear()

        ### get the type from the json file ###
        self.json_info = self.get_shaders_type()
        types = set([i[0] for i in self.json_info])

        self.ui.type_cb.addItem("ALL")
        for each in types:
            self.ui.type_cb.addItem(each)

    def get_shaders_type(self):
        """
        Return the types of the shaders
        """
        files = os.listdir(DIR)

        infoFiles = [f for f in files if f.endswith('.json')]
        types = []
        for info in infoFiles:
            name, ext = os.path.splitext(info)
            with open(os.path.join(DIR, info), 'r') as f:
                data = json.load(f)
                types.append((tuple((data['type'], data['name']))))
        return types

    def populate(self, type=None):
        """
        Populate the items and add the icons
        """
        ### get the icons folder to add in the items ###
        path, lastFolder = os.path.split(os.path.dirname(__file__))
        srcPath = os.path.join(path, 'src', 'icon')

        iconPath = os.path.join(srcPath, os.listdir(srcPath)[0])

        ### clear the list widget to repopulate ###
        self.ui.data_list_wdg.clear()

        ### manualy list the files because a hard arror ocurred when executing this module ###
        files = os.listdir(DIR)

        mayaFiles = [f for f in files if f.endswith('.ma')]

        self.assetList = []
        if type==None:
            for ma in mayaFiles:
                name, ext = os.path.splitext(ma)
                item = QtWidgets.QListWidgetItem(name)
                icon = QtGui.QIcon(iconPath)
                item.setIcon(icon)
                self.ui.data_list_wdg.addItem(item)
                self.assetList.append(item)
        else:
            for ma in mayaFiles:
                name, ext = os.path.splitext(ma)
                for each in type:
                    if name in each:
                        item = QtWidgets.QListWidgetItem(name)
                        icon = QtGui.QIcon(iconPath)
                        item.setIcon(icon)
                        self.ui.data_list_wdg.addItem(item)
                        self.assetList.append(item)
                    else:
                        pass


    def on_combobox_changed(self):
        """
        Function that executes when comboBox changed
        """
        if self.ui.type_cb.currentText() != 'ALL':
            ret = [each[1] for each in self.json_info if each[0]==self.ui.type_cb.currentText()]
            self.populate(type=ret)
        else:
            self.populate(type=None)

    def on_search(self, text):

        for widget in self.assetList:
            if text in widget.text():
                widget.setHidden(False)
            else:
                widget.setHidden(True)



    def on_right_click(self, point):
        """
        Function that executes when the right click on object
        """
        ### create the QMenu to right click actions ###
        popMenu = QtWidgets.QMenu(self)
        importAction = QtWidgets.QAction('import', self)
        refeAction = QtWidgets.QAction('reference', self)
        deleteAction = QtWidgets.QAction('delete', self)

        if self.ui.data_list_wdg.itemAt(point):
            popMenu.addAction(importAction)
            popMenu.addAction(refeAction)
            popMenu.addAction(deleteAction)

        importAction.triggered.connect(self.importAsset)
        refeAction.triggered.connect(self.referenceAsset)
        deleteAction.triggered.connect(self.on_delete)
        popMenu.exec_(self.ui.data_list_wdg.mapToGlobal(point))

    def exportShader(self):
        '''
        This functions export the selected geometry or shader to the data folder and appears in the library
        '''
        try:
            shader = pm.selected()[0]
            hyp_lib.save(shader)
            self.populate()
            self.add_items_combobox()
            self.msgBox('Exported {} to data folder'.format(shader), type='Information')
        except:
            self.msgBox('Must select something to export', type='Warning')


    def on_delete(self):
        '''
        Function to delete the selected item from library
        '''

        hyp_lib.find()
        hyp_lib.delete(self.ui.data_list_wdg.currentItem().text())
        self.populate()
        self.add_items_combobox()

    def importAsset(self):
        '''
        Functions to import the selected item from library to current scene
        '''
        hyp_lib.find()
        hyp_lib.load(self.ui.data_list_wdg.currentItem().text())

        hypUI = hlHypUI.HyperShadeUI()
        hypUI.populateShaders()
        _logger.debug('Imported: {}'.format(self.ui.data_list_wdg.currentItem().text()))

    def referenceAsset(self):
        '''
        Functions to reference the selected item from library to current scene
        '''
        hyp_lib.find()
        hyp_lib.reference(str(self.ui.data_list_wdg.currentItem().text()))
        _logger.debug('Referenced: {}'.format(self.ui.data_list_wdg.currentItem().text()))
    def msgBox(self, text, type='Information'):
        '''
        This funcions create a pop-up window depends of -type flags: "Information", "Warning"
        '''
        mB = QtWidgets.QMessageBox()
        mB.setWindowTitle('Hyper Message')
        mB.setText(text)
        if type == 'Information':
            mB.setIcon(QtWidgets.QMessageBox.Information)
        elif type == 'Warning':
            mB.setIcon(QtWidgets.QMessageBox.Warning)

        mB.exec_()

