[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/) [![codecov](https://codecov.io/gh/louislenezet/files2db/branch/dev/graph/badge.svg)](https://codecov.io/gh/louislenezet/files2db) [![License](https://img.shields.io/badge/license-GPLv3-green.svg)](https://opensource.org/licenses/gpl-3-0)

<div align="center">
  <img src="assets/logo_files2db.svg" width="250">
</div>

# Files2DB

> One script to rule them all, one script to find them, one script to standardize them all and in a database bind them.

`files2db` is a python tool to help anyone concatenate, normalize and check a multitude of flat plain files (`.csv`, `.xlsx`) into a single, standardized database.

## Problematic and objectives

Projects with numerous data sources often begin with many plain files (CSV and Excel) whose variable names and value formats are not standardized.
Record identities are frequently encoded in complex, multi-field keys that differ between files.

`files2db` aims to produce a single working dataset with normalized fields and a formal unique identifier for each observation, enabling easy updates, clear error reporting, and full traceability and reproducibility.

It reliably identifies observations even when candidate keys differ or some identifying fields are missing, normalizes data by splitting/merging fields and converting formats, and validates content by checking formats and internal consistency while reporting errors with causes and locations.

## Python script

`files2db` automates concatenating and ingesting many source files.
I takes as input a CSV or Excel file that lists the files to integrate, the tool reads each file, extracts and normalizes available fields, and updates a single database so adding new source files becomes trivial. The process writes a CSV containing the full consolidated dataset and a separate error report that records each issue’s reason and location; it also validates and, when possible, coerces field formats and generates a unique identifier for every observation.
