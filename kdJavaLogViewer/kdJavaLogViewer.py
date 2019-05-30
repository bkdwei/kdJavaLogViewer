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
import sys, time

from PyQt5.Qt import QListWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit, QTreeWidgetItem, QTableWidgetItem

from .exception_handler import global_exception_hander
from .fileutil import check_and_create_dir, get_file_realpath, check_and_create_sqlite_file
from .kdJavaLogViewer_ui import Ui_MainWindow
from .log import log


class kdJavaLogViewer(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.exception_handler = global_exception_hander()
        self.exception_handler.patch_excepthook()

        self.last_dir = None
        check_and_create_sqlite_file(join(expanduser("~"), ".config/kdJavaLogViewer/data.db"))
        self.log = log()
   
    #             获取上一次打开的目录
    def get_last_dir(self):
        if self.last_dir:
            return self.last_dir
        else:
            return expanduser("~")

    @pyqtSlot()
    def on_action_start_all_port_triggered(self):
        print("g")

    @pyqtSlot()
    def on_pb_import_clicked(self):
        selected_file, _ = QFileDialog.getOpenFileName(self, '选择命令路径', self.get_last_dir(), '*.log', '')
        if selected_file:
            self.statusbar.showMessage("")
            begin_time = time.time()
#             print(now)
            i = 1 
            with open(selected_file, "r", encoding="UTF-8") as f:
                log_time = None
                thread_id = None
                level = None
                clazz = None
                msg = None
                for l in f: 
#                     print(i, fLine)
                    if(l[0] != '2'):
                        msg += l
                        continue
                    else :
#                         print(log_time, thread_id, level, clazz, msg)
                        if log_time:
                            self.log.add_log(log_time, thread_id, level, clazz, msg)
                        log_time = l[0:23]
                        thread_id = l[24:29]
                        level = l[29:34]
                        ll = str(l[35:]).split(']')
                        clazz = ll[0][1:]
                        msg = ll[1][2:]
#                         print(l[0:23], l[24:29], l[29:34], ll[0][1:], ll[1][2:])
#                     print(ll[0], ll[1])
                    i += 1 
                if log_time:
                    self.log.add_log(log_time, thread_id, level, clazz, msg)
                self.log.flush_insert()
#                 print(log_time, thread_id, level, clazz, msg)
            end_time = time.time()
            self.statusbar.showMessage("耗时" + str(end_time - begin_time) + "秒，行数:" + str(i))


def main():
    app = QApplication(sys.argv)
    win = kdJavaLogViewer()
    win.show()
    sys.exit(app.exec_())
