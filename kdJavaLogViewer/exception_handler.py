'''
Created on 2019年4月8日

@author: bkd
'''
import sys
from tkinter import Tk, Label
from traceback import format_exception


class global_exception_hander:

    def new_except_hook(self, etype, evalue, tb):
        err_msg = ''.join(format_exception(etype, evalue, tb))
        print(err_msg)
        win = Tk(className="系统异常")
        Label(win, text=err_msg).pack()
        win.mainloop()
    
#     注册全局异常处理类
    def patch_excepthook(self):
        sys.excepthook = self.new_except_hook
