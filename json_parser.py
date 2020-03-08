import json
import os
from app import app
import oracle_db


def save_all_json(json_file_name):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], json_file_name)) as f:
        json_data = json.load(f)
    # Load data from json
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

    # delete all rows only for testing purpose, dont do it on live system , order matters
    #oracle_db.delete_all_tables() #delets whole table
    #oracle_db.delete_all_tables_data() #deletes all rows from all tables

    # start saving json
    oracle_db.read_all_rows_and_save('A_GEOMETRIES', A_Geometries_cols, A_Geometries_rows)
    oracle_db.read_all_rows_and_save('B_TESTS', B_Tests_cols, B_Tests_rows)
    oracle_db.read_all_rows_and_save('C_LOADING_CONDITIONS', C_Loading_conditions_cols, C_Loading_conditions_rows)
    # oracle_db.read_all_rows_and_save('D_COMPONENTS', D_Components_cols, D_Components_rows)
    # oracle_db.read_all_rows_and_save('E_COMPONENTS_RESULTS', E_Components_results_cols, E_Components_results_rows)

    # start logging data from sql

    # oracle_db.get_all_rows('A_GEOMETRIES')
    # oracle_db.get_all_rows('B_TESTS')
    # oracle_db.get_all_rows('C_LOADING_CONDITIONS')
    # oracle_db.get_all_rows('D_COMPONENTS')
    # oracle_db.get_all_rows('E_COMPONENTS_RESULTS')
