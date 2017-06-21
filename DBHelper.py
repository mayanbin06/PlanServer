#!/usr/bin/env python
# -*-coding:UTF-8-*-
import sys,MySQLdb,traceback
import time
class mysql:
    def __init__ (self,
                  host   = '',
                  user   = '',
                  passwd = '',
                  db     = '',
                  port   = 3306,
                  charset= 'utf8'
                  ):
        self.host   = host
        self.user   = user
        self.passwd = passwd
        self.db     = db
        self.port   = port
        self.charset= charset
        self.conn   = None
        self._conn()

    def _conn (self):
        try:
            self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)
            self.conn.select_db('pk10')
            self.conn.set_character_set('utf8')
            return True
        except Exception, e:
            print e
            return False

    def _reConn (self,num = 28800,stime = 3):
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()
                _status = False
            except Exception, e:
                if self._conn()==True:
                    _status = False
                    break
                _number +=1
                time.sleep(stime)
                print e

    def select(self, sql = ''):
        try:
            self._reConn()
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.cursor.close()
            self.conn.commit()
            return result
        except MySQLdb.Error,e:
            #print "Error %d: %s" % (e.args[0], e.args[1])
            return False

    def close(self):
        self.conn.close()

if __name__=='__main__':
    my = mysql('localhost','dabao','a123456','pk10',3306)
