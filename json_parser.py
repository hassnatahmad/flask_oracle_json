import json
import os
from app import app
import oracle_db
import db_config as config


def col_length_validation(table_name, cols):
    col_length = config.get_table_total_cols(table_name)
    if col_length > len(cols):
        return False
    else:
        return True


def save_all_json(json_file_name):
    error_code = 400
    try:
        # Load data from json
        with open(os.path.join(app.config['UPLOAD_FOLDER'], json_file_name)) as f:
            json_data = json.load(f)
        A_Geometries_cols = json_data["A_Geometries"]["columns"]
        A_Geometries_rows = json_data["A_Geometries"]["data"]
        B_Tests_cols = json_data["B_Tests"]["columns"]
        B_Tests_rows = json_data["B_Tests"]["data"]
        C_Loading_conditions_cols = json_data["C_Loading_conditions"]["columns"]
        C_Loading_conditions_rows = json_data["C_Loading_conditions"]["data"]
        D_Components_cols = json_data["D_Components"]["columns"]
        D_Components_rows = json_data["D_Components"]["data"]
        E_Components_results_cols = json_data["E_Components_results"]["columns"]
        E_Components_results_rows = json_data["E_Components_results"]["data"]
        # We check here that does json contains valid number of column
        if not col_length_validation('A_GEOMETRIES', A_Geometries_cols) or not col_length_validation('B_TESTS',B_Tests_cols) or not col_length_validation('C_LOADING_CONDITIONS', C_Loading_conditions_cols) or not col_length_validation('D_COMPONENTS', D_Components_cols) or not col_length_validation('E_COMPONENTS', E_Components_results_cols):
            # If file exists, delete it because it is invalid
            if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], json_file_name)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], json_file_name))
            error_code = 400
            return 'JSON File is corrupted. File has been deleted from server',error_code

        # delete all rows only for testing purpose, dont do it on live system , order matters
        # oracle_db.delete_all_tables() #delets whole table
        # oracle_db.delete_all_tables_data() #deletes all rows from all tables

        # start saving json
        print('Please wait database is being saved')
        a_dict, a_link_back_dict = oracle_db.read_all_rows_and_save('A_GEOMETRIES', A_Geometries_cols,
                                                                    A_Geometries_rows)
        b_dict, b_link_back_dict = oracle_db.read_all_rows_and_save('B_TESTS', B_Tests_cols, B_Tests_rows)
        c_dict, c_link_back_dict = oracle_db.read_all_rows_and_save('C_LOADING_CONDITIONS', C_Loading_conditions_cols,
                                                                    C_Loading_conditions_rows)
        d_dict, d_link_back_dict = oracle_db.read_all_rows_and_save('D_COMPONENTS', D_Components_cols,
                                                                    D_Components_rows)
        e_dict, e_link_back_dict = oracle_db.read_all_rows_and_save('E_COMPONENTS', E_Components_results_cols,
                                                                    E_Components_results_rows)

        oracle_db.save_a_b_table('A_B', a_dict, b_dict, b_link_back_dict)
        oracle_db.save_b_c_table('B_C', b_dict, c_dict, c_link_back_dict)
        oracle_db.save_b_d_table('B_D', b_dict, d_dict, d_link_back_dict)
        oracle_db.save_c_e_table('C_E', c_dict, e_dict, e_link_back_dict)
        print('database is saved')

        # start logging data from sql

        # oracle_db.get_all_rows('A_GEOMETRIES')
        # oracle_db.get_all_rows('B_TESTS')
        # oracle_db.get_all_rows('C_LOADING_CONDITIONS')
        # oracle_db.get_all_rows('D_COMPONENTS')
        # oracle_db.get_all_rows('E_COMPONENTS_RESULTS')
        return 'JSON File is uploaded',error_code
    except KeyError:  # includes simplejson.decoder.JSONDecodeError
        # If file exists, delete it because it is invalid
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], json_file_name)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], json_file_name))
        return 'Decoding JSON has failed. File has been deleted from server'
