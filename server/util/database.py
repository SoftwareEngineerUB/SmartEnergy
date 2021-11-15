import json

import pymysql
from pymysql.constants import CLIENT


class Database:
    def __init__(self):
        with open("settings.json", "r") as f:
            self.general_settings = json.loads(f.read())
            f.close()

        self.database = pymysql.connect(
            host=self.general_settings['database']['host'],
            user=self.general_settings['database']['username'],
            password=self.general_settings['database']['password'],
            client_flag=CLIENT.MULTI_STATEMENTS
        )

        self.cursor = self.database.cursor()
        self.cursor.execute('use ' + self.general_settings['database']['database'])

    def __del__(self):
        self.cursor.close()
        self.database.close()

    def commit(self):
        self.execute("COMMIT;")

    def useDatabase(self, database=None):
        if database is None:
            database = self.general_settings['database']['database']
        self.cursor.execute(f'use {database}')

    def select(self, query, data=None):
        if data is None:
            data = []
        self.cursor.execute(query, data)
        columnNames = [x[0] for x in self.cursor.description]
        results = self.cursor.fetchall()

        answers = list()
        for result in results:
            ans = dict()
            for index, value in enumerate(result):
                ans[columnNames[index]] = value
            answers.append(ans)
        return answers

    def selectOne(self, query, data=None):
        if data is None:
            data = []
        self.cursor.execute(query, data)
        columnNames = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()
        if result is None:
            return None
        ans = dict()
        for index, value in enumerate(result):
            ans[columnNames[index]] = value
        return ans

    def execute(self, query, data=None):
        if data is None:
            data = []
        self.cursor.execute(query, data)
        self.cursor.connection.commit()
        return self.cursor.lastrowid
