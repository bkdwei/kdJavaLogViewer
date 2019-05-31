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
    
    def add_log(self, time, thread_id, level, clazz, msg, short_clazz):
        if self.log_list_size <= 5000 :
            item = {}
            item["time"] = time
            item["thread_id"] = thread_id.strip()
            item["level"] = level.strip()
            item["clazz"] = clazz
            item["short_clazz"] = short_clazz
            item["msg"] = msg
            self.log_list_size += 1
            self.log_list.append(item)
        else :
            conn = sqlite3.connect(self.db_file)
            cs = conn.cursor()
            for l in self.log_list:
                cs.execute("insert into log (time,thread_id,level,clazz,msg,short_clazz) values(?,?,?,?,?,?)", (l["time"], l["thread_id"], l["level"], l["clazz"], l["msg"], l["short_clazz"]))
            conn.commit()
            self.log_list.clear()
            self.log_list_size = 0
            print("a")
        
    def flush_insert(self):
        self.log_list_size = 5001
        self.add_log(None, None, None, None, None, None)

    def delete_all(self):
        self.run_sql("delete from log ")

    def query(self, thread_id, keyword, short_clazz, start_time , end_time, level_list):
        sql = "select time,thread_id,level,clazz,msg from log where 1= 1 "
        if thread_id :
            sql += "and thread_id ='{}' ".format(thread_id)
        if keyword :
            sql += "and msg like '%{}%' ".format(keyword)
        if short_clazz:
            sql += "and short_clazz = '{}' ".format(short_clazz)
        if start_time and start_time != "00:00:00" :
            sql += "and time >= '{}' ".format(start_time)
        if end_time and start_time != "00:00:00"  and start_time < end_time:
            sql += "and time <= '{}' ".format(end_time)
        if len(level_list) > 0:
            for l in level_list:
                level = "'" + l + "',"
                
            print(level[:-1])
            sql += "and level in ({}) ".format(level[:-1])
            
        return self.run_sql(sql)

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
