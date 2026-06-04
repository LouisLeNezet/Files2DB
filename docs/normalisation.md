# Normalisation steps

After aggregating all input files, `files2db` applies a series of normalisation rules when the `--normalize` option is enabled.
The rules are defined in the _FieldsRules_ table and are applied sequentially to each field.

These steps are applied in the following order:

1. Drop all only NA values rows and columns
2. Remove all ascii characters and encode data in UTF-8
3. Process each field defined in _FieldsRules_:
    - [Split values (`Sep`)](#separate-modalities-in-the-field-using-sep)
    - [Clean values (`DelMatch`, `DelIn`, `DelStart`, `DelEnd` and `StripFrom`)](#clean-the-field-using-delmatch-delin-delstart-delend-and-stripfrom)
    - [Convert data type (`DataType`)](#convert-data-type-datatype)
    - [Apply value mappings with __ValuesMap__ table](#apply-value-mappings-with-valuesmap-table)
    - [Validate values](#validate-values)
    - [Split fields (`SepPattern`)](#split-fields-seppattern)

!!! note
    Fields are processed in the order in which they appear in the **FieldsRules** table.
    This can affect the result when multiple rules interact.

!!! important
    The rules are applied sequentially, meaning that the output of one rule will be the input for the next rule.

## Normalisation rules

### Separate modalities in the field using `Sep`

This step allows to split multiple values in a field using the specified separator.

With _Sep_ as `;`

<table style="margin: 0 auto;">
  <thead>
    <tr>
      <th colspan="1" style="text-align:center">Before</th>
      <th colspan="3" style="text-align:center">After</th>
    </tr>
    <tr>
      <th style="text-align:center">MyField</th>
      <th style="text-align:center">MyField_1</th>
      <th style="text-align:center">MyField_2</th>
      <th style="text-align:center">MyField_3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:center">A;B;C</td>
      <td style="text-align:center">A</td>
      <td style="text-align:center">B</td>
      <td style="text-align:center">C</td>
    </tr>
  </tbody>
</table>

!!! warning
    The separator cannot be `,` as it is used to split the modalities in the _FieldsRules_ table.

### Clean the field using `DelMatch`, `DelIn`, `DelStart`, `DelEnd` and `StripFrom`

This step allows to clean the field using regular expression patterns and is case sensitive.
For details on the regular expression syntax, please refer to the
[Python documentation](https://docs.python.org/3/library/re.html#re-syntax) and test them using
the [regex101](https://regex101.com/) website.

- _DelMatch_: remove values that completely match the pattern
- _DelIn_: remove every occurrence of the pattern within the value
- _DelStart_: remove the pattern when it occurs at the beginning of the value
- _DelEnd_: remove the pattern when it occurs at the end of the value
- _StripFrom_: remove the pattern and everything that follows it

With _pattern_ as `A`:

| Type        | Regex equivalent | A   | AA  | AB  | BA  | BAC |
| ----------- | ---------------- | --- | --- | --- | --- | --- |
| _DelMatch_  | `^{pattern}$`    |     | AA  | AB  | BA  | BAC |
| _DelIn_     | `{pattern}`      |     |     | B   | B   | BC  |
| _DelStart_  | `^{pattern}`     |     | A   | B   | BA  | BAC |
| _DelEnd_    | `{pattern}$`     |     | A   | AB  | B   | BAC |
| _StripFrom_ | `{pattern}.*$`   |     |     |     | B   | B   |

### Convert data type (`DataType`)

This step allows to convert the data type of the field to one of the following:

- `lower`: string converted to lowercase
- `UPPER`: string converted to uppercase
- `Title`: string converted to title case (first letter of each word capitalized)
- `date`: date in the format DD.MM.YYYY
- `int`: integer number
- `float`: floating-point number
- `string`: remains a string
- `bool`: boolean (True/False)

### Apply value mappings with __ValuesMap__ table

This step allows to apply value mappings defined in the _ValuesMap_ table.
The mapping is applied to the field value (i.e.full match) and replaces it with the corresponding mapped value.

!!! note
    Multiple mappings can be applied to the same field by defining multiple rows in the _ValuesMap_ table with the same _FieldName_.
    
    Multiple values can be mapped to the same value by separating them with a comma in the _OriginalValues_ column.

!!! important
    This step is case sensitive except if the field has been converted to lowercase in the previous step.

### Validate values

This step allows to validate the field values using regular expression patterns.
Values that do not match the pattern are removed from the field.

### Split fields (`SepPattern`)

This step allows to split the field into multiple fields using a regular expression pattern as separator.
With _SepPattern_ as `\s*;\s*` (semicolon with optional surrounding whitespace):

