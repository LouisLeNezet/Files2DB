#!/usr/bin/env python3
"""
Created on 22/10/2021
@author: LouisLeNezet
Check for presence absence of file, sheets, columns
"""

import logging
import re
from importlib import resources

import pandas as pd
from openpyxl import load_workbook

from ..read_file.data_read import read_file
from ..ui.get_infos import get_file_path


def load_file_orga():
    """Load internal file_orga.csv as a Pandas DataFrame and transform it into a dictionary."""
    with resources.open_text("files2db.data", "file_orga.csv") as csvfile:
        orga = pd.read_csv(csvfile)

        # Validate required columns
        required_columns = {"file", "columns_needed", "columns_sup"}
        missing_columns = required_columns - set(orga.columns)
        if missing_columns:
            raise KeyError(
                f"Missing required columns in organisation file: {sorted(missing_columns)}"
            )

        # Convert columns_needed from comma-separated strings to lists
        orga["columns_needed"] = orga["columns_needed"].apply(lambda x: x.split(","))

        # Convert columns_sup to boolean (if it's not already)
        orga["columns_sup"] = orga["columns_sup"].astype(bool)

        # Convert DataFrame to dictionary
        orga_dict = orga.set_index("file").to_dict(orient="index")

        return orga_dict


def validate_files_presence(files_needed: set, files_available: set, path: str):
    """Check if required files exist in the dataset."""
    missing_files = files_needed - files_available
    extra_files = files_available - files_needed

    if missing_files:
        raise KeyError(
            f"Missing files {', '.join(sorted(missing_files))} in my_organisation file {path}"
        )

    if extra_files:
        logging.warning("Extra files %s present in %s and not needed", extra_files, path)


def validate_columns(df: pd.DataFrame, path: str, cols_need: list, cols_sup: bool = False):
    """Check for missing and extra columns in each file."""
    # Convert cols_need to a set
    cols_need_set = set(cols_need)

    missing = cols_need_set - set(df.columns)
    extra = set(df.columns) - cols_need_set

    if missing:
        raise KeyError(f"Missing columns {missing} in {path}")

    if not cols_sup and extra:
        logging.warning("Extra columns %s in %s and won't be used", extra, path)


def _apply_key(orga_entry, df, key, func):
    val = orga_entry.get(key)
    if not isinstance(val, str):
        return
    for col in (c.strip() for c in val.split(",") if c.strip()):
        if col in df.columns:
            df[col] = func(df[col])


def validate_columns_orga(df: pd.DataFrame, file_name: str, rules: dict):
    """Check for missing and extra columns in each file based on organisation specifications."""
    validate_columns(
        df,
        path=file_name,
        cols_need=list(rules["columns_needed"]),
        cols_sup=rules["columns_sup"],
    )

    orga_entry = rules

    _apply_key(
        orga_entry, df, "integer", lambda s: pd.to_numeric(s, errors="coerce").astype("Int64")
    )
    _apply_key(
        orga_entry,
        df,
        "list",
        lambda s: s.apply(lambda x: x.split(",") if isinstance(x, str) else x),
    )
    _apply_key(
        orga_entry,
        df,
        "boolean",
        lambda s: s.apply(
            lambda x: str(x).lower() in ("true", "1", "yes", "on") if isinstance(x, str) else x
        ).astype("boolean"),
    )

    return df


def get_db_from_excel(path: str, orga_dict: dict) -> tuple:
    """Load and validate an Excel file based on organisation specifications."""
    path_file = get_file_path(path)

    try:
        wb = load_workbook(path_file, read_only=True)
    except FileNotFoundError as error:
        logging.error("File %s not found", path)
        raise error

    validate_files_presence(set(orga_dict.keys()), set(wb.sheetnames), path)

    if set(wb.sheetnames) != {"Files", "FieldsRules", "ValuesMap"}:
        raise KeyError(
            f"Excel sheets in {path} should only contain ",
            "['Files', 'FieldsRules', 'ValuesMap'] no more no less",
        )

    db_dict = {sheet: read_file(path_file, sheet_name=sheet) for sheet in orga_dict}

    return db_dict["Files"], db_dict["FieldsRules"], db_dict["ValuesMap"]


