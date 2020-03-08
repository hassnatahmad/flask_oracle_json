import platform
import os
import db_config as cfg

cfg.set_oracle_instant_client_location()  # we set location of oracle instant client
import cx_Oracle


# Connect as user "flaskuser" with password "xxxx" to the "flaskuser" service running on this computer.


def get_all_rows(table_name):
    sql_statement = 'select * from ' + table_name
    try:
        # establish a new connection
        with cx_Oracle.connect(cfg.username,
                               cfg.password,
                               cfg.dsn,
                               encoding=cfg.encoding) as connection:
            # create a cursor
            with connection.cursor() as cursor:
                # execute the insert statement
                cursor.execute(sql_statement)
                res = cursor.fetchall()
                print(table_name + ':Data ')
                print(res)
                # cursor.close()
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)


def get_cols(cols, allowed_col_length):
    col_length = len(cols)
    col_string = '(' + put_double_quote_if_space_between_col_name(str(cols[0]))
    for i in range(1, col_length):
        if i >= allowed_col_length:
            continue
        col_string += ',' + put_double_quote_if_space_between_col_name(str(cols[i]))
    return col_string + ')'


def read_all_rows_and_save(table_name, cols, rows):
    allowed_col_length = cfg.get_table_total_cols(table_name)
    col_string = get_cols(cols, allowed_col_length)
    row_string = ''
    for i in range(0, len(rows)):
        actual_row_cols = len(rows[i])
        row_string += 'INSERT INTO ' + table_name + ' ' + col_string + ' VALUES('
        row_string += "'" + str(rows[i][0]) + "'"
        for j in range(1, actual_row_cols):
            if j >= allowed_col_length:
                sql_string = ''
                sql_string += prepare_extra_column_sql(table_name, str(rows[i][0]), str(cols[j]), str(rows[i][j]))
                #print(sql_string)
                save_each_row(sql_string) # save extra columns in extra table
                continue
            row_string += ",'" + str(rows[i][j]) + "'"
        row_string += ')'
        #print(row_string)
        save_each_row(row_string) # save normal columns
        row_string = ''

    # return row_string


def prepare_extra_column_sql(table_name, primary_key_value, col_name, col_value):
    primary_key = cfg.get_table_primary_key(table_name)
    sql_string = ''
    sql_string += 'insert into ' + table_name + '_EXTRA '
    sql_string += '("{0}","Column name","Column value") '.format(primary_key)
    sql_string += "values ('{0}','{1}','{2}')".format(primary_key_value, col_name, col_value)
    return sql_string


def save_each_row(sql_statement):
    print('executing: ', sql_statement)
    try:
        # establish a new connection
        with cx_Oracle.connect(cfg.username,
                               cfg.password,
                               cfg.dsn,
                               encoding=cfg.encoding) as connection:
            # create a cursor
            with connection.cursor() as cursor:
                # execute the insert statement
                cursor.execute(sql_statement)
                # commit work
                connection.commit()
                print('done writing to table')
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)


def delete_all_rows(table_name):
    sql_statement = 'Truncate Table ' + table_name
    try:
        # establish a new connection
        with cx_Oracle.connect(cfg.username,
                               cfg.password,
                               cfg.dsn,
                               encoding=cfg.encoding) as connection:
            # create a cursor
            with connection.cursor() as cursor:
                # execute the insert statement
                cursor.execute(sql_statement)
                print('delete completed:' + table_name)
    except cx_Oracle.Error as error:
        print('Error occurred while deleting:' + table_name)
        print(error)


def delete_table(table_name):
    sql_statement = 'DROP TABLE "' + table_name + '" CASCADE CONSTRAINTS'
    try:
        # establish a new connection
        with cx_Oracle.connect(cfg.username,
                               cfg.password,
                               cfg.dsn,
                               encoding=cfg.encoding) as connection:
            # create a cursor
            with connection.cursor() as cursor:
                # execute the insert statement
                cursor.execute(sql_statement)
                print('delete table:' + table_name)
    except cx_Oracle.Error as error:
        print('Error occurred while deleting:' + table_name)
        print(error)


def delete_all_tables():
    delete_table('C_LOADING_CONDITIONS_EXTRA')
    delete_table('B_TESTS_EXTRA')
    delete_table('A_GEOMETRIES_EXTRA')
    delete_table('C_LOADING_CONDITIONS_TEST_SUBTYPES')
    delete_table('C_LOADING_CONDITIONS')
    delete_table('B_TESTS')
    delete_table('A_GEOMETRIES')


def delete_all_tables_data():
    delete_all_rows('C_LOADING_CONDITIONS_EXTRA')
    delete_all_rows('B_TESTS_EXTRA')
    delete_all_rows('A_GEOMETRIES_EXTRA')
    delete_all_rows('C_LOADING_CONDITIONS_TEST_SUBTYPES')
    delete_all_rows('C_LOADING_CONDITIONS')
    delete_all_rows('B_TESTS')
    delete_all_rows('A_GEOMETRIES')


def put_double_quote_if_space_between_col_name(col_name):
    return '"' + col_name + '"'
