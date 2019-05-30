'''
Created on 2019年4月8日

@author: bkd
'''
import sys
from tkinter import messagebox
from traceback import format_exception


class global_exception_hander:

    def new_except_hook(self, etype, evalue, tb):
        print(''.join(format_exception(etype, evalue, tb)))
        messagebox.showerror("系统异常", ''.join(format_exception(etype, evalue, tb)))
    
#     注册全局异常处理类
    def patch_excepthook(self):
        sys.excepthook = self.new_except_hook
