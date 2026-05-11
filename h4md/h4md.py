#!/usr/bin/env python3
"""
h4md - Convert HDF4 datasets and attributes to markdown
"""
import click
from pyhdf.SD import SD, SDC
import os
import sys

def format_dataset(dataset, dataset_name=None):
    """Format a dataset's information as markdown."""
    try:
        # Get basic dataset information
        info = dataset.info()
        
        # Use provided dataset_name or extract from info tuple when name() method fails
        if dataset_name is not None:
            name = dataset_name
        else:
            try:
                name = dataset.name()
            except (AttributeError, Exception):
                # Extract name from info tuple: (name, rank, shape, data_type, n_attrs)
                name = info[0] if info and len(info) > 0 else "Unknown"
        
        shape = info[2]
        data_type = info[3]
        
        # Build markdown content
        md = f"### Dataset: {name}\n\n"
        md += f"- **Shape**: {shape}\n"
        md += f"- **Type**: {data_type}\n"
        
        # Get attributes if any
        try:
            # This returns a dictionary of attributes
            attrs_dict = dataset.attributes()
            
            if attrs_dict:
                md += "\n#### Attributes:\n\n"
                # The attributes dict contains values directly
                for attr_name, attr_value in attrs_dict.items():
                    # Handle different attribute value types
                    if isinstance(attr_value, bytes):
                        # Convert bytes to string safely, replacing null bytes
                        try:
                            attr_str = attr_value.decode('utf-8', errors='replace').replace('\x00', '')
                        except:
                            attr_str = f"<binary data length={len(attr_value)}>"
                    elif isinstance(attr_value, (list, tuple)):
                        # Handle lists/tuples
                        attr_str = str(attr_value)
                    else:
                        # Handle other types (strings, numbers)
                        attr_str = str(attr_value)
                    
                    # Truncate very long attributes to avoid huge markdown files
                    if len(attr_str) > 50:
                        attr_str = attr_str[:50] + "... (truncated, length=" + str(len(attr_str)) + ")"
                    
                    # Clean up any remaining control characters
                    attr_str = ''.join(char for char in attr_str if ord(char) >= 32 or char in '\n\r\t')
                    
                    md += f"- **{attr_name}**: {attr_str}\n"
        except Exception as attrs_err:
            # In case of error, continue with other parts of the dataset
            md += "\n*Error reading attributes*\n"
        
        return md
    except Exception as e:
        # If there's an error with the dataset, return a placeholder
        return f"### Dataset: {dataset.name() if hasattr(dataset, 'name') else 'Unknown'}\n\n*Error formatting dataset*\n"

def hdf4_to_markdown(file_path):
    """Convert HDF4 file content to markdown format."""
    hdf = None
    try:
        # Check if file exists and is readable
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Open the HDF4 file
        hdf = SD(file_path, SDC.READ)
        
        # Get filename for the header
        filename = os.path.basename(file_path)
        md = f"# HDF4 File: {filename}\n\n"
        
        # Process global attributes
        try:
            # This returns a dictionary of attributes
            attrs_dict = hdf.attributes()
            
            if attrs_dict:
                md += "## Global Attributes\n\n"
                # Use the attributes dictionary directly
                for attr_name, attr_value in attrs_dict.items():
                    # Handle different attribute value types
                    if isinstance(attr_value, bytes):
                        # Convert bytes to string safely, replacing null bytes
                        try:
                            attr_str = attr_value.decode('utf-8', errors='replace').replace('\x00', '')
                        except:
                            attr_str = f"<binary data length={len(attr_value)}>"
                    elif isinstance(attr_value, (list, tuple)):
                        # Handle lists/tuples
                        attr_str = str(attr_value)
                    else:
                        # Handle other types (strings, numbers)
                        attr_str = str(attr_value)
                    
                    # Truncate very long attributes to avoid huge markdown files
                    if len(attr_str) > 50:
                        attr_str = attr_str[:50] + "... (truncated, length=" + str(len(attr_str)) + ")"
                    
                    # Clean up any remaining control characters
                    attr_str = ''.join(char for char in attr_str if ord(char) >= 32 or char in '\n\r\t')
                    
                    md += f"- **{attr_name}**: {attr_str}\n"
                md += "\n"
        except Exception:
            # In case of error, continue with datasets
            pass
        
        # Process datasets
        try:
            # Get all dataset names
            datasets_dict = hdf.datasets()
            dataset_names = list(datasets_dict.keys())
            
            if dataset_names:
                md += "## Datasets\n\n"
                for ds_name in dataset_names:
                    try:
                        # Select and process each dataset
                        dataset = hdf.select(ds_name)
                        md += format_dataset(dataset, ds_name)
                        md += "\n"
                    except Exception:
                        # If there's an error with a dataset, continue with others
                        md += f"### Dataset: {ds_name}\n\n*Error processing dataset*\n\n"
        except Exception:
            # If there's an error getting datasets, note it
            md += "*Error reading datasets*\n"
        
        return md
    except Exception as e:
        # Handle any other errors
        error_msg = str(e)
        if "File is supported, must be either hdf, cdf, netcdf" in error_msg:
            raise click.ClickException(f"File '{os.path.basename(file_path)}' is not a valid HDF4 file. It may be a different format (NetCDF, HDF5, etc.).")
        elif "No such file or directory" in error_msg:
            raise click.ClickException(f"File not found: {file_path}")
        else:
            raise click.ClickException(f"Error processing HDF4 file: {e}")
    finally:
        # Always close the file
        if hdf is not None:
            try:
                hdf.end()
            except Exception:
                # If we can't close it cleanly, that's ok
                pass

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

def test_function():
    """Test function to debug the hdf4_to_markdown function"""
    import tempfile
    from pyhdf.SD import SD, SDC
    import numpy as np
    
    # Create a temporary HDF4 file
    with tempfile.NamedTemporaryFile(suffix='.hdf', delete=False) as tmp:
        file_path = tmp.name
    
    print(f"Creating test HDF4 file at: {file_path}")
    try:
        hdf = SD(file_path, SDC.WRITE | SDC.CREATE)
        
        # Add global attributes
        hdf.setattr('title', 'Test Dataset')
        hdf.setattr('description', 'Sample HDF4 file for testing')
        
        # Create a sample dataset
        data = np.arange(6).reshape(2, 3)
        sds = hdf.create('sample_data', SDC.FLOAT32, (2, 3))
        sds.data[:] = data
        sds.setattr('units', 'meters')
        
        hdf.end()
        
        # Now convert to markdown
        print("\nTesting hdf4_to_markdown function:")
        markdown = hdf4_to_markdown(file_path)
        print("\nGenerated Markdown:")
        print(markdown)
        
        return True
    except Exception as e:
        print(f"\nTest FAILED with error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        import os
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Removed temporary file: {file_path}")
            except:
                print(f"Failed to remove temporary file: {file_path}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main()
    else:
        print("Running test function...")
        success = test_function()
        print(f"Test {'succeeded' if success else 'failed'}")
