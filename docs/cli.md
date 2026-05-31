# Command Line Interface

`files2db` is a python package providing a cli interface as follow:

```bash
files2db --help
files2db --path <path/to/file.csv> \
    --output <output.csv> \
    --normalize \
    --error-report <error_report.csv>
```

This command line will launch the script directly in the command prompt with the file `path/to/file.csv` that you have chosen.
It will then normalize the data and output the resulting database in `output/path`.
You can also choose to only concatenate the files without normalizing them by omitting the `--normalize` flag.
