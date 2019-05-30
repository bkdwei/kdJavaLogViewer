'''
Created on 2019年5月21日

@author: bkd
'''
from os.path import join, expanduser
import sqlite3


class log():
    
    def __init__(self):
        super().__init__()
        self.db_file = join(expanduser("~"), ".config/kdJavaLogViewer/data.db")
        self.id = None
        self.log_list = []
        self.log_list_size = 0
    
    def add_log(self, time, thread_id, level, clazz, msg):
        if self.log_list_size <= 5000 :
            item = {}
            item["time"] = time
            item["thread_id"] = thread_id
            item["level"] = level
            item["clazz"] = clazz
            item["msg"] = msg
            self.log_list_size += 1
            self.log_list.append(item)
        else :
            conn = sqlite3.connect(self.db_file)
            cs = conn.cursor()
            for l in self.log_list:
                cs.execute("insert into log (time,thread_id,level,clazz,msg) values(?,?,?,?,?)", (l["time"], l["thread_id"], l["level"], l["clazz"], l["msg"]))
            conn.commit()
            self.log_list.clear()
            self.log_list_size = 0
            print("a")
        
    def flush_insert(self):
        self.log_list_size = 5001
        self.add_log(None, None, None, None, None)

    def delete_cmd(self, cmdId):
        self.run_sql("delete from cmd where id = '{}'".format(cmdId))

    def get_all(self, model):
        return self.run_sql("select id,model,value,remark,reply_type from cmd where model ='{}' order by remark".format(model))

    def modify_cmd(self):
        reply_type = 1
        if self.rb_random.isChecked():
            reply_type = 2
        self.run_sql("update cmd set  value ='{}', remark='{}', reply_type ='{}' where id='{}'".format(self.le_value.text(), self.le_remark.text(), reply_type, self.id))
    
    def run_sql(self, sql):    
        conn = sqlite3.connect(self.db_file)
        cs = conn.cursor()
        print("execute sql:" + sql)
        cs.execute(sql)
        if "select" in sql:
            return cs.fetchall()  
        conn.commit()
