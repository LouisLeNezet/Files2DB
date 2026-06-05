# Quickstart

## Installation

_files2db_ is available on conda-forge, so you can install it with the following command:

```bash
conda install -c conda-forge files2db
```

## Table that you will need

One excel file with 3 sheets named: _Files_, _FieldsRules_, _ValuesMap_, or 3 different CSV files.

The columns expected for each of these files are the following, but you can find template for each of them in the [assets folder](https://github.com/LouisLeNezet/files2db/tree/main/docs/assets).

### _Files_ table

This table contains the path to each file to aggregate to the database, with information on how to read the data.
You therefore need the following columns:

- `FilePath`: the absolute path to the file
- `SheetName`: the sheet name in case of an Excel file
- `Separator`: character used to separate the columns (e.g. `;`, `\t`, ` `), needed for plain text files (e.g. `.csv`, `.txt`, `.tsv`) (Note: `,` cannot be used as it is used to split the modalities in the _FieldsRules_ table)
- `Header`: the line number where the column names are written
- `LineStart`: the starting line of the data
- `LineEnd`: the ending line of the data
- `ColStart`: the starting column of the data
- `ColEnd`: the ending column of the data
- `ToAdd`: a true/false value telling if this file should be aggregated or not
- `AsCorrection`: a true/false value telling if this file is a special file to be used for data correction
- `meta_*`: any column starting with `meta_` will be added as an additional value for each row of the file.

{{ read_csv('assets/files.csv', sep=";", keep_default_na=False) }}

### _FieldsRules_ table

This table contains the different rules needed to normalize each variable in the aggregated data.
More information on the different rules can be found in the [documentation](https://louislenezet.github.io/files2db/normalisation/).

- `Field`: name of the field to normalize
- `Category`: name of the field category
- `Sep`: character used to separate the modalities in the field (e.g. `,`, `;`, `\t`, ` `)
- `SepPattern`: regular expression pattern to separate the modalities in the field
- `KeepLink`: a boolean value telling if the link to the original data should be kept after separating the modalities in the field
- `DelMatch`: a regular expression pattern to delete in the field (fully match)
- `DelEnd`: a regular expression pattern to delete at the end of the field
- `DelIn`: a regular expression pattern to delete in the field (partially match)
- `DelStart`: a regular expression pattern to delete at the start of the field
- `StripFrom`: a regular expression pattern to strip from the field (fully match)
- `DataType`: the data type to assign to the field (e.g. `str`, `int`, `float`, `date`)
- `Contains`: a regular expression pattern to check if the field contains a specific value
- `Min`: the minimum value for the field (if applicable)
- `Max`: the maximum value for the field (if applicable)

{{ read_csv('assets/field_rules.csv', sep=";", keep_default_na=False) }}

### _ValuesMap_ table

This table contains modalities correspondance for each field

- `Field`: name of the field to normalize
- `OriginalValues`: modalities list to modify separated by a `,`
- `NewValue`: new value to assign to each modality listed in `OriginalValue`

{{ read_csv('assets/values_map.csv', sep=";", keep_default_na=False) }}

#### Explanation:

- values `A` and `otherA` in field `ValueToMap` will be modify as `MyA`
- values `B` in field `ValueToMap` will be modify as `MyB`
- values `A`, `B` and `1` in field `ValueToMap2` will be modify as `AB1`
