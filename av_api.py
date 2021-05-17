import sqlite3
import requests
import pandas as pd

class Company:
    """
    This class create and update data from a selected company
    """
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
    @property
    def time_series_daily(self):
        """
        This property is use to fill the company's table. 
        """
        data=self.data
        lista_tuples = [(self.ticker, date,data['Time Series (Daily)'][date]['4. close']) for date in data['Time Series (Daily)'].keys()]
        return lista_tuples

    def create_table(self):
        """
        Create company table
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE {} (
            ticker text,
            date text PRIMARY KEY,
            close real
        )
        """.format(self.ticker.split('.')[0].lower()))
        connection.commit()
        connection.close()

    def update_table(self, only_days=None, full=True):
        """
        Update company table. 
        """
        if full:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()
            cursor.executemany("""
            INSERT INTO {}
            VALUES (?,?,?)
            """.format(self.ticker.split('.')[0].lower()), self.time_series_daily)
            connection.commit()
            connection.close()
        else:
            if isinstance(only_days, int):
                connection = sqlite3.connect(self.database)
                cursor = connection.cursor()
                cursor.executemany("""
                INSERT OR REPLACE INTO {}
                VALUES (?,?,?)
                """.format(self.ticker.split('.')[0].lower()), self.time_series_daily[:only_days])
                connection.commit()
                connection.close()
            else:
                raise ValueError("If full is mark as False, the integer 'only_days' must be specified.")

class Database:
    """
    This class allow the user to manipulate the saved databases
    """
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

    def to_dataframe(self, table_name: str):
        """
        Returns a pandas DataFrame
        """
        connection = sqlite3.connect(self.file)
        df = pd.read_sql_query("SELECT * FROM {}".format(table_name), connection)
        connection.close()
        df.set_index('date', inplace=True)
        return df        

