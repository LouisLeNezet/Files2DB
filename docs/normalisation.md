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
   - [Apply value mappings with _ValuesMap_ table](#apply-value-mappings-with-valuesmap-table)
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
The separator cannot be a comma (`,`) as it is used to split the modalities in the _FieldsRules_ table.

### Clean the field using `DelMatch`, `DelIn`, `DelStart`, `DelEnd` and `StripFrom`

This step allows to clean the field using regular expression patterns and is case sensitive.

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

!!! note
For details on the regular expression syntax, please refer to the
[Python documentation](https://docs.python.org/3/library/re.html#re-syntax) and test them using
the [regex101](https://regex101.com/) website.

### Convert data type (`DataType`)

This step allows to convert the data type of the field to one of the following:

- `lower`: string converted to lowercase
- `UPPER`: string converted to uppercase
- `Title`: string converted to title case (first letter of each word capitalized)
- `date`: date in the format DD.MM.YYYY
- `int`: integer number (e.g. `"1"` and `"1.2"` will become `1`)
- `float`: floating-point number (e.g. `"1.2"` and `"1,2"` will become `1.2`)
- `string`: remains a string
- `bool`: boolean (e.g. case insensitive `"TRUE"`, `"1"` will become `True` while `"false"` and `0` will become `False`)

### Apply value mappings with _ValuesMap_ table

This step allows to apply value mappings defined in the _ValuesMap_ table.
For each `Field`provided, the `OriginalValues` will be split by a comma (`,`) and each resulting
modalities, if fully matched, will be replaced by the `NewValue`.

With _ValuesMap_ as:

| Field | OriginalValues  | NewValue |
| ----- | --------------- | -------- |
| ColA  | OldVal1,OldVal2 | NewVal1  |
| ColA  | OldVal3         | NewVal2  |
| ColB  | OldVal4         | NewVal3  |

<table style="margin: 0 auto;">
  <thead>
    <tr>
      <th colspan="2" style="text-align:center">Before</th>
      <th colspan="2" style="text-align:center">After</th>
    </tr>
    <tr>
      <th style="text-align:center">ColA</th>
      <th style="text-align:center">ColB</th>
      <th style="text-align:center">ColA</th>
      <th style="text-align:center">ColB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th style="text-align:center">OldVal1</th>
      <th style="text-align:center">OldVal4</th>
      <th style="text-align:center">NewVal1</th>
      <th style="text-align:center">NewVal3</th>
    </tr>
    <tr>
      <th style="text-align:center">OldVal3</th>
      <th style="text-align:center">OldVal5</th>
      <th style="text-align:center">NewVal2</th>
      <th style="text-align:center">OldVal5</th>
    </tr>
  </tbody>
</table>

!!! note
Multiple mappings can be applied to the same field by defining multiple rows in the _ValuesMap_ table with the same _FieldName_.

    Multiple values can be mapped to the same value by separating them with a comma in the _OriginalValues_ column.

!!! important
This step is case sensitive except if the field has been converted to lowercase in the previous step.

### Validate values

This step allows to validate the field values using regular expression patterns.
Values that do not match the pattern will generate an error in the error output file.

There is two validation possible:

- `Contains`: list of values separated by a comma (`,`). This test is case sensitive.
- `Min` and `Max`: for numerical values only.

### Split fields (`SepPattern`)

This step allows to split the field into multiple fields using a regular expression pattern as separator.
This use named regex pattern to capture the new field.
`SepPattern` has to be in the form `(?P<NewFieldName>{pattern})`, `KeepLink` is a boolean stating if the
`NewFieldName` should be appended to the old `Field` or as a separate new field.

!!! note
For details on the regular expression syntax, please refer to the
[Python documentation](https://docs.python.org/3/library/re.html#re-syntax) and test them using
the [regex101](https://regex101.com/) website.

!!! warning
Only the first match of the pattern will be stored in the new field

#### Simple example

With `SepPattern` = `(?P<Int>\\d+)|(?P<String>[A-Za-z]+)`

<table style="margin: 0 auto;">
  <thead>
    <tr>
      <th colspan="1" style="text-align:center">Before</th>
      <th colspan="4" style="text-align:center">After</th>
    </tr>
    <tr>
      <th rowspan="2" style="text-align:center">MyField</th>
      <th colspan="2" style="text-align:center">KeepLink = True</th>
      <th colspan="2" style="text-align:center">KeepLink = False</th>
    </tr>
    <tr>
      <th style="text-align:center">MyField_Int</th>
      <th style="text-align:center">MyField_String</th>
      <th style="text-align:center">Int</th>
      <th style="text-align:center">String</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th style="text-align:center">1234ABCD</th>
      <th style="text-align:center">1234</th>
      <th style="text-align:center">ABCD</th>
      <th style="text-align:center">1234</th>
      <th style="text-align:center">ABCD</th>
    </tr>
    <tr>
      <th style="text-align:center">ABCD 1234</th>
      <th style="text-align:center">1234</th>
      <th style="text-align:center">ABCD</th>
      <th style="text-align:center">1234</th>
      <th style="text-align:center">ABCD</th>
    </tr>
    <tr>
      <th style="text-align:center">456 ABCD 1234</th>
      <th style="text-align:center">456</th>
      <th style="text-align:center">ABCD</th>
      <th style="text-align:center">456</th>
      <th style="text-align:center">ABCD</th>
    </tr>
  </tbody>
</table>

#### More complex example

A more complex example when you expect either 1 or 2 value, and if two then split it into left and right.

With `SepPattern` = `((?P<Left>[A-E])(\/*)(?P<Right>[A-E]))|(?P<Both>[A-E])`

<table style="margin: 0 auto;">
  <thead>
    <tr>
      <th colspan="1" style="text-align:center">Before</th>
      <th colspan="3" style="text-align:center">After</th>
    </tr>
    <tr>
      <th style="text-align:center">MyField</th>
      <th style="text-align:center">Left</th>
      <th style="text-align:center">Right</th>
      <th style="text-align:center">Both</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th style="text-align:center">A/B</th>
      <th style="text-align:center">A</th>
      <th style="text-align:center">B</th>
      <th style="text-align:center"></th>
    </tr>
    <tr>
      <th style="text-align:center">BE</th>
      <th style="text-align:center">B</th>
      <th style="text-align:center">E</th>
      <th style="text-align:center"></th>
    </tr>
    <tr>
      <th style="text-align:center">D</th>
      <th style="text-align:center"></th>
      <th style="text-align:center"></th>
      <th style="text-align:center">D</th>
    </tr>
  </tbody>
</table>
