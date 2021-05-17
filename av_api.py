import sqlite3
import requests
import pandas as pd

class Company:
    def __init__(self, ticker: str, key: str, database: str, outputsize='compact'):
        self.ticker=ticker
        self.key=key
        self.database=database
        self.outputsize=outputsize

    @property
    def data(self):
        """
        Company's json data
        """
        url='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize={}&apikey={}'.format(self.ticker, self.outputsize, self.key)
        response=requests.get(url)
        if response.status_code!=200:
            raise ValueError("A problem occurs when trying to download data. Status error code: {:d}. Make sure this ticker exists.".format(response.status_code))
        else:
            pass
        data=response.json()
        return data

    def time_series_daily(self, periods_to_update ='all'):
        """
        This property is use to fill the company's table. If 'all' is selected, the API gives the whole data, according to selected outputsize. For a specific number of days, use an integer (example: periods_to_update=5 updates only the last 5 days of data). If you are building the table for the first time, use 'all' option. 
        """
        data=self.data
        lista_tuples = [(self.ticker, date,data['Time Series (Daily)'][date]['4. close']) for date in data['Time Series (Daily)'].keys()]
        if periods_to_update=='all':
            return lista_tuples
        elif isinstance(periods_to_update, int):
            return lista_tuples[:-periods_to_update]
        else:
            raise ValueError("Please, use 'all' or an integer in periods_to_update argument")

    def create_table(self):
        """
        Create company table
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE {} (
            ticker text,
            date text,
            close real
        )
        """.format(self.ticker.split('.')[0].lower()))
        connection.commit()
        connection.close()

    def update_table(self, periods_to_update='all'):
        """
        Update company table
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.executemany("""
        INSERT INTO {}
        VALUES (?,?,?)
        """.format(self.ticker.split('.')[0].lower()), self.time_series_daily(periods_to_update))
        connection.commit()
        connection.close()

class Database:
    def __init__(self, file: str):
        self.file=file

    def list_tables(self):
        """
        List Database tables
        """
        connection = sqlite3.connect(self.file)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print([k[0] for k in cursor.fetchall()])
        connection.close()

    def drop_table(self, table_name: str):
        """
        Drop specific table
        """
        connection = sqlite3.connect(self.file)
        cursor = connection.cursor()
        cursor.execute("DROP TABLE {}".format(table_name))
        connection.commit()
        connection.close()

    # def drop_record(self, table_name: str, rows: list):
    #     """
    #     Drop a list of rows by id
    #     """
    #     connection = sqlite3.connect(self.file)
    #     cursor = connection.cursor()
    #     cursor.execute("DELETE FROM {} WHERE rowid IN ".format(table_name))
    #     connection.commit()
    #     connection.close()

    def to_dataframe(self, table_name: str):
        """
        Returns a pandas DataFrame
        """
        connection = sqlite3.connect(self.file)
        df = pd.read_sql_query("SELECT * FROM {}".format(table_name), connection)
        connection.close()
        df.set_index('date', inplace=True)
        return df

    # def drop_database(self):
        

