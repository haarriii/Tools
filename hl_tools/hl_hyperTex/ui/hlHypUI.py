#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import pymel.core as pm

from functools import partial
import os

import hlHypFuncs as hyp_funcs
reload(hyp_funcs)

import hlHypLib as hypLib
reload(hypLib)
hyp_lib = hypLib.HypLibrary()

import config
reload(config)

import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(config._logging_level)



def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class HyperShadeUI(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(HyperShadeUI, self).__init__(parent)


        self.create_widgets()
        self.create_layout()
        self.create_connections()


    def create_widgets(self):
        """
        Create all the widgets for the window
        """
        ### create a QTableView to sort the shaders in a table ###
        self.table = QtWidgets.QTableView()
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        ### create a QLineEdit to filter the table's shaders ###
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.setPlaceholderText('Type for search shader')
        self.search_field.setStyleSheet('font-size: 10px; height: 20px;')
        self.search_field.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)

        ### populate the shaders in the table ###
        self.populateShaders()

        ### create the buttons ###
        self.apply_shader_btn = QtWidgets.QPushButton('Apply Material To Viewport Selection')
        self.sel_shader_btn = QtWidgets.QPushButton('Select Shader')
        self.rename_shader_btn = QtWidgets.QPushButton('Rename Shader')
        self.openHyper_btn = QtWidgets.QPushButton('Open Shader in HyperShade')
        self.flush_list = QtWidgets.QPushButton("Refresh List")

        ### create the labels and center ###
        self.obj_lbl = QtWidgets.QLabel('Objects With Selected Shader')
        self.obj_lbl.setAlignment(QtCore.Qt.AlignCenter)

        ### create the listWidget to add the objects with the selected shader ###
        self.list_wdg = QtWidgets.QListWidget()
        self.list_wdg.setResizeMode(QtWidgets.QListWidget.Adjust)

        self.list_wdg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_wdg.customContextMenuRequested.connect(self.on_right_click)

        ### create the lineedit to filter the objects ###
        self.obj_brw = QtWidgets.QLineEdit()
        self.obj_brw .setPlaceholderText('Type for search objects')
        self.obj_brw .setStyleSheet('font-size: 10px; height: 20px;')

    def create_layout(self):
        """
        Create all the layouts for the window
        """
        main_layout = QtWidgets.QHBoxLayout(self)

        ### shaders layout ###
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.search_field)
        layout.addWidget(self.table)

        ### buttons layout ###
        butn_layout = QtWidgets.QVBoxLayout()
        butn_layout.addWidget(self.apply_shader_btn)
        butn_layout.addWidget(self.sel_shader_btn)
        butn_layout.addWidget(self.rename_shader_btn)
        butn_layout.addWidget(self.openHyper_btn)
        butn_layout.addWidget(self.flush_list)

        ### objects layout ###
        obj_layout = QtWidgets.QVBoxLayout(self)
        obj_layout.setContentsMargins(2, 2, 2, 2)
        obj_layout.addWidget(self.obj_lbl)
        obj_layout.addWidget(self.obj_brw)
        obj_layout.addWidget(self.list_wdg)
        # obj_layout.addStretch(1)

        ### main layout ###
        main_layout.addLayout(obj_layout)
        main_layout.addLayout(layout)
        main_layout.addLayout(butn_layout)






    def create_connections(self):
        """
        Create all the connections for the widgets
        """
        ### buttons ###
        self.apply_shader_btn.clicked.connect(partial(hyp_funcs._applySHD, self.table))
        self.sel_shader_btn.clicked.connect(partial(hyp_funcs._selShader, self.table))
        self.openHyper_btn.clicked.connect(partial(hyp_funcs.graphShader, self.table))
        self.rename_shader_btn.clicked.connect(self.renameShader)
        self.flush_list.clicked.connect(self.flushList)

        ### list_wdg ###
        self.list_wdg.itemSelectionChanged.connect(self.on_click)

        self.list_wdg.customContextMenuRequested.connect(self.on_right_click)

        ### obj_brw ###
        self.obj_brw.textChanged.connect(self.on_search)

        ### table ###
        self.table.clicked.connect(self.onClickedRow)


    def renameShader(self):

        ### popup window to enter the name to rename the shader ###
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
        'Enter new name:')

        ### call the remaneShader function ###
        hyp_funcs.renameShader(self.table, text)

        ### refresh the shader list ###
        self.flushList()


    def on_search(self, text):
        """
        Function to hide and unhide the items depending the text of lineedit
        """
        for widget in self.assetsItems:
            if text in widget.text():
                widget.setHidden(False)
            else:
                widget.setHidden(True)

    def flushList(self):
        """
        Refresh the tableview ><
        """
        ### get all the shaders ###
        shaders_list = hyp_funcs._get_shaders()

        ### delete always the 0 row to refresh the table ###
        for i in range(len(shaders_list)):
            self.filter_proxy_model.removeRow(i-i)

        ### populate again with all the new shaders ###
        self.populateShaders()


    def populateShaders(self):

        ### get all the shaders in the scene ###
        shaders_list = hyp_funcs._get_shaders()

        ### create a standarditemmodel by the length of the shaders list ###
        self.model = QtGui.QStandardItemModel(len(shaders_list), 1)
        self.model.setHorizontalHeaderLabels(['Shaders'])

        ### add the shaders to the tableview ###
        for row, shader in enumerate(shaders_list):
            item = QtGui.QStandardItem(unicode(shader))
            self.model.setItem(row, 0, item)

        ### create a QSortFilterProxyModel to sort the shader using a QLineEdit ###
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)

        ### connect the QLineEdit to the tableView ###
        self.search_field.textChanged.connect(self.filter_proxy_model.setFilterRegExp)

        self.table.setModel(self.filter_proxy_model)

    def onClickedRow(self, item, index=None):
        """
        Function that executes when the clicked shader changed
        """
        ### clear and populate the objects list ###
        shader = item.data()
        self.obj_brw.clear()
        self.populateObj(shader)

    def on_right_click(self, point):
        """
        Function that executes when the right click on object
        """
        ### create a popMenu with some functions ###
        popMenu = QtWidgets.QMenu(self)
        selectAction = QtWidgets.QAction('frame to viewport', self)

        if self.list_wdg.itemAt(point):
            popMenu.addAction(selectAction)
        selectAction.triggered.connect(self.fitView)
        popMenu.exec_(self.list_wdg.mapToGlobal(point))

    def fitView(self):
        """
        Function that fit the object to the viewport
        """
        pm.viewFit()

    def on_click(self, fit=False):
        """
        Select the clicked object
        """
        item = self.list_wdg.selectedItems()[0]

        object_name = item.text()
        pm.select(object_name)

    def populateObj(self, shader=''):
        """
        Function to populate the object list
        """
        self.list_wdg.clear()
        objects_list = hyp_funcs._selObj(shader)
        if objects_list != False:
            objectsList_name = [each.name() for each in objects_list]
        else:
            objectsList_name = ['No objects with this shader']

        self.assetsItems = []
        for each in objectsList_name:
            item = QtWidgets.QListWidgetItem(each)
            self.list_wdg.addItem(item)
            self.assetsItems.append(item)

    def showUI(self):
        global ui
        try:
            ui.close() # pylint: disable=E0601
            ui.deleteLater()
        except:
            pass

        ui = HyperShadeUI()
        ui.show()
