#!/usr/bin/env python3
"""
Created on 25/11/2022
@author: LouisLeNezet
Testing scripts for the different common functions.
"""

import logging
import os
import unittest
from unittest.mock import patch

import pandas as pd

from files2db.read_file.orga_read import (
    get_db_from,
    get_db_from_csv,
    get_db_from_excel,
    get_db_from_path,
    load_file_orga,
    validate_columns,
    validate_columns_orga,
    validate_files_presence,
)


class TestValidateFiles(unittest.TestCase):
    """Check that the validate_files_presence function works as expected."""

    def setUp(self):
        """Set up test"""
        logging.getLogger().setLevel(logging.CRITICAL)

    def test_validate_files_presence_missing_files(self):
        """Test missing files detection."""
        with self.assertRaises(KeyError) as context:
            validate_files_presence({"file1", "file2"}, {"file1"}, "test.xlsx")
        self.assertIn("Missing files file2", str(context.exception))

    @patch("logging.warning")
    def test_validate_files_presence_extra_files(self, mock_log):
        """Test logging when extra files are present."""
        validate_files_presence({"file1"}, {"file1", "file2"}, "test.xlsx")
        mock_log.assert_called_once_with(
            "Extra files %s present in %s and not needed", {"file2"}, "test.xlsx"
        )

    def test_validate_files_presence_correct(self):
        """Test when all files are correctly present."""
        try:
            validate_files_presence({"file1", "file2"}, {"file1", "file2"}, "test.xlsx")
        except KeyError:
            self.fail("validate_files_presence raised KeyError unexpectedly!")


class TestingLoadFileOrga(unittest.TestCase):
    """Class for testing load_file_orga"""

    def setUp(self):
        """Set up test"""
        logging.getLogger().setLevel(logging.CRITICAL)
        return super().setUp()

    def test_load_file_orga(self):
        """Test load_file_orga"""
        db_orga = load_file_orga()
        self.assertEqual(
            list(db_orga.keys()),
            ["Files", "FieldsRules", "ValuesMap"],
        )
        self.assertEqual(
            list(db_orga["Files"].keys()),
            ["columns_needed", "columns_sup", "integer", "list", "boolean"],
        )
        self.assertEqual(
            db_orga["Files"]["columns_needed"],
            [
                "FilePath",
                "SheetName",
                "LineStart",
                "LineEnd",
                "Header",
                "ColStart",
                "ColEnd",
                "ToAdd",
                "AsCorrection",
                "Separator",
            ],
        )


class TestColumnValidation(unittest.TestCase):
    """Check that the validate_columns function works as expected."""

    def setUp(self):
        """Set up test"""
        logging.getLogger().setLevel(logging.CRITICAL)

    def test_validate_columns_missing_columns(self):
        """Test missing columns error."""
        with self.assertRaises(KeyError) as context:
            validate_columns(
                pd.DataFrame(columns=["A"]),
                "test.xlsx",
                cols_need={"A", "B"},
                cols_sup=False,
            )
        self.assertIn("Missing columns {'B'} in", str(context.exception))

    @patch("logging.warning")
    def test_validate_columns_extra_columns(self, mock_log):
        """Test logging when extra columns exist."""
        validate_columns(
            pd.DataFrame(columns=["A", "B", "C"]),
            "test.xlsx",
            cols_need={"A", "B"},
            cols_sup=False,
        )
        mock_log.assert_called_once_with(
            "Extra columns %s in %s and won't be used", {"C"}, "test.xlsx"
        )

    def test_validate_columns_correct(self):
        """Test when all columns match expectations."""
        try:
            validate_columns(
                pd.DataFrame(columns=["A", "B", "C"]),
                "test.xlsx",
                cols_need={"A", "B"},
                cols_sup=True,
            )
        except KeyError:
            self.fail("validate_columns raised KeyError unexpectedly!")


class TestColumnValidationOrga(unittest.TestCase):
    """Check that the validate_columns_orga function works as expected."""

    def setUp(self):
        """Set up test"""
        logging.getLogger().setLevel(logging.CRITICAL)

    def test_validate_columns_missing_columns(self):
        """Test missing columns error."""
        with self.assertRaises(KeyError) as context:
            validate_columns_orga(
                pd.DataFrame(columns=["A", "D"]),
                "file1",
                {"columns_needed": ["A", "B"], "columns_sup": False},
            )
        self.assertIn("Missing columns {'B'} in", str(context.exception))

    @patch("logging.warning")
    def test_validate_columns_orga_extra_columns(self, mock_log):
        """Test logging when extra columns exist."""
        validate_columns_orga(
            pd.DataFrame(columns=["C", "D", "E"]),
            "file2",
            {"columns_needed": ["C", "D"], "columns_sup": False},
        )
        mock_log.assert_called_once_with("Extra columns %s in %s and won't be used", {"E"}, "file2")

    def test_validate_columns_orga_correct(self):
        """Test validate_columns_orga."""
        validate_columns_orga(
            pd.DataFrame(columns=["C", "D", "E"]),
            "file2",
            {"columns_needed": ["C", "D"], "columns_sup": True},
        )


