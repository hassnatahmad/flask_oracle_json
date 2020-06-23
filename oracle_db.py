import os
import db_config as config
from exceptions import UploadProcessException
from fastnumbers import fast_real

# config.set_oracle_instant_client_location()  # we set location of oracle instant client
import cx_Oracle


def get_connection():
    return cx_Oracle.connect(config.username, config.password, config.dsn, encoding=config.encoding)


def convert_number_or_into_string(str_input, col):
    """Optimizes the Data Types. If VARCHAR type is defined in SQL for any value, it saves the similar value by adding quotation marks.
    However, if not, then by default it's a Number. In the later case, if the value is NULL, convert it to 0 else save the number."""

    if (col == "CRD-revision-side ID") or (col == "CRD") or \
            (col == "CRD revision") or (col == "Folder name") or (col == "Symmetric") or (col == "Side") or (
            col == "User") or (col == "Origin") or (col == "Tire size") or \
            (col == "CTC revision") or (col == "ERD-ARD") or (col == "Design manual") or (col == "Design code") or \
            (col == "Rim flange protector") or (col == "Apex 3 layup") or (col == "Ply layu") or (
            col == "Flipper layup") or \
            (col == "Stiffener inside layup") or (col == "First chipper layup") or (col == "Toeguard layup") or (
            col == "Sidewall layup") or \
            (col == "Overlay layup") or (col == "Tread layup") or (col == "Bead configuration") or (col == "Type") or (
            col == "Description") or \
            (col == "Construction") or (col == "Material model") or (col == "DEW version") or (
            col == "Rolling surface") or (col == "Cooldown") or \
            (col == "Unit system") or (col == "Rim contour") or (col == "Test-component ID") or (
            col == "Component") or (col == "Compound") or (
            col == "Sample ID") or \
            (col == "Cord code") or (col == "Cord serial") or (
            col == "Treatment code") or \
            (col == "Test-load-pressure ID") or (col == "TD") or (
            col == "FP") or (col == "SR") or (col == "RR") or \
            (col == "FM") or (col == "COSTGV") or (col == "COSBO"):
        return "'" + str_input + "'"

    if str_input == 'null' or str_input == 'None':
        return 0
    elif str_input.isdigit() or (str_input.replace('.', '', 1).isdigit() and str_input.count('.') < 2) or (
            str_input.replace('-', '', 1).replace('.', '', 1).isdigit()):
        return fast_real(str_input)
    else:
        return "'" + str_input + "'"


def get_unique_id(connection):
    """Getting unique primary id from SQL"""
    sql_statement = 'select EM_REPO.shared_sequence.nextval from dual'
    try:
        # create a cursor
        with connection.cursor() as cursor:
            cursor.execute(sql_statement)
            return int(cursor.fetchone()[0])
    except cx_Oracle.Error as e:
        raise UploadProcessException("Could not allocate sequence ID: {0}".format(e)) from e

def get_crd_id(connection, crd):
    """Getting unique primary id from SQL"""
    sql_statement = 'select A_CCSD_ID from EM_REPO.A_CCSD where'
    try:
        # create a cursor
        with connection.cursor() as cursor:
            cursor.execute(sql_statement)
            while True:
                rows = cursor.fetchone()
                if not rows:
                    return 'NONE'
                else:
                    return str(rows[0])
    except cx_Oracle.Error as e:
        raise UploadProcessException("Could not allocate sequence ID: {0}".format(e)) from e

def search_and_delete(connection, first_value):
    """Getting unique primary id from SQL"""
    sql_statement = 'delete from EM_REPO.B_TESTS where B_TESTS_ID=ANY(select B_TESTS_ID from EM_REPO.BTESTS where ' \
                    '"Test ID"="{0}")'.format(first_value)
    try:
        # create a cursor
        with connection.cursor() as cursor:
            cursor.execute(sql_statement)
            print('deleted b_test with id',first_value)
    except cx_Oracle.Error as e:
        raise UploadProcessException("Could not allocate sequence ID: {0}".format(e)) from e


def search_and_update(connection, first_value):
    """Getting unique primary id from SQL"""
    sql_statement = 'delete from EM_REPO.B_TESTS where B_TESTS_ID=ANY(select B_TESTS_ID from EM_REPO.BTESTS where ' \
                    '"Test ID"="{0}")'.format(first_value)
    try:
        # create a cursor
        with connection.cursor() as cursor:
            cursor.execute(sql_statement)
            return int(cursor.fetchone()[0])
    except cx_Oracle.Error as e:
        raise UploadProcessException("Could not allocate sequence ID: {0}".format(e)) from e


