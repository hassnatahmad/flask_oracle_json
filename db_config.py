import os
import crypto as cr
import uuid
import cx_Oracle

username = 'flaskuser'
password = 'flaskuser'
dsn = 'localhost'
# username = 'lda5148'
# password = cr.decrypt(cr.lda5148_gds187)
dsn_tns = cx_Oracle.makedsn('gisvms187.ec.goodyear.com', '1521', service_name='ora')
port = 1521
encoding = 'UTF-8'

# here fix the length of columns from json
a_geometries_column = 46
b_tests_column = 10
c_loading_conditions_column = 30
connection_string = 'oracle://{user}:{password}@{sid}'.format(
    user=username,
    password=password,
    sid=dsn  # dsn_tns
)


def generate_uuid():
    return str(uuid.uuid4())


def get_table_total_cols(table_name):
    if table_name == 'A_GEOMETRIES':
        return a_geometries_column
    elif table_name == 'B_TESTS':
        return b_tests_column
    elif table_name == 'C_LOADING_CONDITIONS':
        return c_loading_conditions_column


def get_table_primary_key(table_name):
    if table_name == 'A_GEOMETRIES':
        return 'A_GEOMETRIES_ID'
    elif table_name == 'B_TESTS':
        return 'B_TESTS_ID'
    elif table_name == 'C_LOADING_CONDITIONS':
        return 'C_LOADING_ID'
    elif table_name == 'A_GEOMETRIES_EXTRA':
        return 'A_GEOMETRIES_EXTRA_ID'
    elif table_name == 'B_TESTS_EXTRA':
        return 'B_TESTS_EXTRA_ID'
    elif table_name == 'C_LOADING_CONDITIONS_EXTRA':
        return 'C_LOADING_EXTRA_ID'
    elif table_name == 'A_B':
        return 'A_B_ID'
    elif table_name == 'B_C':
        return 'B_C_ID'
    elif table_name == 'C_LOADING_SUBTYPES':
        return 'C_LOADING_SUBTYPES_ID'


def get_table_link_back_key(table_name):
    if table_name == 'A_GEOMETRIES':
        return 'CRD'
    elif table_name == 'B_TESTS':
        return 'Test ID'
    elif table_name == 'C_LOADING_CONDITIONS':
        return 'Test-load-pressure ID'


def get_key_by_value(dictOfElements, valueToFind):
    try:
        for key, value in dictOfElements.items():
            if value == valueToFind:
                return key,value
    except KeyError:
        print('seems no values', KeyError)


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
# INSERT INTO C_LOADING_CONDITIONS ("C_LOADING_CONDITIONS_ID","Test-load-pressure ID","Test ID","Pressure (bar)","Vertical load (kg)","SD (mm)","OD (mm)","CL (mm)","Width (mm)","ISL (mm)","OSL (mm)","Net area (mm2)","Gross area (mm2)","FSF","DOF","Vertical spring rate tangent (","Vertical spring rate secant (N","Lateral spring rate (N/mm)","Longitudinal spring rate (N/mm","Torsional spring rate (N/mm)","RRc","RR (kg)","Loss (N-mm/rev)","Temperature (C)","CS","SAS","TD","FP","SR","RR","FM") VALUES('3671ca83-3765-4ea6-a698-e08ee9a46aab','201911140132_0_2.2','201911140132','2.2','0','222.092','678.112','None','None','None','None','None','None','None','None','None','None','None','None','None','None','None','None','None','None','None','yes','no','no','no','no')
