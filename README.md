[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/) [![codecov](https://codecov.io/gh/louislenezet/files2db/branch/dev/graph/badge.svg)](https://codecov.io/gh/louislenezet/files2db) [![License](https://img.shields.io/badge/license-GPLv3-green.svg)](https://opensource.org/licenses/gpl-3-0)

# Files2DB

<table>
  <tr>
    <td>
      <p>
        <i>One script to rule them all, one script to find them, one script to norm them all and in a database bind them.</i>
      </p>
      <p>
        <strong>files2db</strong> is a python tool to help anyone concatenate, normalize and check a multitude of flat plain files (.csv, .xlsx) into a single, standardized database.
      </p>
    </td>
    <td style="text-align:right;">
      <img src="docs/assets/logo_files2db.png" alt="Files2DB Logo" height="100%"/>
    </td>
  </tr>
</table>

## 1. Problematic and objectives

Projects with numerous data sources often begin with many plain files (`.csv` and `.xlsx`) whose variable names and value formats are not standardized.
Record identities are frequently encoded in complex, multi-field keys that differ between files.

_files2db_ aims to produce a single working dataset with normalized fields and a formal unique identifier for each observation, enabling easy updates, clear error reporting, and full traceability and reproducibility.

It reliably identifies observations even when candidate keys differ or some identifying fields are missing, normalizes data by splitting/merging fields and converting formats, and validates content by checking formats and internal consistency while reporting errors with causes and locations.

## 2. Python script

_files2db_ automates concatenating and ingesting many source files.
I takes as input a `.csv` or `.xlsx` file that lists the files to integrate, the tool reads each file, extracts and normalizes available fields, and updates a single database so adding new source files becomes trivial. The process writes a `.csv` containing the full consolidated dataset and a separate error report that records each issue’s reason and location; it also validates and, when possible, coerces field formats and generates a unique identifier for every observation.

### 2.1 Installation

_files2db_ is available on conda-forge, so you can install it with the following command:

```bash
conda install -c conda-forge files2db
```

### 2.2 Input file

To run _files2db_, you need three different tables:

- _Files_: list of files to integrate, with their paths and formats.
- _ValueMap_: modalities mapping between the source files and the output database
- _FieldsRules_: rules to normalize the data (e.g. how to split or merge fields, expected formats, ...)

These tables can be in 3 `.csv` or 1 `.xlsx` file, and should be structured with the following columns:

- _Files_: `FilePath`, `SheetName`, `LineStart`, `LineEnd`, `Header`, `ColStart`, `ColEnd`, `ToAdd`, `AsCorrection`, `Separator`
- _ValueMap_: `Field`, `OriginalValue`, `NewValue`
- _FieldsRules_: `Field`, `Category`, `Sep`, `DelMatch`, `DelEnd`, `DelIn`, `DelStart`, `StripFrom`, `DataType`, `Contains`, `Min`, `Max`, `SepPattern`, `KeepLink`

Template of this files can be found in the [assets folder](https://github.com/LouisLeNezet/files2db/tree/main/docs/assets/)
Details on how to structure these tables can be found in the [documentation](https://louislenezet.github.io/files2db/quickstart/).

### 2.3 Launch of the script

Run

```bash
files2db --help
files2db --path "path/to/file.csv" --normalize --output "output/path"
```

This command line will launch the script directly in the command prompt with the file `path/to/file.csv` that you have chosen.
It will then normalize the data and output the resulting database in `output/path`.
You can also choose to only concatenate the files without normalizing them by omitting the `--normalize` flag.

## 3. Contributions and License

Contributions to this project are welcome! If you have any suggestions, improvements, or bug fixes, please feel free to submit a pull request. For major changes, please open an issue first to discuss what you would like to change. A detailed contribution guide can be found in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
