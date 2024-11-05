from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Define the global database engine (connection object)
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
CONN_STR = f'mysql+pymysql://{USER}:{PASSWORD}@localhost/tacto'
ENGINE = create_engine(CONN_STR, future=True)


def reset_database(database_name):
    session = sessionmaker(bind=ENGINE)()  # Create a new session
    # Use string formatting to include the database name directly in the SQL query
    session.execute(text(f"DROP DATABASE IF EXISTS {database_name}"))
    session.commit()  # Commit the transaction to apply the change

    session.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))
    session.commit()  # Commit the transaction to apply the change

    # Close the session
    session.close()
    ENGINE.dispose()  # Dispose of the engine to prevent connection issues


def fetch_query_as_dataframe(sql_file_path):
    """
    Executes a query from a SQL file and returns the result as a DataFrame.
    
    Parameters:
    - sql_file_path (str): The path to the .sql file containing the query.

    Returns:
    - pd.DataFrame: DataFrame containing the query results.
    """
    with open(sql_file_path, 'r') as file:
        query = file.read()
    
    # Execute the query and load the result into a DataFrame
    with ENGINE.connect() as connection:
        result = connection.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    return df