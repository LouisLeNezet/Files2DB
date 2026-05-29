# `files2db`: Contributing Guidelines

Hi there!
Many thanks for taking an interest in improving `files2db`.

We try to manage the required tasks for `files2db` using GitHub issues, you probably came to this page when creating one.

## Contribution workflow

If you'd like to write some code for `files2db`, the standard workflow is as follows:

1. Check that there isn't already an issue about your idea in the [files2db](https://github.com/LouisLeNezet/files2db/issues) to avoid duplicating work. If there isn't one already, please create one so that others know you're working on this
2. [Fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) the [files2db repository](https://github.com/LouisLeNezet/files2db/) to your GitHub account
3. Checkout the devel branch and create your work environment
4. Make the necessary changes / additions within your forked repository
5. Submit a Pull Request against the `devel` branch and wait for the code to be reviewed and merged

If you're not used to this workflow with git, you can start with some [docs from GitHub](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests) or even their [excellent `git` resources](https://try.github.io/).

## Install the development environment

You will need the conda environment mentioned in the `environment.yml` file.
To install it use:

```bash
conda env create --file environment.yml
conda activate env_concat
# Run the following to update it
conda env update --file environment.yml
```

## Tests

You have the option to test your changes locally by running the unittests.
Execute all the tests with the following command:

```bash
pytest --cov --cov-report=lcov
coverage lcov
```

When you create a pull request with changes, [GitHub Actions](https://github.com/features/actions) will run automatic tests.
Typically, pull-requests are only fully reviewed when these tests are passing, though of course we can help out before then.

## Patch

:warning: Only in the unlikely and regretful event of a release happening with a bug.

- On your own fork, make a new branch `patch` based on `upstream/main`.
- Fix the bug, and bump version (X.Y.Z+1).
- Open a pull-request from `patch` to `main`/`master` with the changes.

## Package contribution conventions

To make the `files2db` code and processing logic more understandable for new contributors and to ensure quality, we semi-standardise the way the code and other contributions are written.

### Adding a new function

If you wish to contribute a new function, please use the following coding standards:

1. Use snake_case
2. Lint the code
3. Add documentation and example through docstring syntax
4. Add a unittest and aim for a full coverage

### Update the documentation

```bash
mkdocs serve
```
