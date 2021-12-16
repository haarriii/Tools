from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

import os
import json

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def read_json():
    '''
    This functions return all the json file text as a dict
    '''
    with open(r"P:\VFX_Project_17\Repath\tools\hlRepathTools\hl_tools\rp_import\Shaders_Path.json", 'r') as f:
        data2 = json.load(f)
    return data2


def get_key(ky):
    '''
    Function to get the value giving the key argument
    '''
    for key, value in read_json().items():
        if ky == key:
            return value

def shaders_disc(object):
    object = object
    shader_path = get_key(object)
    return shader_path


class DesignerUI(QtWidgets.QDialog):
    
    WINDOW_TITLE = "RP Scene Set"
    
    def __init__(self, parent=maya_main_window()):
        super(DesignerUI, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
        
        width = 250
        height = 200
       
        
        # setting  the fixed width of window
        self.setFixedWidth(width)
        self.setFixedHeight(height)
          

        self.init_ui()
        self.create_layout()
        self.create_connections()

    def init_ui(self):
        current_filepath = os.path.abspath(__file__)
        file_name = current_filepath.split('\\')[-1]
        current_path = current_filepath.rstrip(file_name)
       
        f = QtCore.QFile("{}main_ui.ui".format(current_path))
        f.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        
        self.ui = loader.load(f, parentWidget=None)

        f.close()

    def eyes_shd(self):
        
        eyes_shd_path = r'P:\VFX_Project_17\ftrack\PROJECT\02_PRODUCTION\ASSETS\CHARS\char_kaede\04_texturing\RESOURCES\char_kaede_eyes_SH.ma'
        cmds.file(eyes_shd_path, r=True, mnc=1, namespace=":")
        iris_shd_name = 'char_kaede_iris_SHD'
        cornea_R_shd_name = 'Kaede_Cornea_R_SHD'
        cornea_L_shd_name = 'Kaede_Cornea_L_SHD'
        earrings_shd_path = r'P:\VFX_Project_17\ftrack\PROJECT\02_PRODUCTION\ASSETS\CHARS\char_kaede\04_texturing\RESOURCES\char_kaede_earrings_SH.ma'
        earrings_shd_name = 'char_kaede_earrings_SHD'        
        pupil_shd_name = 'Kaede_Pupil_SHD'
        
        iris_list = ['Kaede:Kaede_eye_white_GRP']
        L_cornea_list = ['Kaede:L_Kaede_eye_glass_GEO']
        R_cornea_list = ['Kaede:R_Kaede_eye_glass_GEO']
        earrings_list = ['Kaede:Kaede_earrings_GRP']
        pupil_list = ['Kaede:Kaede_eye_iris_GRP']
        
        # char_kaede_iris_SHD >> Kaede:Kaede_eye_iris_GRP
        # Kaede_Cornea_R_SHD >> Kaede:R_Kaede_eye_glass_GEO
        # Kaede_Cornea_L_SHD >> Kaede:L_Kaede_eye_glass_GEO
        # Kaede_Pupil_SHD >> Kaede:Kaede_eye_white_GRP
        
        ### IRIS ###
        try:
            
            for each in iris_list:
                cmds.select(each)
                cmds.hyperShade(a=iris_shd_name)
        except:
            print('No se existe ningun objecto llamado: {}'.format(iris_list))
        ### PUPIL ###
        try:
            
            for each in pupil_list:
                cmds.select(each)
                cmds.hyperShade(a=pupil_shd_name)
        except:
            print('No se existe ningun objecto llamado: {}'.format(pupil_list))
        
        ### CORNEA ###
        try:
        
            for each in L_cornea_list:
                cmds.select(each)
                cmds.hyperShade(a=cornea_L_shd_name)
            for each in R_cornea_list:
                cmds.select(each)
                cmds.hyperShade(a=cornea_R_shd_name)
        except:
            print('No se existe ningun objecto llamado: {}'.format(cornea_list))
        
        ### EARRINGS ###
        try:
            cmds.file(earrings_shd_path, r=True, mnc=1, namespace=":")
        
            for each in earrings_list:
                cmds.select(each)
                cmds.hyperShade(a=earrings_shd_name)
        except:
            print('No se existe ningun objecto llamado: {}'.format(earrings_list))
            
    def applySHD(self, name):
       

        shd_path = str(shaders_disc(self.oDict['{}_objects'.format(name)][0].split(':')[0])[0]['path'])
        shd_name = str(shaders_disc(self.oDict['{}_objects'.format(name)][0].split(':')[0])[0]['name'])
        cmds.file(shd_path, r=True, mnc=1, itr="combine")
        cmds.select(self.oDict['{}_objects'.format(name)])
        cmds.hyperShade(a=shd_name)
        # cmds.select('Kaede:Kaede_eye_white_GRP')
        
        
    
    def create_layout(self):
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.ui)

    def create_connections(self):
        self.ui.btn_importabc.clicked.connect(self.importABC)
        self.ui.btn_importshd.clicked.connect(self.importSHD)
        self.ui.btn_eyes.clicked.connect(self.eyes_shd)
    

    def importABC(self):
        logger.debug('Importing alembics')
    
        current_filepath = cmds.file(q=True, sn=True)
        file_name = current_filepath.split('/')[-1]
        current_path = current_filepath.rstrip(file_name).rstrip('/').rstrip('v001')
        files = os.listdir(current_path)
        export_path = current_path + files[0]
        
        alembics_files = [each for each in os.listdir(export_path)]
        
        for abc in alembics_files:
            namespace = abc.split('_')[0]
            cmds.file(export_path + '/' + abc, reference=True, namespace=namespace)
     
        logger.debug('Alembics imported succesfully')
    
    def importSHD(self):
        logger.debug('Importing shaders')
        list_outliner = cmds.ls(assemblies=True)
        
        self.oDict = {}

        oList = ['Bag', 'Mechanicaldoor', 'Drone', 'Kaede', 'Path', 'Ozaru', 'Boots', 'Cloth', 'Earrings']
        
        for each in oList:
            self.oDict['{}_objects'.format(each)] = [file for file in list_outliner if '{}:'.format(each) in file]
            try:
                self.applySHD(each)
                logger.debug('Shaders imported succesfully')
            except:
                raise IOError('Error while importing shaders')
                pass
        
        
      


    

if __name__ == "__main__":

    try:
        designer_ui.close() # pylint: disable=E0601
        designer_ui.deleteLater()
    except:
        pass

    designer_ui = DesignerUI()
    designer_ui.show()