def get_cols(cols, table_name):
    primary_key = config.get_table_primary_key(table_name)
    col_length = len(cols)
    col_string = '(' + put_double_quote_if_space_between_col_name_and_length_30(primary_key)
    parent_primary_key = config.get_parent_table_primary_key(table_name)
    if not table_name == 'A_CCSD':
        col_string += ",{0}".format(put_double_quote_if_space_between_col_name_and_length_30(parent_primary_key))
    for i in range(0, col_length):
        col_string += ',' + put_double_quote_if_space_between_col_name_and_length_30(str(cols[i]))
    return col_string + ')'


def get_extra_cols(cols, allowed_col_length, table_name):
    primary_key = config.get_table_primary_key(table_name)
    col_list = []
    col_length = len(cols)
    col_string = '(' + put_double_quote_if_space_between_col_name_and_length_30(primary_key)
    parent_primary_key = config.get_parent_table_primary_key(table_name)
    if not table_name == 'A_CCSD':
        col_string += ",{0}".format(put_double_quote_if_space_between_col_name_and_length_30(parent_primary_key))
    for i in range(0, col_length):
        if i >= allowed_col_length:
            col_list.append(truncate_30_chars(str(cols[i])))
            continue
        col_string += ',' + put_double_quote_if_space_between_col_name_and_length_30(str(cols[i]))
    return col_string + ')', col_list


def read_all_rows_and_save_extra(connection, table_name, cols, rows, allowed_col_length, link_dict):
    sql_list = []
    id_map = dict()
    col_string, col_list = get_extra_cols(cols, allowed_col_length, table_name)
    dict_data = dict()
    dict_data_link_back = dict()
    # col_string = get_cols(cols, table_name)
    link_key = ''
    if table_name == 'A_CCSD' or table_name == 'B_TESTS':
        link_key += config.get_table_link_back_key('A_CCSD')
    elif table_name == 'C_COMPONENTS':
        link_key += config.get_table_link_back_key('B_TESTS')
    elif table_name == 'D_REINFORCEMENTS':
        link_key += config.get_table_link_back_key('B_TESTS')
    elif table_name == 'E_INDICATORS':
        link_key += config.get_table_link_back_key('B_TESTS')
    link_back_key_index = cols.index(link_key)
    row_string = ''
    extra_row_string = []
    current_index = 0
    for i in range(0, len(rows)):
        actual_row_cols = len(rows[i])
        uid = get_unique_id(connection)
        first_value = str(rows[i][0])
        if table_name == 'A_CCSD':  # in each row first make sure if value exist then delete
            search_and_update(connection, first_value)
        if table_name == 'B_TEST':  # in each row first make sure if value exist then delete
            search_and_delete(connection, first_value)
        link_back_value = str(rows[i][cols.index(config.get_table_link_back_key(table_name))])
        id_map[link_back_value] = uid
        dict_data.update({uid: first_value})
        dict_data_link_back.update({uid: link_back_value})
        row_string += 'INTO EM_REPO.' + table_name + ' ' + col_string + ' VALUES({0}'.format(uid)
        if not table_name == 'A_CCSD':
            link_fk_key = config.get_key_by_value(link_dict, link_back_value)
            row_string += ",{0}".format(link_fk_key)
        row_string += ",'{0}'".format(first_value)
        for j in range(1, actual_row_cols):
            if j >= allowed_col_length:
                statement = prepare_extra_column_sql(table_name, uid, str(cols[j]), str(rows[i][j]))
                extra_row_string.append(statement)
                continue

            val = convert_number_or_into_string(str(rows[i][j]), cols[j])

            row_string += ",{0}".format(val)

        row_string += ')'
        sql_list.append(row_string)  # save normal columns
        row_string = ''
    # iterate through all extra col
    for sql_stmt in extra_row_string:
        extra_uid = get_unique_id(connection)
        sql_list.append(sql_stmt.replace('REPLACE_ID', str(extra_uid)))

    return dict_data, dict_data_link_back, sql_list, id_map


