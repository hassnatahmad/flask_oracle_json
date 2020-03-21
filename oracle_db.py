import db_config as config

# config.set_oracle_instant_client_location()  # we set location of oracle instant client
import cx_Oracle


def get_all_rows(table_name):
    sql_statement = 'select * from ' + table_name
    try:
        # establish a new connection
        with cx_Oracle.connect(config.username,
                               config.password,
                               config.dsn,
                               encoding=config.encoding) as connection:
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


def get_cols(cols, table_name):
    primary_key = config.get_table_primary_key(table_name)
    col_length = len(cols)
    col_string = '(' + put_double_quote_if_space_between_col_name_and_length_30(primary_key)
    for i in range(0, col_length):
        col_string += ',' + put_double_quote_if_space_between_col_name_and_length_30(str(cols[i]))
    return col_string + ')'


def get_extra_cols(cols, allowed_col_length, table_name):
    primary_key = config.get_table_primary_key(table_name)
    col_list = []
    col_length = len(cols)
    col_string = '(' + put_double_quote_if_space_between_col_name_and_length_30(primary_key)
    for i in range(0, col_length):
        if i >= allowed_col_length:
            col_list.append(truncate_30_chars(str(cols[i])))
            continue
        col_string += ',' + put_double_quote_if_space_between_col_name_and_length_30(str(cols[i]))
    return col_string + ')', col_list


def read_all_rows_and_save_extra(table_name, cols, rows, allowed_col_length):
    col_string, col_list = get_extra_cols(cols, allowed_col_length, table_name)
    dict_data = dict()
    dict_data_link_back = dict()
    # col_string = get_cols(cols, table_name)
    link_key = ''
    if table_name == 'A_GEOMETRIES' or table_name == 'B_TESTS':
        link_key += config.get_table_link_back_key('A_GEOMETRIES')
    else:
        link_key += config.get_table_link_back_key('B_TESTS')
    link_back_key_index = cols.index(link_key)
    row_string = ''
    extra_row_string = []
    current_index = 0
    for i in range(0, len(rows)):
        actual_row_cols = len(rows[i])
        uid = config.generate_uuid()
        first_value = str(rows[i][0])
        link_back_value = str(rows[i][link_back_key_index])
        dict_data.update({uid: first_value})
        dict_data_link_back.update({uid: link_back_value})
        row_string += 'INSERT INTO ' + table_name + ' ' + col_string + ' VALUES('
        row_string += "'" + uid + "'"
        row_string += ",'" + first_value + "'"
        for j in range(1, actual_row_cols):
            if j >= allowed_col_length:
                extra_row_string.append(
                    prepare_extra_column_sql(table_name, uid, str(cols[j]), str(rows[i][j])))
                continue
            row_string += ",'" + str(rows[i][j]) + "'"
        row_string += ')'
        save_each_row(row_string, table_name)  # save normal columns
        row_string = ''
        # iterate through al extra col
        for sql_stmnt in extra_row_string:
            save_each_row(sql_stmnt, table_name + '_EXTRA')

        return dict_data, dict_data_link_back


def read_all_rows_and_save(table_name, cols, rows):
    allowed_col_length = config.get_table_total_cols(table_name)
    dict_data = dict()
    dict_data_link_back = dict()
    if len(cols) > allowed_col_length:
        return read_all_rows_and_save_extra(table_name, cols, rows, allowed_col_length)
    else:
        col_string = get_cols(cols, table_name)
        link_key = ''
        if table_name == 'A_GEOMETRIES' or table_name == 'B_TESTS':
            link_key += config.get_table_link_back_key('A_GEOMETRIES')
        else:
            link_key += config.get_table_link_back_key('B_TESTS')
        link_back_key_index = cols.index(link_key)
        row_string = ''
        for i in range(0, len(rows)):
            actual_row_cols = len(rows[i])
            uid = config.generate_uuid()
            first_value = str(rows[i][0])
            link_back_value = str(rows[i][link_back_key_index])
            dict_data.update({uid: first_value})
            dict_data_link_back.update({uid: link_back_value})
            row_string += 'INSERT INTO ' + table_name + ' ' + col_string + ' VALUES('
            row_string += "'" + uid + "'"
            row_string += ",'" + first_value + "'"
            for j in range(1, actual_row_cols):
                row_string += ",'" + str(rows[i][j]) + "'"
            row_string += ')'
            save_each_row(row_string, table_name)  # save normal columns
            row_string = ''

    return dict_data, dict_data_link_back


