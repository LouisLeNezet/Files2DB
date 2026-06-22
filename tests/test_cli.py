#!/usr/bin/env python3
"""
Created on 07/10/2021
@author: Louis Le Nézet
"""

import os
import unittest
from unittest.mock import patch

from typer.testing import CliRunner

from files2db.cli import app

runner = CliRunner()


class TestCLI(unittest.TestCase):
    def setUp(self):
        """Set up test data path"""
        self.test_data_path = os.path.join(os.path.dirname(__file__), "test_dataset")

    def test_version(self):
        result = runner.invoke(app, ["--version"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("files2db version", result.stdout)

    def test_license(self):
        result = runner.invoke(app, ["--license"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("license", result.stdout.lower())

    def test_warranty(self):
        result = runner.invoke(app, ["--warranty"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("warranty", result.stdout.lower())

    @patch("files2db.cli.sys.argv", ["files2db"])
    def test_no_arguments(self):
        result = runner.invoke(app, [])

        print(result.exit_code)
        print(result.stdout)

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage:", result.stdout)

    @patch("files2db.cli.get_db_from")
    @patch("files2db.cli.main")
    def test_main_no_error(self, mock_main, mock_get_db):
        mock_get_db.return_value = ([], None, None)
        db_path = os.path.join(self.test_data_path, "test1/orga.csv")
        result = runner.invoke(
            app,
            [
                "--path-orga",
                db_path,
                "--output-dir",
                "outdir",
                "--output-prefix",
                "testprefix",
            ],
        )

        self.assertEqual(result.exit_code, 0)
        mock_main.assert_called_once()

    @patch("files2db.cli.get_db_from")
    @patch("files2db.cli.main")
    def test_main_error_normalise_table_missing(self, mock_main, mock_get_db):
        mock_get_db.return_value = ([], None, None)
        db_path = os.path.join(self.test_data_path, "test1/orga.csv")
        result = runner.invoke(
            app,
            [
                "--path-orga",
                db_path,
                "--normalize",
                "--output-dir",
                "outdir",
                "--output-prefix",
                "testprefix",
            ],
        )
        print(result.exception)

        self.assertEqual(result.exit_code, 1)
        self.assertRegex(
            str(result.exception),
            "Normalising step needs at least fields rules or values map table.",
        )
        mock_main.assert_not_called()

    def test_main_error_main_table_mising(self):
        result = runner.invoke(
            app,
            [
                "--output-dir",
                "outdir",
                "--output-prefix",
                "testprefix",
            ],
        )

        self.assertEqual(result.exit_code, 1)
        self.assertRegex(result.stdout, "Error: You must provide either:")

    def test_main_error_main_table_mising_with_normalize(self):
        result = runner.invoke(
            app,
            [
                "--normalize",
                "--output-dir",
                "outdir",
                "--output-prefix",
                "testprefix",
            ],
        )

        self.assertEqual(result.exit_code, 1)
        self.assertRegex(result.stdout, "Error: You must provide either:")
