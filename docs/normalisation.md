# Normalisation

## Normalisation steps

After aggregating all input files, _files2db_ applies a series of normalisation rules when the `--normalize` option is enabled.
The rules are defined in the _FieldsRules_ table and are applied sequentially to each field.

These steps are applied in the following order:

1. Drop all only NA values rows and columns
2. Remove all ascii characters and encode data in UTF-8
3. Process each field defined in _FieldsRules_:
   1. [Split values (`Sep`)](#separate-modalities)
   2. [Clean values (`DelMatch`, `DelIn`, `DelStart`, `DelEnd` and `StripFrom`)](#clean-the-field)
   3. [Convert data type (`DataType`)](#convert-data-type)
   4. [Apply value mappings with _ValuesMap_ table](#value-mapping)
   5. [Validate values](#validate-values)
   6. [Split fields (`SepPattern`)](#split-fields)

!!! note

    Fields are processed in the order in which they appear in the **FieldsRules** table.
    This can affect the result when multiple rules interact.

!!! important

    The rules are applied sequentially, meaning that the output of one rule will be the input for the next rule.

## Normalisation rules

### Separate modalities

This step allows to split multiple values in a field using the specified separator.

With _Sep_ as `;`

<div class="table-center">
<table class="docutils">
  <thead>
    <tr>
      <th colspan="1">Before</th>
      <th colspan="3">After</th>
    </tr>
    <tr>
      <th>MyField</th>
      <th>MyField_1</th>
      <th>MyField_2</th>
      <th>MyField_3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A;B;C</td>
      <td>A</td>
      <td>B</td>
      <td>C</td>
    </tr>
  </tbody>
</table>
</div>

!!! warning

    The separator cannot be a comma (`,`) as it is used to split the modalities in the _FieldsRules_ table.

### Clean the field

This step allows to clean the field using regular expression patterns and is case sensitive.

- _DelMatch_: remove values that completely match the pattern
- _DelIn_: remove every occurrence of the pattern within the value
- _DelStart_: remove the pattern when it occurs at the beginning of the value
- _DelEnd_: remove the pattern when it occurs at the end of the value
- _StripFrom_: remove the pattern and everything that follows it

With `{pattern}` as `A`:

<div class="table-center">
<table class="docutils">
  <thead>
    <tr>
      <th>Type</th>
      <th>Regex equivalent</th>
      <th>A</th>
      <th>AA</th>
      <th>AB</th>
      <th>BA</th>
      <th>BAC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><em>DelMatch</em></td>
      <td><code>^{pattern}$</code></td>
      <td></td>
      <td>AA</td>
      <td>AB</td>
      <td>BA</td>
      <td>BAC</td>
    </tr>
    <tr>
      <td><em>DelIn</em></td>
      <td><code>{pattern}</code></td>
      <td></td>
      <td></td>
      <td>B</td>
      <td>B</td>
      <td>BC</td>
    </tr>
    <tr>
      <td><em>DelStart</em></td>
      <td><code>^{pattern}</code></td>
      <td></td>
      <td>A</td>
      <td>B</td>
      <td>BA</td>
      <td>BAC</td>
    </tr>
    <tr>
      <td><em>DelEnd</em></td>
      <td><code>{pattern}$</code></td>
      <td></td>
      <td>A</td>
      <td>AB</td>
      <td>B</td>
      <td>BAC</td>
    </tr>
    <tr>
      <td><em>StripFrom</em></td>
      <td><code>{pattern}.*$</code></td>
      <td></td>
      <td></td>
      <td></td>
      <td>B</td>
      <td>B</td>
    </tr>
  </tbody>
</table>
</div>

!!! note

    For details on the regular expression syntax, please refer to the
    [Python documentation](https://docs.python.org/3/library/re.html#re-syntax) and test them using
    the [regex101](https://regex101.com/) website.

### Convert data type

This step allows to convert the data type of the field to one of the following:

- `lower`: string converted to lowercase
- `UPPER`: string converted to uppercase
- `Title`: string converted to title case (first letter of each word capitalized)
- `date`: date in the format DD.MM.YYYY
- `int`: integer number (e.g. `"1"` and `"1.2"` will become `1`)
- `float`: floating-point number (e.g. `"1.2"` and `"1,2"` will become `1.2`)
- `string`: remains a string
- `bool`: boolean (e.g. case insensitive `"TRUE"`, `"1"` will become `True` while `"false"` and `0` will become `False`)

### Value mapping

This step allows to apply value mappings defined in the _ValuesMap_ table.
For each `Field`provided, the `OriginalValues` will be split by a comma (`,`) and each resulting
modalities, if fully matched, will be replaced by the `NewValue`.

With _ValuesMap_ as:

<div class="table-center">
<table class="docutils">
  <thead>
    <tr>
      <th>Field</th>
      <th>OriginalValues</th>
      <th>NewValue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ColA</td>
      <td>OldVal1,OldVal2</td>
      <td>NewVal1</td>
    </tr>
    <tr>
      <td>ColA</td>
      <td>OldVal3</td>
      <td>NewVal2</td>
    </tr>
    <tr>
      <td>ColB</td>
      <td>OldVal4</td>
      <td>NewVal3</td>
    </tr>
  </tbody>
</table>
</div>

Then :

<div class="table-center">
<table class="docutils">
  <thead>
    <tr>
      <th colspan="2">Before</th>
      <th colspan="2">After</th>
    </tr>
    <tr>
      <th>ColA</th>
      <th>ColB</th>
      <th>ColA</th>
      <th>ColB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OldVal1</td>
      <td>OldVal4</td>
      <td>NewVal1</td>
      <td>NewVal3</td>
    </tr>
    <tr>
      <td>OldVal3</td>
      <td>OldVal5</td>
      <td>NewVal2</td>
      <td>OldVal5</td>
    </tr>
  </tbody>
</table>
</div>

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

### Split fields

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

<div class="table-center">
<table class="docutils">
  <thead>
    <tr>
      <th colspan="1">Before</th>
      <th colspan="4">After</th>
    </tr>
    <tr>
      <th rowspan="2">MyField</th>
      <th colspan="2">KeepLink = True</th>
      <th colspan="2">KeepLink = False</th>
    </tr>
    <tr>
      <th>MyField_Int</th>
      <th>MyField_String</th>
      <th>Int</th>
      <th>String</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1234ABCD</td>
      <td>1234</td>
      <td>ABCD</td>
      <td>1234</td>
      <td>ABCD</td>
    </tr>
    <tr>
      <td>ABCD 1234</td>
      <td>1234</td>
      <td>ABCD</td>
      <td>1234</td>
      <td>ABCD</td>
    </tr>
    <tr>
      <td>456 ABCD 1234</td>
      <td>456</td>
      <td>ABCD</td>
      <td>456</td>
      <td>ABCD</td>
    </tr>
  </tbody>
</table>
</div>

#### More complex example

A more complex example when you expect either 1 or 2 value, and if two then split it into left and right.

With `SepPattern` = `((?P<Left>[A-E])(\/*)(?P<Right>[A-E]))|(?P<Mono>[A-E])`

<div class="table-center">
<table class="docutils">
  <thead>
    <tr>
      <th colspan="1">Before</th>
      <th colspan="3">After</th>
    </tr>
    <tr>
      <th>MyField</th>
      <th>Left</th>
      <th>Right</th>
      <th>Mono</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A/B</td>
      <td>A</td>
      <td>B</td>
      <td></td>
    </tr>
    <tr>
      <td>BE</td>
      <td>B</td>
      <td>E</td>
      <td></td>
    </tr>
    <tr>
      <td>D</td>
      <td></td>
      <td></td>
      <td>D</td>
    </tr>
  </tbody>
</table>
</div>
