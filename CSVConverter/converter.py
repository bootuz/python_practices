from sqlalchemy import create_engine
import pandas as pd


class CSVConverter:
    
    def __init__(self, data, separator):
        """
        Constructs a csv_to_sql converter.

        -- data: a csv file
        -- separator: defines a way csv file separated
        """
        self.data = data
        self.separator = separator

    def _create_df(self):
        """
        Creates and returns a pandas data frame from csv file
        """
        df = pd.read_csv(self.data, sep=self.separator)
        return df

    def to_mysql(self, table_name, user, password, host, db):
        """
        Converts a data frame created by _create_df() into mysql.

        -- table_name: A name for mysql table
        -- user: user name in mysql server
        -- password: password of mysql server
        -- host: host name
        -- db: database name
        """
        if self.data.endswith('.csv'):
            df = self._create_df()
            mysql_engine = create_engine('mysql://{user}:{pw}@{host}'.format(user=user,
                                                                             pw=password,
                                                                             host=host))

            databases = mysql_engine.execute("SHOW DATABASES;")
            db_list = [d[0] for d in databases]
            if db not in db_list:
                mysql_engine.execute('create database {};'.format(db))

            db_engine = create_engine('mysql://{user}:{pw}@{host}/{db}'.format(user=user,
                                                                               pw=password,
                                                                               host=host,
                                                                               db=db))
            df.to_sql(con=db_engine,
                      index_label='id',
                      name=table_name,
                      if_exists='replace')
            
            print('Done!')

        else:
            raise TypeError("Invalid file format. Must be a .csv file.")

    def to_sqlite(self, db, table_name):
        """
        Converts a data frame into sqlite.

        -- db: Database name for sqlite
        -- table_name: Table name
        """
        df = self._create_df()
        engine = create_engine('sqlite:///' + db + '.db')
        df.to_sql(table_name, engine, if_exists='replace')

    def to_postgress(self):
        pass


if __name__ == "__main__":
    x = CSVConverter(data='student-por.csv', separator=';')
    x.to_mysql(table_name='students', user='root', password='', host='localhost', db='test')
    x.to_sqlite(db='stud', table_name='students')
