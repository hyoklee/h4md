# h4md (HDF4 to Markdown)

A command-line tool to convert HDF4 datasets and attributes to markdown format.

## Installation

You can install h4md directly from the repository:

```bash
pip install .

## Usage

After installation, you can use the `h4md` command directly:

```bash
h4md input.hdf output.md
```

If you don't specify an output file, it will use the input filename with a `.md` extension:
```bash
h4md input.hdf
# Creates input.md
```

## Output Format

The tool generates markdown with the following structure:
- File name as main heading
- Global attributes section
- Datasets section with each dataset containing:
  - Shape information
  - Data type
  - Dataset-specific attributes
