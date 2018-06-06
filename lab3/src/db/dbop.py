import pymysql


class mysqlConn():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    user='root',
                                    password='123456',
                                    db='bank',
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cursor = pymysql.cursors.SSCursor(self.conn)

    def execSQL(self, SQL, args=None):
        self.cursor.execute(SQL, args)
        return self.cursor

    def execCommit(self, SQL, args=None):
        self.cursor.execute(SQL, args)
        self.conn.commit()

    def distroy(self):
        self.cursor.close()
        self.conn.close()
