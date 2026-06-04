# Normalisation steps

After aggregation all the data, `files2db` will apply, if `--normalize` is provided, the different normalisation
steps to the data, as specified in the _FieldsRules_ table.

These steps are applied in the following order:

1. Drop all only NA values rows and columns
2. Remove all ascii characters and encode data in UTF-8
3. For each field in the _FieldsRules_ table order (full match of `Field` value):
    1. Separate the modalities in the field using `Sep`
    2. Clean the field using:
        1. Remove full match of `DelMatch` pattern
        2. Remove substring match of `DelIn` pattern
        3. Remove start match of `DelStart` pattern
        4. Remove end match of `DelEnd` pattern
        5. Strip everything after `StripFrom` pattern
    3. Convert the field to the specified `DataType`
    4. Use the __ValuesMap__ table to map the values in the field (full match of `Value` value, split by `,`)
    5. Validate the field using:
        1. Check if the field contains the `Contains` pattern
        2. Check if the field values are between `Min` and `Max` values (if applicable)
    6. Split the field into several fields using `SepPattern` and keep the link to the original data if `KeepLink` is true