def read_all_rows_and_save(connection, table_name, cols, rows, link_dict):
    sql_list = []
    id_map = dict()
    allowed_col_length = config.get_table_total_cols(table_name)
    dict_data = dict()
    dict_data_link_back = dict()
    if len(cols) > allowed_col_length:
        return read_all_rows_and_save_extra(connection, table_name, cols, rows, allowed_col_length, link_dict)
    else:
        col_string = get_cols(cols, table_name)
        link_key = ''
        if table_name == 'A_CCSD' or table_name == 'B_TESTS':
            link_key += config.get_table_link_back_key('A_CCSD')
        elif table_name == 'C_COMPONENTS':
            link_key += config.get_table_link_back_key('B_TESTS')
        elif table_name == 'D_REINFORCEMENTS':
            link_key += config.get_table_link_back_key('B_TESTS')
        elif table_name == 'E_INDICATORS':
            link_key += config.get_table_link_back_key('B_TESTS')
        link_back_key_index = cols.index(link_key)
        row_string = ''
        for i in range(0, len(rows)):
            actual_row_cols = len(rows[i])
            uid = get_unique_id(connection)
            first_value = str(rows[i][0])
            if table_name == 'B_TEST':  # in each row first make sure if value exist then delete
                search_and_delete(connection, first_value)
            link_back_value = str(rows[i][cols.index(config.get_table_link_back_key(table_name))])
            id_map[link_back_value] = uid
            dict_data.update({uid: first_value})
            dict_data_link_back.update({uid: link_back_value})
            row_string += 'INTO  EM_REPO.' + table_name + ' ' + col_string + ' VALUES({0}'.format(uid)
            if not table_name == 'A_CCSD':
                link_fk_key = config.get_key_by_value(link_dict, link_back_value)
                row_string += ",{0}".format(link_fk_key)
            row_string += ",'{0}'".format(first_value)
            for j in range(1, actual_row_cols):
                val = convert_number_or_into_string(str(rows[i][j]), cols[j])
                row_string += ",{0}".format(val)
            row_string += ')'
            sql_list.append(row_string)  # save normal columns
            row_string = ''
    return dict_data, dict_data_link_back, sql_list, id_map


def prepare_extra_column_sql(table_name, primary_key_value, col_name, col_value):
    primary_key = config.get_table_primary_key(table_name)
    primary_key_extra = config.get_table_primary_key(table_name + '_EXTRA')
    sql_string = ''
    sql_string += 'INTO EM_REPO.' + table_name + '_EXTRA '
    sql_string += '("{0}","{1}","Column name","Column value") '.format(primary_key_extra, primary_key)
    sql_string += "VALUES (REPLACE_ID,{0},'{1}','{2}')".format(primary_key_value, col_name, col_value)
    return sql_string


def save_all_tables(connection, sql_statement, json_file_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_statement)
            connection.commit()
    except cx_Oracle.Error as e:
        raise UploadProcessException('Could not save data!: {0}'.format(e)) from e


def delete_all_rows(connection, table_name):
    sql_statement = 'Truncate Table ' + table_name
    try:
        # create a cursor
        with connection.cursor() as cursor:
            # execute the insert statement
            cursor.execute(sql_statement)
            print('delete completed:' + table_name)
    except cx_Oracle.Error as error:
        print('Error occurred while deleting:' + table_name)
        print(error)


def delete_table(connection, table_name):
    sql_statement = 'DROP TABLE "' + table_name + '" CASCADE CONSTRAINTS'
    try:
        # create a cursor
        with connection.cursor() as cursor:
            # execute the insert statement
            cursor.execute(sql_statement)
            print('delete table:' + table_name)
    except cx_Oracle.Error as error:
        print('Error occurred while deleting:' + table_name)
        print(error)


def delete_all_tables(connection):
    delete_table(connection, 'E_INDICATORS_EXTRA')
    delete_table(connection, 'E_INDICATORS')
    delete_table(connection, 'D_REINFORCEMENTS_EXTRA')
    delete_table(connection, 'D_REINFORCEMENTS')
    delete_table(connection, 'C_COMPONENTS_EXTRA')
    delete_table(connection, 'C_COMPONENTS')
    delete_table(connection, 'B_TESTS_EXTRA')
    delete_table(connection, 'B_TESTS')
    delete_table(connection, 'A_CCSD_EXTRA')
    delete_table(connection, 'A_CCSD')


def delete_all_tables_data(connection):
    delete_all_rows(connection, 'E_INDICATORS_EXTRA')
    delete_all_rows(connection, 'E_INDICATORS')
    delete_all_rows(connection, 'D_REINFORCEMENTS_EXTRA')
    delete_all_rows(connection, 'D_REINFORCEMENTS')
    delete_all_rows(connection, 'C_COMPONENTS_EXTRA')
    delete_all_rows(connection, 'C_COMPONENTS')
    delete_all_rows(connection, 'B_TESTS_EXTRA')
    delete_all_rows(connection, 'B_TESTS')
    delete_all_rows(connection, 'A_CCSD_EXTRA')
    delete_all_rows(connection, 'A_CCSD')


def put_double_quote_if_space_between_col_name_and_length_30(col_name):
    """As the Oracle only allows maximum 30 characters for columns names, we limit the names of the columns to 30
    from JSON """

    str = col_name
    if len(col_name) > 30:
        return '"' + truncate_30_chars(str) + '"'
    return '"' + col_name + '"'


def truncate_30_chars(input_string):
    return input_string[:30]
