from sqlalchemy import create_engine, text
import pandas as pd
import os
from datetime import datetime

username = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
database = os.getenv('POSTGRES_DB')
host = 'postgres-db'
#host = 'localhost'
port = '5432'  # default PostgreSQL port is 5432

# Create the database engine
try:
    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
    print('Connection to database succeeded')
except:
    print('Connection to database failed')

def inject_sql(df):
    now = datetime.now()
    df['created_at'] = df['updated_at'] = now
    df.to_sql('ads', engine, if_exists='append', index=False)

def add_columns_to_table(df, table_name):

    # Get the list of columns in the DataFrame
    df_columns = df.columns.tolist()

    # Query the database for table schema
    query = """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'ads' AND table_schema = 'public'
    """

    existing_columns_df = pd.read_sql(query, engine)
    existing_columns = existing_columns_df['column_name'].tolist()

    # Find missing columns in the database table
    missing_columns = set(df_columns) - set(existing_columns)

    print(missing_columns)

    # Function to map pandas dtype to SQL type
    def map_dtype_to_sql(dtype):
        if "int" in dtype:
            return "INTEGER"
        elif "float" in dtype:
            return "FLOAT"
        elif "datetime" in dtype:
            return "TIMESTAMP"
        else:
            return "TEXT"

    # Alter table to add missing columns
    with engine.connect() as conn:
        for column in missing_columns:
            dtype = df[column].dtype.name
            sql_type = map_dtype_to_sql(dtype)
            alter_query = f"ALTER TABLE ads ADD COLUMN {column} {sql_type};"
            print(alter_query)
            #conn.execute(text(alter_query))

def check_table(table_name):         
    print(engine.url)
    query = f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = {table_name} AND table_schema = 'public'
    """
    existing_columns_df = pd.read_sql(query, engine)
    print(existing_columns_df)

    print(pd.read_sql(f'SELECT * FROM {table_name} LIMIT 5', engine))

#add_columns_to_table(df, "ads")
#inject_sql()

def add_scraped_data_to_postgresDB(dept, date):
    """ Adds scraped data of the day to POSTGRESQL database
    """
    
    cwd = os.getcwd()

    files = [f for f in os.listdir(os.path.join(cwd, 'files')) if (f.endswith('.csv')) & (f[-34:-24] == date) & (f.split("_")[1] == str(dept))]
    print(files)

    df = pd.DataFrame()
    for file in files:
        df_add = pd.read_csv(f'files/{file}', sep = ";", index_col = 0)
        df = pd.concat([df, df_add])

    df['date_scraped'] = date

    try:
        inject_sql(df)
        print('Injection succeeded')
    except:
        print('Injection failed')
        raise Exception()

