from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class CustomTabWidget(QtWidgets.QWidget):

    def __init__(self, parent=maya_main_window()):
        """
        This is a modified TabWidget with different characteristics
        """

        super(CustomTabWidget, self).__init__(parent)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """
        Create QTabBar widgets
        """

        ### create and set the stylesheet for a QTabBar ###
        self.tab_bar = QtWidgets.QTabBar()
        self.tab_bar.setObjectName("customTabBar")
        self.tab_bar.setStyleSheet("#customTabBar {background-color: #383838}")

        ### create and set the stylesheet for a QStackedWidget ###
        self.stacked_wdg = QtWidgets.QStackedWidget()
        self.stacked_wdg.setObjectName("tabBarStackedWidget")
        self.stacked_wdg.setStyleSheet("#tabBarStackedWidget {border: 1px solid #2e2e2e}")

    def create_layout(self):
        """
        Create QTabBar widgets
        """
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.tab_bar)
        main_layout.addWidget(self.stacked_wdg)

    def create_connections(self):
        """
        Create QTabBar connections
        """
        self.tab_bar.currentChanged.connect(self.stacked_wdg.setCurrentIndex)

    def addTab(self, widget, label):
        """
        Adding a TabBar to the layout
        """
        self.tab_bar.addTab(label)

        self.stacked_wdg.addWidget(widget)