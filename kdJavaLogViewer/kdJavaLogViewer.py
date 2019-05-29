'''
Created on 2019年5月20日

@author: bkd
'''
'''
Created on 2019年5月9日

@author: bkd
'''

from os.path import expanduser, join, exists
from shutil import copy2
import sys

from PyQt5.Qt import QListWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QTreeWidgetItem, QTableWidgetItem

from .exception_handler import global_exception_hander
from .fileutil import check_and_create_dir, get_file_realpath
from .kdJavaLogViewer_ui import Ui_MainWindow


class kdJavaLogViewer(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.exception_handler = global_exception_hander()
        self.exception_handler.patch_excepthook()

        self.last_dir = None
        check_and_create_dir(
            join(expanduser("~"), ".config/kdCarCheckDevSimulator"))
        if not exists(join(expanduser("~"), ".config/kdCarCheckDevSimulator/kdCarCheckDevSimulator.db")):
            copy2(get_file_realpath("../data/kdCarCheckDevSimulator.db"),
                  join(expanduser("~"), ".config/kdCarCheckDevSimulator/kdCarCheckDevSimulator.db"))
   
    #             获取上一次打开的目录
    def get_last_dir(self):
        if self.last_dir:
            return self.last_dir
        else:
            return expanduser("~")

    @pyqtSlot()
    def on_action_start_all_port_triggered(self):
        print("g")


def main():
    app = QApplication(sys.argv)
    win = kdJavaLogViewer()
    win.show()
    sys.exit(app.exec_())
