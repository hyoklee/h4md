#!/usr/bin/env python3
"""
h4md - Convert HDF4 datasets and attributes to markdown
"""
import click
from pyhdf.SD import SD, SDC
import os

def format_dataset(dataset):
    """Format a dataset's information as markdown."""
    info = dataset.info()
    print(info)
    # attrs = dataset.attributes()
    
    md = f"### Dataset: {dataset.name()}\n\n"
    md += f"- **Shape**: {info[2]}\n"
    md += f"- **Type**: {info[3]}\n"
    
    # if attrs:
    #     md += "\n#### Attributes:\n\n"
    #     for name, value in attrs.items():
    #         md += f"- **{name}**: {value}\n"
    
    return md

def hdf4_to_markdown(file_path):
    """Convert HDF4 file content to markdown format."""
    try:
        hdf = SD(file_path, SDC.READ)
    except Exception as e:
        raise click.ClickException(f"Error opening HDF4 file: {e}")

    datasets = hdf.datasets()
    print(datasets)
    # file_attrs = hdf.attributes()
    
    md = f"# HDF4 File: {os.path.basename(file_path)}\n\n"
    
    # if file_attrs:
    #     md += "## Global Attributes\n\n"
    #     for name, value in file_attrs.items():
    #         md += f"- **{name}**: {value}\n"
    #     md += "\n"
    
    if datasets:
        md += "## Datasets\n\n"
        for name, info in datasets.items():
            dataset = hdf.select(name)
            md += format_dataset(dataset)
            md += "\n"
    
    hdf.end()
    return md

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path(), required=False)
def main(input_file, output_file=None):
    """
    Convert HDF4 file to markdown format.
    
    INPUT_FILE: Path to the input HDF4 file
    OUTPUT_FILE: Optional path for the output markdown file (defaults to input_file with .md extension)
    """
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.md'
    
    try:
        markdown_content = hdf4_to_markdown(input_file)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        click.echo(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        raise click.ClickException(str(e))

if __name__ == '__main__':
    main()