def prepare_extra_column_sql(table_name, primary_key_value, col_name, col_value):
    primary_link_key_value = config.generate_uuid()
    primary_key = config.get_table_primary_key(table_name)
    primary_key_extra = config.get_table_primary_key(table_name + '_EXTRA')
    sql_string = ''
    sql_string += 'insert into ' + table_name + '_EXTRA '
    sql_string += '("{0}","{1}","Column name","Column value") '.format(primary_key_extra, primary_key)
    sql_string += "values ('{0}','{1}','{2}','{3}')".format(primary_link_key_value, primary_key_value, col_name,
                                                            col_value)
    return sql_string


def save_a_b_table(table_name, a_dict, b_dict, b_link_dict):
    primary_key = config.get_table_primary_key(table_name)

    for key, value in b_link_dict.items():
        try:
            primary_key_value = config.generate_uuid()
            link_key, b_crd = config.get_key_by_value(a_dict, value)
            sql_string = 'insert into ' + table_name + ' ("{0}","B_TESTS_ID","A_GEOMETRIES_ID") values ('.format(
                primary_key)
            sql_string += "'{0}','{1}','{2}')".format(primary_key_value, key, link_key)
            save_each_row(sql_string, table_name)
        except TypeError:
            print('seems no values', TypeError)


def save_b_c_table(table_name, b_dict, c_dict, c_link_dict):
    primary_key = config.get_table_primary_key(table_name)

    for key, value in c_link_dict.items():
        primary_key_value = config.generate_uuid()
        try:
            link_key, b_crd = config.get_key_by_value(b_dict, value)
            sql_string = 'insert into ' + table_name + ' ("{0}","B_TESTS_ID","C_LOADING_ID") values ('.format(
                primary_key)
            sql_string += "'{0}','{1}','{2}')".format(primary_key_value, link_key, key)
            save_each_row(sql_string, table_name)
        except TypeError:
            print('seems no values', TypeError)


def save_each_row(sql_statement, table_name):
    # print('done writing {0} to table'.format(table_name))
    print('executing: ', sql_statement)
    try:
        # establish a new connection
        with cx_Oracle.connect(config.username,
                               config.password,
                               config.dsn,
                               encoding=config.encoding) as connection:
            # create a cursor
            with connection.cursor() as cursor:
                # execute the insert statement
                cursor.execute(sql_statement)

                # commit work
                connection.commit()
                print('done writing {0} to table'.format(table_name))
    except cx_Oracle.Error as error:
        print('{0} Error occurred: {1}'.format(table_name, error))
    finally:
        if not connection.close:
            cursor.close()
            connection.close()
            print("Oracle connection is closed")


def delete_all_rows(table_name):
    sql_statement = 'Truncate Table ' + table_name
    try:
        # establish a new connection
        with cx_Oracle.connect(config.username,
                               config.password,
                               config.dsn,
                               encoding=config.encoding) as connection:
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
        with cx_Oracle.connect(config.username,
                               config.password,
                               config.dsn,
                               encoding=config.encoding) as connection:
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


def put_double_quote_if_space_between_col_name_and_length_30(col_name):
    str = col_name
    if len(col_name) > 30:
        return '"' + truncate_30_chars(str) + '"'
    return '"' + col_name + '"'


def truncate_30_chars(str):
    return str[:30]
