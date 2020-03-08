import os

# default values
username = 'flaskuser'
password = 'flaskuser'
dsn = 'localhost'
port = 1521
encoding = 'UTF-8'
# here fix the length of columns from json
a_geometries_column = 46
b_tests_column = 10
c_loading_conditions_column = 30


def get_table_total_cols(table_name):
    if table_name == 'A_GEOMETRIES':
        return a_geometries_column
    elif table_name == 'B_TESTS':
        return b_tests_column
    elif table_name == 'C_LOADING_CONDITIONS':
        return c_loading_conditions_column


def get_table_primary_key(table_name):
    if table_name == 'A_GEOMETRIES':
        return 'CRD'
    elif table_name == 'B_TESTS':
        return 'Test ID'
    elif table_name == 'C_LOADING_CONDITIONS':
        return 'Test-load-pressure ID'


def get_connection_string():
    return "%s/%s@%s" % (username, password, dsn)  # connection format username/password@oracleServer


# on windows there was problem of oracle instant client so we set up manually path
def set_oracle_instant_client_location():
    LOCATION = r"C:\app\instantclient_19_5"
    # print("ARCH:", platform.architecture())
    # print("FILES AT LOCATION:")
    # for name in os.listdir(LOCATION):
    # print(name)
    os.environ["PATH"] = LOCATION
