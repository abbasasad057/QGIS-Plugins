import psycopg2


class DbConfig:
    def __init__(self, db_ip, db_name, db_port, db_username, db_password):
        self.db_ip = db_ip
        self.db_name = db_name
        self.db_port = db_port
        self.db_username = db_username
        self.db_password = db_password

    def ConnectDb(self):  # self,db_ip,db_name, db_port, db_username, db_password):

        try:
            self.conn = psycopg2.connect(
                "dbname='" + self.db_name + "' user='" + self.db_username + "' host='" + self.db_ip + "' password='" + self.db_password + "' port=" + str(
                    self.db_port) + ")")
            return True
        except:
            return False

    def DbResultsQuery(self, query, vire = None):
        cursor = self.conn.cursor()
        cursor.execute(query, vire)
        res = cursor.fetchall()
        cursor.close()
        return res

    def DbModifyQuery(self,query, vire = None):
        cursor = self.conn.cursor()
        cursor.execute(query, vire)
        cursor.close()
        self.conn.commit()

    def PluginDbQuery(self,query,vire=None):
        cursor = self.conn.cursor()
        cursor.execute(query, vire)
        res = cursor.fetchall()
        cursor.close()
        self.conn.commit()
        return res


    def releaseDbConnection(self):
        self.conn.close()
