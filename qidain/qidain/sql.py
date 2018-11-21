import pymysql


class Sql(object):
    def __init__(self, host='localhost', user='root', pwd='819555147', dbname='spider'):
        if host is None or user is None or pwd is None or dbname is None:
            raise ValueError('Error in parameter')
        try:
            self.db_connect = pymysql.connect(host, user, pwd, dbname)
            self.cursor = self.db_connect.cursor()
        except Exception as e:
            print('Error happened when connect db:', str(e))

    def execute_select_sql(self, query):
        try:
            self.cursor.execute(query)
        except Exception as e:
            print('Error happened when execute select sql query:', str(e))

    def execute_other_sql(self, query):
        try:
            self.cursor.execute(query)
            self.db_connect.commit()
        except Exception as e:
            print('Error happened when execute update or insert or delete sql:', str(e))
            self.db_connect.rollback()

    def __del__(self):
        self.db_connect.close()
