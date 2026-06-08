#!/usr/bin/env python3

# files2db - A tool to normalize and combine flat files into a database
# Copyright (C) 2024 Louis Le Nezet
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Created on 22/10/2021
@author: LouisLeNezet
Script to launch the application
"""

import logging
import sys

import typer

from files2db.__version__ import __version__
from files2db.main import main

from .read_file.orga_read import get_db_from

logging.basicConfig(level=logging.INFO)

app = typer.Typer(
    name="files2db",
    add_completion=False,
    invoke_without_command=True,
)


def show_notice():
    typer.echo(f"files2db v{__version__}  Copyright (C) 2024 Louis Le Nezet")
    typer.echo("This program comes with ABSOLUTELY NO WARRANTY; for details type '--warranty'.")
    typer.echo("This is free software, and you are welcome to redistribute it")
    typer.echo("under certain conditions; type '--license' for details.\n")


@app.callback()
def cli(
    ctx: typer.Context,
    path_orga: str = typer.Option(
        None, "--path-orga", "-g", help="Path to the file with the three tables."
    ),
    path_files: str = typer.Option(
        None, "--path-files", "-f", help="Path to the table listing the files to aggregate."
    ),
    path_fields_rules: str = typer.Option(
        None,
        "--path-fields-rules",
        "-r",
        help="Path to the table with the fields normalising rules.",
    ),
    path_values_map: str = typer.Option(
        None, "--path-values-map", "-m", help="Path to the modalities mapping table."
    ),
    sep: str = typer.Option(
        None, "--sep", "-s", help="Separator to be used for the input csv files."
    ),
    normalize: bool = typer.Option(
        False, "--normalize", "-n", help="Normalize the data after concatenation."
    ),
    output_dir: str = typer.Option(
        "./results/", "--output-dir", "-o", help="Output path for the aggregated data."
    ),
    output_prefix: str = typer.Option(
        "data_processed", "--output-prefix", "-p", help="Prefix used for each file generated."
    ),
    license: bool = typer.Option(False, "--license", help="Show license information and exit."),
    warranty: bool = typer.Option(False, "--warranty", help="Show warranty disclaimer and exit."),
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
):
    if len(ctx.args) == 0 and len(sys.argv) == 1:
        typer.echo(ctx.get_help())
        raise typer.Exit()

    if version:
        typer.echo(f"files2db version {__version__}")
        raise typer.Exit()

    if license:
        typer.echo(
            "This program is free software: you can redistribute it and/or modify\n"
            "it under the terms of the GNU General Public License as published by\n"
            "the Free Software Foundation, either version 3 of the License, or\n"
            "(at your option) any later version.\n\n"
            "See <https://www.gnu.org/licenses/> for details."
        )
        raise typer.Exit()

    if warranty:
        typer.echo(
            "This program is distributed in the hope that it will be useful,\n"
            "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n\n"
            "See <https://www.gnu.org/licenses/> for details."
        )
        raise typer.Exit()

    show_notice()

    if not path_orga and not path_files:
        typer.echo(
            "Error: You must provide either:\n"
            "  --path-orga PATH\n"
            "or\n"
            "  --path-files PATH [--path-fields-rules PATH] [--path-values-map PATH]"
        )
        raise typer.Exit(code=1)

    files_list, fields_rules, values_map = get_db_from(
        path_orga=path_orga,
        path_files=path_files,
        path_fields_rules=path_fields_rules,
        path_values_map=path_values_map,
        sep=sep,
    )

    if normalize and fields_rules is None and values_map is None:
        raise ValueError("Normalising step needs at least fields rules or values map table.")

    # Call the main logic
    main(
        files_list=files_list,
        fields_rules=fields_rules,
        values_map=values_map,
        normalize=normalize,
        output_dir=output_dir,
        output_prefix=output_prefix,
    )


if __name__ == "__main__":
    app()
