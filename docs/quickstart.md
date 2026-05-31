# What you need

One excel file with 3 sheets named: "Files", "FieldsRules", "ValuesMap", or 3 different CSV files.

The columns expected for each of these files are the following, but you can find template for each of them in the [assets folder](https://github.com/LouisLeNezet/files2db/tree/main/assets).

## Files

This file contains the path to each file to aggregate to the database, with information on how to read the data.
You therefore need the following columns:

- `FilePath`: the absolute path to the file
- `SheetName`: the sheet name in case of an Excel file
- `Separator`: character used to separate the columns (e.g. `,`, `;`, `\t`, ` `), needed for plain text files (e.g. `.csv`, `.txt`, `.tsv`)
- `Header`: the line number where the column names are written
- `LineStart`: the starting line of the data
- `LineEnd`: the ending line of the data
- `ColStart`: the starting column of the data
- `ColEnd`: the ending column of the data
- `ToAdd`: a true/false value telling if this file should be aggregated or not
- `AsCorrection`: a true/false value telling if this file is a special file to be used for data correction

## FieldsRules

This file contains the different rules needed to normalize each variable in the aggregated data

- Field
- Category
- Sep
- DelMatch
- DelEnd
- DelIn
- DelStart
- StripFrom
- DataType
- Contains
- Min
- Max
- SepPattern
- KeepLink

## ValuesMap

This files contains modalities correspondance for each field

- Field
- Eq
- Value
