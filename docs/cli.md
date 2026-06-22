# Command Line Interface

_files2db_ is a python package providing a cli interface as follow:

```bash
# Get help
files2db --help

# Use one file with all tables
files2db --path-orga path/to/orga.{csv,xlsx} \
    --output-dir results \
    --output-prefix normalized_data \
    --normalize

# Give each table separately
files2db --path-files path/to/files.csv \
    --path-fields-rules path/to/fields_rules.csv \
    --path-values-map path/to/values_map.csv \
    --output-dir results \
    --output-prefix normalized_data \
    --normalize
```

You can provide the 3 tables necessary in two ways:

- use `--path-orga` with one file, either a `.xlsx` with `Files`, `FieldsRules` and `ValuesMap` sheets,
  or a `.csv` with `file`, `path`, `sep` columns giving the path to the three tables.
- use `--path-files`, `--path-fields-rules` and `--path-values-map` to provide each table separately.

_files2db_ will then normalize the data and output the resulting database in `results/normalize_data{,_errors}.csv`.
You can also choose to only concatenate the files without normalizing them by omitting the `--normalize` flag.