class TestGetDBFromExcel(unittest.TestCase):
    """Check that the get_db_from_excel function works as expected."""

    def setUp(self):
        """Set up test data path"""
        self.test_data_path = os.path.join(os.path.dirname(__file__), "test_dataset")

    def test_get_db_from_excel_missing_file(self):
        """Test missing file error."""
        file_path = os.path.join(self.test_data_path, "missing.xlsx")
        with self.assertRaises(FileNotFoundError):
            get_db_from_excel(file_path, {})

    def test_get_db_from_excel_extra_sheets(self):
        """Test missing file error."""
        file_path = os.path.join(self.test_data_path, "RepTest_wrong_extra_sheets.xlsx")
        with self.assertRaises(KeyError) as context:
            get_db_from_excel(file_path, {})
        self.assertIn(
            "should only contain 'Files', 'FieldsRules', 'ValuesMap' no more no less",
            str(context.exception),
        )

    def test_get_db_from_excel_missing_sheet(self):
        """Test missing sheet error."""
        file_path = os.path.join(self.test_data_path, "RepTest_wrong.xlsx")
        with self.assertRaises(KeyError) as context:
            get_db_from_excel(file_path, load_file_orga())
        self.assertIn("'Missing files ValuesMap in", str(context.exception))


class TestGetDBFromPath(unittest.TestCase):
    """Check that the get_db_from_path function works as expected."""

    def setUp(self):
        """Set up test data path"""
        self.test_data_path = os.path.join(os.path.dirname(__file__), "test_dataset")
        logging.getLogger().setLevel(logging.CRITICAL)

    @patch("logging.warning")
    def test_get_db_from_path_correct_xlsx(self, mock_log):
        """Test missing sheet error."""
        file_path = os.path.join(self.test_data_path, "RepTest_correct.xlsx")
        files_list, fields_rules, values_map = get_db_from_path(file_path, load_file_orga())
        self.assertEqual(files_list.shape, (2, 20))
        self.assertEqual(fields_rules.shape, (10, 15))
        self.assertEqual(values_map.shape, (6, 3))

    def test_get_db_from_path_correct_csv(self):
        """Test missing sheet error."""
        file_path = os.path.join(self.test_data_path, "test1/orga.csv")
        files_list, fields_rules, values_map = get_db_from_path(file_path, load_file_orga())
        self.assertEqual(files_list.shape, (4, 18))
        self.assertEqual(fields_rules.shape, (9, 14))
        self.assertEqual(values_map.shape, (2, 3))
        self.assertEqual(fields_rules["DelMatch"][5], "delmatchitis,othermatch")
        self.assertTrue(pd.isna(fields_rules["SepPattern"].iloc[2]))


class TestGetDBFromCSV(unittest.TestCase):
    """Check that the get_db_from_csv function works as expected."""

    def setUp(self):
        """Set up test data path"""
        self.test_data_path = os.path.join(os.path.dirname(__file__), "test_dataset")

    def test_get_db_from_csv_wrong_columns(self):
        """Test wrong columns error."""
        file_path = os.path.join(self.test_data_path, "wrong_orga.csv")
        with self.assertRaises(KeyError) as context:
            get_db_from_csv(file_path, {})
        self.assertIn("should only contain 'file', 'path', 'sep'", str(context.exception))

    def test_get_db_from_csv_wrong_values_in_files(self):
        """Test wrong columns error."""
        file_path = os.path.join(self.test_data_path, "wrong_orga_extra_file.csv")
        with self.assertRaises(KeyError) as context:
            get_db_from_csv(file_path, {})
        self.assertIn(
            "should only contain 'Files', 'FieldsRules', 'ValuesMap' no more no less",
            str(context.exception),
        )

    def test_get_db_from_csv_missing_files(self):
        """Test missing files error."""
        file_path = os.path.join(self.test_data_path, "missing.csv")
        with self.assertRaises(FileNotFoundError):
            get_db_from_csv(file_path, {})

    def test_get_db_from_csv_correct(self):
        """Test correct file."""
        file_path = os.path.join(self.test_data_path, "test1/orga.csv")
        files_list, fields_rules, values_map = get_db_from_csv(file_path, load_file_orga())
        self.assertEqual(files_list.shape, (4, 18))
        self.assertEqual(fields_rules.shape, (9, 14))
        self.assertEqual(values_map.shape, (2, 3))