def get_db_from_csv(path: str, orga_dict: dict) -> tuple:
    """Load and validate a CSV file based on organisation specifications."""
    path_file = get_file_path(path)
    all_db_files = pd.read_csv(path_file)

    if set(all_db_files.columns) != {"file", "path", "sep"}:
        raise KeyError(f"Columns in {path} should only contain ['file', 'path', 'sep']")

    if set(all_db_files["file"]) != {"Files", "FieldsRules", "ValuesMap"}:
        raise KeyError(
            f"'file' column in {path} should only contain "
            "['Files', 'FieldsRules', 'ValuesMap'] no more no less"
        )

    validate_files_presence(set(orga_dict.keys()), set(all_db_files["file"]), path)

    db_dict = {}
    all_db_files.set_index("file", inplace=True)
    for file, file_path, sep in all_db_files.itertuples():
        db_path_file = get_file_path(file_path)
        db_dict[file] = read_file(db_path_file, sep=sep)

    return db_dict["Files"], db_dict["FieldsRules"], db_dict["ValuesMap"]


def get_db_from_path(path_file: str, db_orga: dict) -> tuple:
    """
    Get the database from a file based on its extension and organisation specifications.
    Parameters
    ----------
    path_file : str
        Full path to the file.
    db_orga : dict
        Organisation dictionary containing file specifications.
    Returns
    -------
    db_dict : dict
        Dictionary containing the database loaded from the file.
    Raises
    ------
    TypeError
        If the file extension is not supported (not .csv or .xlsx).
    """
    path_file = get_file_path(path_file)

    if not isinstance(path_file, str):
        raise TypeError("The path_file should be a string")
    if not isinstance(db_orga, dict):
        raise TypeError("The db_orga should be a dictionary")

    if re.search(string=path_file, pattern=r"\.csv$"):
        files_list, fields_rules, values_map = get_db_from_csv(path_file, db_orga)
    elif re.search(string=path_file, pattern=r"\.(xlsx|xls|xlsm)"):
        files_list, fields_rules, values_map = get_db_from_excel(path_file, db_orga)
    else:
        raise TypeError(f"File {path_file} should be either an .xlsx, .xls, xlsm or a .csv")

    return files_list, fields_rules, values_map


def get_db_from(
    path_orga: str | None = None,
    path_files: str | None = None,
    path_fields_rules: str | None = None,
    path_values_map: str | None = None,
    sep: str = ",",
):

    db_orga = load_file_orga()

    if path_orga is not None:
        if not all(f is None for f in [path_files, path_fields_rules, path_values_map]):
            raise ValueError(
                "--path-orga should be used alone. "
                "No --path-files, --path-fields-rules or --path-values-map allowed"
            )
        files_list, fields_rules, values_map = get_db_from_path(path_orga, db_orga)
    else:
        if path_files is None:
            raise ValueError("--path-orga nor --path-files provided")
        else:
            path_files_norm = get_file_path(path_files)
            files_list = read_file(path_files_norm, sep=sep)

            if path_fields_rules is not None:
                path_fields_rules_norm = get_file_path(path_fields_rules)
                fields_rules = read_file(path_fields_rules_norm, sep=sep)

            if path_values_map is not None:
                path_values_map_norm = get_file_path(path_values_map)
                values_map = read_file(path_values_map_norm, sep=sep)

    logging.info("Input files loaded successfully")

    files_list = validate_columns_orga(files_list, "Files", db_orga["Files"])
    fields_rules = validate_columns_orga(fields_rules, "FieldsRules", db_orga["FieldsRules"])
    values_map = validate_columns_orga(values_map, "ValuesMap", db_orga["ValuesMap"])

    logging.info("Input files successfully checked")

    return (files_list, fields_rules, values_map)
