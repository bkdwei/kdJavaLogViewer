'''
Created on 2019年5月20日

@author: bkd
'''
'''
Created on 2019年5月9日

@author: bkd
'''

from os import environ
from os.path import expanduser, join
import sys, time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog

from .exception_handler import global_exception_hander
from .fileutil import  check_and_create_sqlite_file
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
            return join(environ["CATALINA_HOME"], "logs")

    @pyqtSlot()
    def on_action_start_all_port_triggered(self):
        print("g")

    @pyqtSlot()
    def on_pb_query_clicked(self):
        self.statusbar.showMessage("")
        thread_id = self.le_prefex.text().strip() + self.le_thread.text().strip()
        if thread_id == "T":
            thread_id = None
        keyword = self.le_keyword.text().strip()
        short_clazz = self.le_method.text().strip()
        start_time = self.te_start.time().toString()
        end_time = self.te_end.time().toString()
        level_list = []
        if self.cb_debug.isChecked():
            level_list.append("DEBUG")
        if self.cb_info.isChecked():
            level_list.append("INFO")
        if self.cb_warn.isChecked():
            level_list.append("WARN")
        if self.cb_error.isChecked():
            level_list.append("ERROR")
        if any([thread_id != "" , keyword != ""]):
            log_list = self.log.query(thread_id, keyword, short_clazz, start_time, end_time, level_list)
            if not log_list :
                self.statusbar.showMessage("查询结果为空")
                return
            self.log_list = log_list
            msg = ""
            for item in log_list :
                msg = msg + item[0] + " " + item[1] + " " + item[2] + " [" + item[3] + "] " + item[4]
            self.tb_result.clear()
            self.tb_result.setText(msg)

    @pyqtSlot()
    def on_pb_open_clicked(self):
        hour , ok = QInputDialog.getInt(self, "导入指定小时之后的日志", "点击取消将导入全部日志。", 0, 0, 24, 1)
        selected_file, _ = QFileDialog.getOpenFileName(self, '选择日志文件路径', self.get_last_dir(), '*.log', '')
        if selected_file:
            self.log.delete_all()
            self.statusbar.showMessage("")
            begin_time = time.time()
            i = 1 
            encoding = self.le_encoding.text().strip()
            f = None
            if encoding == "" :
                f = open(selected_file, "r")
            else :
                f = open(selected_file, "r", encoding=encoding)
                
#             with open(selected_file, "r", encoding=self.le_encoding.text().strip()) as f:
            log_time = None
            thread_id = None
            level = None
            clazz = None
            short_clazz = None
            msg = None
            l = f.readline()
            while l: 
#                     不以时间开头的行，默认不是一行
                if(l[0] != '2'):
                    msg += l
                    i += 1 
                    l = f.readline()
                    continue
                # 跳过指定时间之前的日志
                elif int(l[11:13]) < hour and ok:
#                     print(int(l[11:13]))
                    l = f.readline()
                    continue
                else :
#                         print(log_time, thread_id, level, clazz, msg)
                    if log_time:
                        self.log.add_log(log_time, thread_id, level, clazz, msg, short_clazz)
                    log_time = l[11:23]
                    thread_id = l[24:28]
                    level = l[29:35]
                    ll = str(l[35:]).split(']')
                    clazz = ll[0][2:]
                    short_clazz = clazz.split(".")[-1]
                    msg = ll[1][2:]
                    l = f.readline()
                i += 1 
            if log_time:
                self.log.add_log(log_time, thread_id, level, clazz, msg, short_clazz)
            self.log.flush_insert()
            end_time = time.time()
            self.tb_result.setText("导入日志成功，耗时" + str(end_time - begin_time) + "秒，行数:" + str(i))
            f.close()


def main():
    app = QApplication(sys.argv)
    win = kdJavaLogViewer()
    win.show()
    sys.exit(app.exec_())