class TestGetDBFromPATH(unittest.TestCase):
    """Check that the get_db_from_path function works as expected."""

    def setUp(self):
        """Set up test data path"""
        self.test_data_path = os.path.join(os.path.dirname(__file__), "test_dataset")

    def test_get_db_from_path_correct(self):
        """Test should work."""
        file_path = os.path.join(self.test_data_path, "RepTest_correct.xlsx")
        files_list, fields_rules, values_map = get_db_from_path(file_path, load_file_orga())
        self.assertEqual(files_list.shape, (2, 20))
        self.assertEqual(fields_rules.shape, (10, 15))
        self.assertEqual(values_map.shape, (6, 3))

    def test_get_db_from_path_orga_wrong_db_format(self):
        """Test wrong db_orga type."""
        file_path = os.path.join(self.test_data_path, "RepTest_correct.xlsx")
        with self.assertRaises(TypeError) as context:
            get_db_from_path(file_path, [])
        self.assertIn("The db_orga should be a dictionary", str(context.exception))

    def test_get_db_from_path_orga_wrong_file_format(self):
        """Test wrong file format."""
        # From xlsx
        file_path = os.path.join(self.test_data_path, "RepTest_correct.tsv")
        with self.assertRaises(TypeError) as context:
            get_db_from_path(file_path, load_file_orga())
        self.assertIn("should be either an .xlsx, .xls, xlsm or a .csv", str(context.exception))


class TestGetDBFrom(unittest.TestCase):
    """Check that the get_db_from function works as expected."""

    def setUp(self):
        """Set up test data path"""
        self.test_data_path = os.path.join(os.path.dirname(__file__), "test_dataset")

    def test_get_db_from_wrong_columns(self):
        """Test wrong columns error."""
        file_path = os.path.join(self.test_data_path, "wrong_orga.csv")
        with self.assertRaises(KeyError) as context:
            get_db_from(path_orga=file_path)
        self.assertIn("Columns in", str(context.exception))

    def test_get_db_from_missing_files(self):
        """Test missing files error."""
        file_path = os.path.join(self.test_data_path, "missing.csv")
        with self.assertRaises(FileNotFoundError):
            get_db_from(path_orga=file_path)

    def test_get_db_from_path_orga_not_alone(self):
        """Test path_orga should be used alone."""
        path_files = os.path.join(self.test_data_path, "test1/files.csv")
        path_values_map = os.path.join(self.test_data_path, "test1/values_map.csv")
        with self.assertRaises(ValueError) as context:
            get_db_from(path_orga=path_files, path_values_map=path_values_map)
        self.assertIn("--path-orga should be used alone.", str(context.exception))

    def test_get_db_from_no_path_file(self):
        """Test no path_files provided."""
        path_values_map = os.path.join(self.test_data_path, "test1/values_map.csv")
        with self.assertRaises(ValueError) as context:
            get_db_from(path_values_map=path_values_map)
        self.assertIn("--path-orga nor --path-files provided", str(context.exception))

    def test_get_db_from_correct(self):
        """Test correct file."""
        # From CSV
        file_path = os.path.join(self.test_data_path, "test1/orga.csv")
        files_list, fields_rules, values_map = get_db_from(path_orga=file_path)
        self.assertEqual(files_list.shape, (4, 18))
        self.assertEqual(fields_rules.shape, (9, 14))
        self.assertEqual(values_map.shape, (2, 3))
        self.assertEqual(fields_rules["DelMatch"][5], ["delmatchitis", "othermatch"])
        self.assertTrue(pd.isna(fields_rules["SepPattern"].iloc[2]))

        # From xlsx
        file_path = os.path.join(self.test_data_path, "RepTest_correct.xlsx")
        files_list, fields_rules, values_map = get_db_from(file_path)
        self.assertEqual(files_list.shape, (2, 20))
        self.assertEqual(fields_rules.shape, (10, 15))
        self.assertEqual(values_map.shape, (6, 3))

        # From multiple CSV
        path_files = os.path.join(self.test_data_path, "test1/files.csv")
        path_fields_rules = os.path.join(self.test_data_path, "test1/fields_rules.csv")
        path_values_map = os.path.join(self.test_data_path, "test1/values_map.csv")
        files_list, fields_rules, values_map = get_db_from(
            path_files=path_files,
            path_fields_rules=path_fields_rules,
            path_values_map=path_values_map,
            sep=";",
        )
        self.assertEqual(files_list.shape, (4, 18))
        self.assertEqual(fields_rules.shape, (9, 14))
        self.assertEqual(values_map.shape, (2, 3))


if __name__ == "__main__":
    unittest.main()
